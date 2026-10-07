"""Validate exported historical tables; never infer or publish missing results."""
import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path


def close(a, b, label, abs_tol=0.1):
    if not math.isclose(float(a), float(b), rel_tol=1e-6, abs_tol=abs_tol):
        raise ValueError(f'{label}: {a} != {b}')


def number(row, key):
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f'Nonfinite {key}')
    return value


def validate(tables, years=(2021, 2026), thresholds=(0.5, 0.6, 0.7)):
    if tuple(thresholds) != (0.5, 0.6, 0.7):
        raise ValueError('Prespecified 0.50/0.60/0.70 thresholds must be retained')
    coverage = tables['coverage']
    whole = tables['whole_window_areas']
    changes = tables['matched_changes']
    transitions = tables['transitions']
    provenance = tables['provenance']
    if {int(r['year']) for r in provenance} != set(years):
        raise ValueError('Missing or unexpected provenance year')
    canonical_sources = []
    for row in provenance:
        year = int(row['year'])
        raw_id = row['asset_id']
        dataset = 'GOOGLE/DYNAMICWORLD/V1'
        full_id = raw_id.startswith(dataset + '/')
        if row.get('dataset', dataset if full_id else '') != dataset:
            raise ValueError('Incorrect source asset')
        index = raw_id[len(dataset) + 1:] if full_id else raw_id
        if not re.fullmatch(r'\d{8}T\d{6}_\d{8}T\d{6}_T\d{2}[A-Z]{3}', index):
            raise ValueError('Malformed source image index')
        date = datetime.strptime(row['acquired_utc'], '%Y-%m-%d %H:%M:%S')
        if date.year != year or date.month != 9 or index[:8] != date.strftime('%Y%m%d'):
            raise ValueError('Acquisition outside matching September window')
        if row.get('start_inclusive', f'{year}-09-01') != f'{year}-09-01' or row.get('end_exclusive', f'{year}-10-01') != f'{year}-10-01':
            raise ValueError('Inconsistent monthly window metadata')
        sentinel_id = 'COPERNICUS/S2_HARMONIZED/' + index
        if row.get('source_sentinel2_id', sentinel_id) != sentinel_id:
            raise ValueError('Sentinel source identifier disagrees with image index')
        canonical_sources.append({'year': year, 'raw_asset_id': raw_id,
            'canonical_asset_id': dataset + '/' + index,
            'identifier_origin': 'exported_full_path' if full_id else 'derived_from_declared_dataset_and_exported_index',
            'source_sentinel2_id': sentinel_id, 'acquired_utc': row['acquired_utc'],
            'independently_fetched': False})
        if not row['dynamicworld_algorithm_version'] or not row['qa_algorithm_version']:
            raise ValueError('Missing model/QA version')
        if row['crs'] != 'EPSG:32639' or row['grid_transform'] != '10,0,544635,0,-10,2845905':
            raise ValueError('Inconsistent grid metadata')
    if len(coverage) != len(years)*len(thresholds):
        raise ValueError('Missing or extra coverage rows')
    if len(whole) != len(years)*len(thresholds)*10:
        raise ValueError('Missing or extra whole-window rows')
    window_areas = []
    for year in years:
        source_ids = [r['asset_id'] for r in provenance if int(r['year']) == year]
        if len(set(source_ids)) != len(source_ids):
            raise ValueError('Duplicate source provenance')
        if len({r['asset_id'] for r in provenance if int(r['year']) == year}) < 3:
            raise ValueError('Fewer than three distinct source assets for a year')
        previous = float('inf')
        for threshold in thresholds:
            rows = [r for r in coverage if int(r['year']) == year and float(r['confidence_threshold']) == threshold]
            if len(rows) != 1:
                raise ValueError('Duplicated/missing coverage key')
            row = rows[0]
            window = number(row, 'window_area_m2')
            valid = number(row, 'accepted_area_m2')
            unknown = number(row, 'unknown_area_m2')
            observed = number(row, 'observed_area_m2')
            if window <= 0 or not 0 <= valid <= observed <= window or unknown < 0:
                raise ValueError('Invalid area or observed/accepted support ordering')
            if int(row['minimum_observations']) != 3 or valid > previous + 0.1:
                raise ValueError('Inconsistent observation rule or confidence sensitivity')
            previous = valid
            close(valid + unknown, window, 'Whole-window conservation')
            close(valid/window, number(row, 'accepted_fraction'), 'Accepted fraction', abs_tol=1e-9)
            window_areas.append(window)
            classes = [r for r in whole if int(r['year']) == year and float(r['confidence_threshold']) == threshold]
            if len(classes) != 10 or {int(r['class_code']) for r in classes} != {*range(9), 255}:
                raise ValueError('All nine classes and Unknown must be present exactly once')
            if any(number(r, 'area_m2') < 0 for r in classes):
                raise ValueError('Negative class area')
            close(sum(number(r, 'area_m2') for r in classes), window, 'Class totals')
            close(next(number(r,'area_m2') for r in classes if int(r['class_code']) == 255), unknown, 'Unknown area')
    for window in window_areas:
        close(window, window_areas[0], 'Consistent study-window area')
    keys = {(int(r['before_year']), int(r['after_year']), float(r['confidence_threshold'])) for r in changes}
    expected = {(a,b,t) for i,a in enumerate(years) for b in years[i+1:] for t in thresholds}
    if keys != expected or len(changes) != len(expected)*9 or len(transitions) != len(expected)*81:
        raise ValueError('Missing/extra comparison pairs, classes or transitions')
    coverage_suitability = []
    for before, after, threshold in sorted(expected):
        rows = [r for r in changes if (int(r['before_year']),int(r['after_year']),float(r['confidence_threshold'])) == (before,after,threshold)]
        trans = [r for r in transitions if (int(r['before_year']),int(r['after_year']),float(r['confidence_threshold'])) == (before,after,threshold)]
        if len(rows) != 9 or {int(r['class_code']) for r in rows} != set(range(9)):
            raise ValueError('Comparison class duplication')
        if len(trans) != 81 or {(int(r['from_code']),int(r['to_code'])) for r in trans} != {(a,b) for a in range(9) for b in range(9)}:
            raise ValueError('Transition duplication')
        common = number(rows[0], 'common_support_m2')
        if common < 0 or common > window_areas[0]:
            raise ValueError('Invalid common support')
        fraction = common / window_areas[0]
        coverage_suitability.append({'before_year': before, 'after_year': after,
            'confidence_threshold': threshold, 'common_support_m2': common,
            'window_fraction': fraction, 'minimum_window_fraction': 0.5,
            'gate_passed': fraction >= 0.5, 'primary': threshold == 0.6})
        for row in rows:
            close(number(row, 'common_support_m2'), common, 'Common support')
            close(common + number(row, 'excluded_window_m2'), window_areas[0], 'Excluded area')
            close(number(row, 'common_window_fraction'), fraction, 'Matched fraction', abs_tol=1e-9)
            if 'coverage_screen_pass' in row and str(row['coverage_screen_pass']).lower() not in ('1' if fraction >= 0.5 else '0', 'true' if fraction >= 0.5 else 'false'):
                raise ValueError('Exported coverage gate flag disagrees with fixed 50% rule')
            if number(row,'before_m2') < 0 or number(row,'after_m2') < 0 or number(row,'excluded_window_m2') < 0:
                raise ValueError('Negative matched or excluded area')
            close(number(row,'after_m2') - number(row,'before_m2'), number(row,'change_m2'), 'Change arithmetic')
            code = int(row['class_code'])
            close(sum(number(t,'area_m2') for t in trans if int(t['from_code']) == code), number(row,'before_m2'), 'Transition row margin')
            close(sum(number(t,'area_m2') for t in trans if int(t['to_code']) == code), number(row,'after_m2'), 'Transition column margin')
        if any(number(t,'area_m2') < 0 for t in trans):
            raise ValueError('Negative transition area')
        close(sum(number(t,'area_m2') for t in trans), common, 'Transition total')
        close(sum(number(r,'change_m2') for r in rows), 0, 'Net area conservation')
        for year, area_key in [(before,'before_m2'),(after,'after_m2')]:
            accepted = next(number(r,'accepted_area_m2') for r in coverage if int(r['year']) == year and float(r['confidence_threshold']) == threshold)
            if common > accepted + 0.1:
                raise ValueError('Matched support exceeds accepted whole-year area')
            close(sum(number(r,area_key) for r in rows), common, 'Matched class total')
    return {'status': 'integrity_passed_scientific_release_blocked', 'years': list(years),
            'thresholds': list(thresholds), 'comparison_keys': len(keys),
            'arithmetic_integrity': 'passed',
            'provenance_grid_metadata': 'passed; source assets not independently fetched',
            'canonical_sources': canonical_sources,
            'scene_counts': {str(y): sum(int(r['year']) == y for r in provenance) for y in years},
            'row_counts': {k: len(v) for k,v in tables.items()},
            'model_versions': sorted({r['dynamicworld_algorithm_version'] for r in provenance}),
            'qa_versions': sorted({r['qa_algorithm_version'] for r in provenance}),
            'coverage_suitability': coverage_suitability,
            'primary_coverage_gate_passed': all(r['gate_passed'] for r in coverage_suitability if r['primary']),
            'publication_ready': False,
            'publication_blockers': ['Independent dated-imagery classification review pending',
                'Raster/source checks must be completed'] + ([] if all(r['gate_passed'] for r in coverage_suitability if r['primary']) else ['Primary 0.60 common support fails unchanged provisional 50% coverage gate']),
            'area_convention': 'Unmodified Earth Engine pixelArea/reduceRegion CSV m2; not projected pixel count times 100',
            'raster_grid_and_probabilities': 'not checked by table validator',
            'manual_imagery_validation': 'pending; arithmetic alone does not establish accuracy'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exports', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    tables = {}
    for name in ['coverage','whole_window_areas','matched_changes','transitions','provenance']:
        with (args.exports / f'AlKhor_DW_{name}.csv').open(newline='') as handle:
            tables[name] = list(csv.DictReader(handle))
    try:
        report = validate(tables)
    except (ValueError, KeyError, StopIteration) as error:
        args.output.write_text(json.dumps({'status':'integrity_failed', 'publication_ready':False,
            'error':str(error)}, indent=2) + '\n')
        raise SystemExit(str(error))
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
