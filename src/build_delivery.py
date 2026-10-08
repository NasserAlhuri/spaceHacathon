"""Assemble existing, manifest-checked delivery files without running analysis."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import fitz
from pptx import Presentation


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(root, output, source_commit):
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Supply the full verified published commit SHA')
    output = output.resolve()
    if output == root or root in output.parents:
        raise ValueError('Delivery output must be outside the project directory')
    manifest = json.loads((root / 'PACKAGE-SHA256.json').read_text())
    for name, expected in manifest.items():
        path = (root / name).resolve()
        if root not in path.parents or digest(path.read_bytes()) != expected:
            raise ValueError(f'Manifest mismatch or unsafe path: {name}')
    inputs = json.loads((root / 'data/sample_input/SHA256.json').read_text())
    results = json.loads((root / 'metadata/original-results-sha256.json').read_text())
    for name, expected in inputs.items():
        assert digest((root / 'data/sample_input' / name).read_bytes()) == expected, name
    for name, expected in results.items():
        assert digest((root / name).read_bytes()) == expected, name
    assert len(inputs) == 35 and len(results) == 7
    pdf = root / 'docs/UrbanHeat-AlKhor-Pitch.pdf'
    pptx = root / 'docs/UrbanHeat-AlKhor-Pitch.pptx'
    with fitz.open(pdf) as presentation:
        pages = len(presentation)
    slides = len(Presentation(pptx).slides)
    assert pages == slides == 12
    assert pdf.stat().st_size <= 50_000_000
    output.mkdir(parents=True, exist_ok=True)
    copies = ['docs/UrbanHeat-AlKhor-Pitch.pdf', 'docs/UrbanHeat-AlKhor-Pitch.pptx',
              'preview/UrbanHeat-AlKhor-Preview.html', 'docs/Three-Minute-Presentation.md',
              'docs/Judge-Questions.md', 'PROJECT_STATE.md']
    for name in copies:
        shutil.copyfile(root / name, output / Path(name).name)
    readme = output / 'DELIVERY-README.md'
    readme.write_text('# UrbanHeat Al Khor delivery\n\n'
                      'Review-ready; no hackathon submission has been performed.\n\n'
                      '- [Presentation PDF](UrbanHeat-AlKhor-Pitch.pdf)\n'
                      '- [Editable PowerPoint](UrbanHeat-AlKhor-Pitch.pptx)\n'
                      '- [Full project ZIP](UrbanHeat-AlKhor-Project.zip)\n'
                      '- [Standalone map](UrbanHeat-AlKhor-Preview.html): open with Chrome or Edge.\n'
                      '- [Three-minute English script](Three-Minute-Presentation.md)\n'
                      '- [Judge questions](Judge-Questions.md)\n'
                      '- [Project state](PROJECT_STATE.md)\n'
                      '- [Verification report](DELIVERY-VERIFICATION.json)\n'
                      '- [Checksums](SHA256SUMS.json)\n\n'
                      f'Published source: https://github.com/NasserAlhuri/spaceHacathon/tree/{source_commit}\n\n'
                      'Extract the ZIP for the full source, original inputs/results, complete app, '
                      'preview, licences and docs/Delivery-Guide.md. The standalone map embeds its '
                      'resources; external source and Street View links need internet.\n\n'
                      'Visits to the original three reviewed sites are confirmed. Added reports '
                      'have no separate visit confirmation. User counts, use times and detailed shade '
                      'assessment were not measured; photographs are pending and Unknown values remain. '
                      'Mohammed practises the presentation; Abdulrahman reviews the project and collects '
                      'photos/observations. Their tasks remain pending. Physical-device, teammate reviews '
                      'and rehearsal are pending. Chromium desktop/mobile-emulation checks are '
                      'technical evidence only. Separate final approval is required to submit.\n')
    dynamic_world = root / 'results/dynamic-world-export-status.json'
    if dynamic_world.exists():
        with readme.open('a') as handle:
            handle.write('\nActual Dynamic World Code Editor exports succeeded. The ZIP includes all eight '
                         'immutable original exports: five CSVs, two exact reassembled annual TIFFs '
                         'and the primary transition TIFF. Six supplied parts and both assembled '
                         'original hashes were verified. The original 137 MB external ZIP itself is '
                         'not included or independently archive-hash verified. Primary common '
                         'coverage is 30.94%, below the unchanged 50% gate. The two unique 2021 reference '
                         'RGB/QA TIFFs and provenance are included; the exact duplicate was ignored. '
                         'The assistant paired review of 18 targets/72 dated views is complete: eight '
                         'clear broad patterns, ten exact-class ambiguities and three overlapping '
                         'potential disagreement flags. Independent scientific review remains pending; '
                         'technical integrity and source-linked convenience views do not establish '
                         'classification accuracy, causes or citywide change totals. '
                         'Only a limited coverage experiment is shown. No general change result is '
                         'adopted. See docs/Dynamic-World-Paired-Reference-Review.md.\n')
    names = sorted([*manifest, 'PACKAGE-SHA256.json'])
    archive_path = output / 'UrbanHeat-AlKhor-Project.zip'
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            archive.write(root / name, 'UrbanHeat-AlKhor/' + name)
        archive.writestr('UrbanHeat-AlKhor/SOURCE-COMMIT.txt', source_commit + '\n')
    assert archive_path.stat().st_size <= 200_000_000
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {'UrbanHeat-AlKhor/' + n for n in [*names, 'SOURCE-COMMIT.txt']}
        for name in names:
            assert archive.read('UrbanHeat-AlKhor/' + name) == (root / name).read_bytes(), name
        assert archive.read('UrbanHeat-AlKhor/SOURCE-COMMIT.txt').decode().strip() == source_commit
    files = [output / Path(n).name for n in copies] + [archive_path, readme]
    checksums = {p.name: {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())} for p in files}
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'source_commit': source_commit, 'source_commit_remote_verified': False,
              'status': 'packaging_passed_remote_verification_required',
              'files': checksums, 'pdf_pages': pages, 'pptx_slides': slides,
              'manifest_files_verified': len(manifest), 'archive_entries': len(names) + 1,
              'zip_integrity': 'passed', 'zip_snapshot_matches_local_manifest': True,
              'original_input_hashes_verified': len(inputs), 'original_csv_hashes_verified': len(results),
              'analysis_rerun': False, 'pdf_limit_bytes': 50_000_000, 'zip_limit_bytes': 200_000_000,
              'member_reviews': 'pending until individually confirmed',
              'submission': 'not performed; separate final approval required'}
    improvement = root / 'results/improvement-revision-verification.json'
    if improvement.exists():
        report['previous_improvement_milestone'] = json.loads(improvement.read_text())
    if dynamic_world.exists():
        report['dynamic_world_current_status'] = json.loads(dynamic_world.read_text())
        with readme.open('a') as handle:
            handle.write('\nHistorical comparison status is recorded in '
                         'UrbanHeat-AlKhor/results/dynamic-world-export-status.json inside the ZIP. '
                         'It supersedes the retained earlier improvement milestone. Technical '
                         'export/raster checks do not establish scientifically validated change.\n')
        checksums[readme.name] = {'bytes': readme.stat().st_size, 'sha256': digest(readme.read_bytes())}
    (output / 'DELIVERY-VERIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'SHA256SUMS.json').write_text(json.dumps(checksums, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.project.resolve(), args.output, args.source_commit), indent=2))
