"""Run notebook cells through IPython without starting a Jupyter kernel."""
from pathlib import Path
from io import BytesIO
import base64
import json
import os
import sys

root = Path(__file__).resolve().parents[1]
cache = root / '.venv' / 'validation-cache'
cache.mkdir(parents=True, exist_ok=True)
os.environ['IPYTHONDIR'] = str(cache / 'ipython')
os.environ['MPLCONFIGDIR'] = str(cache / 'matplotlib')
os.environ['MPLBACKEND'] = 'Agg'
os.chdir(root)

import nbformat
from nbconvert import HTMLExporter
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import matplotlib.pyplot as plt

shell = InteractiveShell.instance()
notebook = nbformat.read(root / 'notebooks' / 'baseline_workshop.ipynb', as_version=4)
nbformat.validate(notebook)
figure_outputs = []
def capture_show(*args, **kwargs):
    for number in plt.get_fignums():
        stream = BytesIO()
        plt.figure(number).savefig(stream, format='png', dpi=120, bbox_inches='tight')
        figure_outputs.append(nbformat.v4.new_output(
            'display_data', data={'image/png': base64.b64encode(stream.getvalue()).decode('ascii')}, metadata={}))
plt.show = capture_show

count = 0
for cell in notebook.cells:
    if cell.cell_type != 'code':
        continue
    count += 1
    figure_outputs.clear()
    with capture_output(stdout=True, stderr=True, display=True) as captured:
        result = shell.run_cell(cell.source, store_history=False)
    if result.error_before_exec or result.error_in_exec:
        print(captured.stdout)
        print(captured.stderr)
        raise RuntimeError(f'Notebook code cell {count} failed') from (result.error_before_exec or result.error_in_exec)
    cell.execution_count = count
    cell.outputs = []
    if captured.stdout:
        cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
    if captured.stderr:
        cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
    for output in captured.outputs:
        cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
    cell.outputs.extend(figure_outputs)
    print(f'Validated code cell {count}')

nbformat.validate(notebook)
notebook.metadata['validation_method'] = 'Fresh Python process, IPython InteractiveShell; no Jupyter kernel was started.'
outputs = root / 'outputs'
nbformat.write(notebook, outputs / 'baseline_workshop_executed.ipynb')
html, _ = HTMLExporter(template_name='lab').from_notebook_node(notebook)
(outputs / 'baseline_workshop.html').write_text(html, encoding='utf-8')

print('Rendered HTML:', outputs / 'baseline_workshop.html')
