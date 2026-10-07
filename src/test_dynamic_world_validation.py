"""Synthetic arithmetic tests only; no Earth Engine imagery or access is implied."""
import copy
import unittest
from validate_dynamic_world import validate


def fixture():
    tables = {k: [] for k in ['coverage','whole_window_areas','matched_changes','transitions','provenance']}
    for year in [2021,2026]:
        for i in range(3):
            tables['provenance'].append({'year':year,'asset_id':f'GOOGLE/DYNAMICWORLD/V1/{year}09{i+1:02}T080000_{year}09{i+1:02}T080000_T39RWJ',
                'acquired_utc':f'{year}-09-{i+1:02} 08:00:00','dynamicworld_algorithm_version':'test-only',
                'qa_algorithm_version':'test-only','crs':'EPSG:32639','grid_transform':'10,0,544635,0,-10,2845905'})
        for t in [0.5,0.6,0.7]:
            # Different unknown coverage must not be counted as a land transition.
            valid = 900 if year == 2021 else 800
            tables['coverage'].append({'year':year,'confidence_threshold':t,'window_area_m2':1000,
                'observed_area_m2':1000,'accepted_area_m2':valid,'unknown_area_m2':1000-valid,
                'accepted_fraction':valid/1000,'minimum_observations':3})
            for c in [*range(9),255]:
                tables['whole_window_areas'].append({'year':year,'confidence_threshold':t,'class_code':c,
                    'area_m2':1000-valid if c == 255 else valid if c == 7 else 0})
    for t in [0.5,0.6,0.7]:
        for c in range(9):
            tables['matched_changes'].append({'before_year':2021,'after_year':2026,'confidence_threshold':t,
                'class_code':c,'common_support_m2':700,'excluded_window_m2':300,'common_window_fraction':0.7,
                'before_m2':700 if c == 7 else 0,'after_m2':700 if c == 7 else 0,'change_m2':0})
            for d in range(9):
                tables['transitions'].append({'before_year':2021,'after_year':2026,'confidence_threshold':t,
                    'from_code':c,'to_code':d,'area_m2':700 if c == d == 7 else 0})
    return tables


class HistoricalArithmeticTests(unittest.TestCase):
    def test_fraction_checks_do_not_inherit_square_metre_tolerance(self):
        t=fixture();t['coverage'][0]['accepted_fraction']+=.01
        with self.assertRaises(ValueError):validate(t)
        t=fixture();t['matched_changes'][0]['common_window_fraction']+=.01
        with self.assertRaises(ValueError):validate(t)

    def test_duplicate_sources_or_arbitrary_thresholds_rejected(self):
        t=fixture();t['provenance'].append(copy.deepcopy(t['provenance'][0]))
        with self.assertRaises(ValueError):validate(t)
        with self.assertRaises(ValueError):validate(fixture(),thresholds=(.4,.5,.6))

    def test_real_index_provenance_is_explicitly_derived_not_independently_fetched(self):
        t=fixture()
        for r in t['provenance']:
            r['dataset']='GOOGLE/DYNAMICWORLD/V1';r['asset_id']=r['asset_id'].split('/')[-1]
        original=copy.deepcopy(t)
        report=validate(t)
        self.assertEqual(t,original)
        self.assertTrue(all(r['identifier_origin'].startswith('derived') and not r['independently_fetched'] for r in report['canonical_sources']))
        t['provenance'][0]['dataset']='untrusted'
        with self.assertRaises(ValueError):validate(t)

    def test_coverage_failure_is_reported_without_rejecting_valid_arithmetic(self):
        t=fixture()
        for r in t['matched_changes']:
            r.update(common_support_m2=300,excluded_window_m2=700,common_window_fraction=.3,
                before_m2=300 if r['class_code']==7 else 0,after_m2=300 if r['class_code']==7 else 0)
        for r in t['transitions']:r['area_m2']=300 if r['from_code']==r['to_code']==7 else 0
        report=validate(t)
        self.assertEqual(report['arithmetic_integrity'],'passed')
        self.assertFalse(report['primary_coverage_gate_passed'])
        self.assertFalse(report['publication_ready'])
        self.assertTrue(all(r['minimum_window_fraction']==.5 and not r['gate_passed'] for r in report['coverage_suitability']))

    def test_false_export_gate_flag_is_integrity_failure(self):
        t=fixture();t['matched_changes'][0]['coverage_screen_pass']='0'
        with self.assertRaises(ValueError):validate(t)

    def test_different_missing_coverage_is_not_change_or_publication_approval(self):
        report = validate(fixture())
        self.assertFalse(report['publication_ready'])
        self.assertEqual(report['comparison_keys'],3)

    def test_unknown_cannot_disappear(self):
        t=fixture();t['whole_window_areas'][9]['area_m2']=0
        with self.assertRaises(ValueError):validate(t)

    def test_transition_margins_must_reconcile(self):
        t=fixture();t['transitions'][0]['area_m2']=100
        with self.assertRaises(ValueError):validate(t)

    def test_unsupported_year_or_wrong_grid_rejected(self):
        t=fixture();t['provenance'][0]['grid_transform']='wrong'
        with self.assertRaises(ValueError):validate(t)
        with self.assertRaises(ValueError):validate(fixture(),years=(2021,2023,2026))

    def test_reject_nonfinite_and_negative_values(self):
        t=fixture();t['coverage'][0]['unknown_area_m2']=float('nan')
        with self.assertRaises(ValueError):validate(t)
        t=fixture();t['coverage'][0]['accepted_area_m2']=-1
        with self.assertRaises(ValueError):validate(t)


if __name__ == '__main__':
    unittest.main()
