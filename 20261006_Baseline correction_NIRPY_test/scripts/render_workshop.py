"""Execute from a fresh Python kernel and export a self-contained HTML review."""
from pathlib import Path
import os
import sys
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec

root = Path(__file__).resolve().parents[1]
# Local runtime/config/cache paths make execution independent of user Jupyter settings.
runtime = root / '.venv' / 'workshop-runtime'
runtime.mkdir(parents=True, exist_ok=True)
os.environ['JUPYTER_RUNTIME_DIR'] = str(runtime)
os.environ['IPYTHONDIR'] = str(runtime / 'ipython')
os.environ['MPLCONFIGDIR'] = str(runtime / 'matplotlib')
os.environ.setdefault('MPLBACKEND', 'Agg')
source = root / 'notebooks' / 'baseline_workshop.ipynb'
nb = nbformat.read(source, as_version=4)
nbformat.validate(nb)
manager = KernelManager(kernel_name='python3')
manager._kernel_spec = KernelSpec(argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                                  display_name='Workshop environment', language='python')
client = NotebookClient(nb, timeout=180, km=manager, resources={'metadata': {'path': str(root)}})
client.execute()
nbformat.validate(nb)
out = root / 'outputs'
out.mkdir(exist_ok=True)
nbformat.write(nb, out / 'baseline_workshop_executed.ipynb')
html, _ = HTMLExporter(template_name='lab').from_notebook_node(nb)
(out / 'baseline_workshop.html').write_text(html, encoding='utf-8')
errors = [o for cell in nb.cells if cell.cell_type == 'code' for o in cell.outputs if o.output_type == 'error']
print(f'Executed {sum(c.cell_type == "code" for c in nb.cells)} code cells; {len(errors)} cell errors.')
print(f'HTML preview: {out / "baseline_workshop.html"}')
