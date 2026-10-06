# Baseline correction workshop — 1KB163

An editable pilot workshop based on Daniel Pelliccia's [NIRPY tutorial](https://nirpyresearch.com/two-methods-baseline-correction-spectral-data/), prepared 6 October 2026.

Start with **notebooks/baseline_workshop.ipynb** in VS Code. Use **outputs/baseline_workshop.html** to review the executed workshop without Python.

## Set up in VS Code (Windows)

1. Install Microsoft's **Python** and **Jupyter** extensions. Open this whole project folder with **File > Open Folder**.
2. In the VS Code PowerShell terminal, create a local environment using Python 3.12 (the tested version):

```powershell
# First-time setup
py -3.12 -m venv .venv

# Install the packages listed in requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Open the notebook. Choose **Select Kernel > Python Environments > .venv**. If it is missing, choose **Select Another Kernel** and browse to `.venv\Scripts\python.exe`.
4. Read the data-status table, run cells from top to bottom, and edit the marked parameter cell. The synthetic spectrum always runs. Raman and XRF run when their exact source files are present in `data/raw/`; see `data/README.md`.
5. Before sharing, **Restart Kernel > Run All**, then save. Preserve your exported run in a named output directory; the export cell overwrites files with the same run label.

No environment activation or PowerShell execution-policy change is necessary. The virtual environment stays local and is not shared.

## Project contents

| File/folder | Purpose |
| --- | --- |
| `notebooks/baseline_workshop.ipynb` | Teaching narrative, executable steps, plots, discussion prompts |
| `src/baseline.py` | Data loaders and wrappers for wavelet, AsLS, arPLS |
| `data/raw/` | Source files, unchanged; missing data never silently substituted |
| `data/README.md` | Source metadata, expected filenames and import assumptions |
| `data/download_manifest.json` | Successful downloads, retrieval times and SHA-256 hashes |
| `outputs/` | HTML preview, comparison figures, processed CSVs and run metadata |
| `requirements.txt` | Direct package versions used for validation |
| `requirements-lock.txt` | Full tested Windows/Python 3.12 environment snapshot |
| `scripts/render_workshop.py` | Execute a fresh notebook and export HTML |
| `TEACHING_NOTES.md` | Learning outcomes, teaching suggestions and pilot checklist |
| `CHANGELOG.md` | Workshop milestones and differences from the article |

To execute and export without opening VS Code:

```powershell
.\.venv\Scripts\python.exe scripts\render_workshop.py
```

The renderer uses this interpreter as the kernel, starts a fresh process, and writes the executed notebook plus an HTML preview. It needs no global kernel registration. Jupyter kernel startup was blocked by a Windows permission operation in the validation sandbox. The calculations and exports were instead validated with the following headless alternative, which runs the same cells in order through IPython without starting a kernel:

```powershell
.\.venv\Scripts\python.exe scripts\render_workshop_headless.py
```

Both renderers write the same output paths. See `VALIDATION.md` for tested coverage and missing source data.

## Tracking edits and sharing

The parent `C:\Git_repo\1KB163` is already a Git repository. Keep this workshop as a subfolder rather than creating a nested repository. From the parent repository, review and stage only this workshop:

```powershell
git status --short
git add -- "20261006_Baseline correction_NIRPY_test"
git diff --cached --stat
git commit -m "Add baseline correction workshop pilot"
```

Use small commits for meaningful changes. Clear notebook outputs before committing routine code changes if the plots make the diff hard to read; regenerate the HTML preview for review. Include small raw data files with their metadata when redistribution terms permit. Keep `.venv`, caches and generated outputs excluded from Git. For a course-platform ZIP, include the project source and the HTML preview, exclude `.venv` and caches. Do not place an instructor solution in a student distribution.

## Relation to the tutorial

This is an adaptation, not an exact numerical reproduction. It retains the wavelet/AsLS/arPLS comparison and tutorial starting settings (`db6`, level 7, lambda 1e6, AsLS p=0.1). It uses `pybaselines` instead of copying the article's LGPL appendix. Its API uses `max_iter`, and the workshop allows convergence with a tolerance check rather than fixing all runs to five iterations. The original article's calls use `niter` although its appended functions take `itermax`.

The wavelet reconstruction is cropped to the input length, and excessive decomposition levels are rejected with a clear error. A known-baseline synthetic spectrum adds quantitative evaluation; it is labelled as synthetic throughout. Real spectra have no known true baseline. No data download occurs during notebook execution.

## References

- Pelliccia, D. (2024), [Two methods for baseline correction of spectral data](https://nirpyresearch.com/two-methods-baseline-correction-spectral-data/).
- [pybaselines AsLS API](https://pybaselines.readthedocs.io/en/stable/generated/api/pybaselines.Baseline.asls.html) and [arPLS API](https://pybaselines.readthedocs.io/en/stable/generated/api/pybaselines.Baseline.arpls.html). AsLS: Eilers and Boelens (2005). arPLS: Baek et al. (2015), *Analyst*, 140, 250–257.
- [PyWavelets](https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html).
- Real-data attribution and access status: `data/README.md`.
