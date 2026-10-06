"""Compare freshly generated CSV tables with the preserved original SHA256 hashes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
expected = json.loads((ROOT / 'metadata/original-results-sha256.json').read_text())
assert len(expected) == 7, 'Expected exactly seven original result tables'
checks = {}
for relative_path, original_sha256 in expected.items():
    actual = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
    checks[relative_path] = {'sha256': actual, 'matches_original': actual == original_sha256}
report = {'status': 'passed' if all(x['matches_original'] for x in checks.values()) else 'failed',
          'original_csv_tables_identical': sum(x['matches_original'] for x in checks.values()),
          'comparison': 'Byte-for-byte SHA256 comparison against preserved original tables',
          'tables': checks}
(ROOT / 'results/original-results-comparison.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if report['status'] != 'passed':
    raise SystemExit('Regenerated result tables differ from the original baseline')
