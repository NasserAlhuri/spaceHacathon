"""Execute the packaged notebook through an ordinary Jupyter kernel."""
from pathlib import Path
import hashlib
import json
import os
import platform
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
inputs = ROOT / 'data/sample_input'
hashes = json.loads((inputs / 'SHA256.json').read_text())
for relative_path, expected in hashes.items():
    actual = hashlib.sha256((inputs / relative_path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f'Sample input hash mismatch: {relative_path}')

nb = nbformat.read(ROOT / 'pilot.ipynb', as_version=4)
start = time.monotonic()
client = NotebookClient(
    nb, timeout=180, kernel_name='python3',
    resources={'metadata': {'path': str(ROOT)}},
)
client.execute()
elapsed = time.monotonic() - start
code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
report = {
    'status': 'passed_normal_jupyter_kernel',
    'runtime_seconds': round(elapsed, 1),
    'executed_code_cells': len(code_cells),
    'errors': sum(output.output_type == 'error' for cell in code_cells for output in cell.outputs),
    'sample_hashes_verified': len(hashes),
    'python_version': platform.python_version(),
    'system': platform.system(),
    'environment': 'GitHub-hosted runner' if os.environ.get('GITHUB_ACTIONS') == 'true' else 'Local Jupyter-capable machine',
    'separate_execution_environment': os.environ.get('GITHUB_ACTIONS') == 'true',
    'review_note': 'Kernel execution verifies reproducibility, not independent scientific accuracy.',
}
if os.environ.get('GITHUB_ACTIONS') == 'true':
    report['source_commit'] = os.environ['GITHUB_SHA']
    report['workflow_run_url'] = (
        f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    )
nb.metadata['verification'] = report
nbformat.write(nb, ROOT / 'pilot.ipynb')
(ROOT / 'results/notebook-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
