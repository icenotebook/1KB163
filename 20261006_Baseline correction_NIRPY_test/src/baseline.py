"""Workshop helpers; algorithm implementations are supplied by pybaselines/PyWavelets."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
import pywt
from pybaselines import Baseline


def validate_spectrum(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 3:
        raise ValueError('Expected equal-length 1D axis/intensity arrays with at least 3 points.')
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError('Spectrum contains missing or nonfinite values; inspect before processing.')
    steps = np.diff(x)
    if not (steps > 0).all():
        raise ValueError('Axis must be strictly increasing; inspect ordering and duplicates.')
    if not np.allclose(steps, np.median(steps), rtol=0.01, atol=1e-8):
        raise ValueError('These methods assume approximately uniform sampling. Inspect/resample explicitly.')
    return x, y


def read_rruff(path):
    metadata, pairs = [], []
    for line_number, line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith('##END='):
            break
        if line.startswith('##'):
            metadata.append(line)
            continue
        try:
            fields = line.split(',')
            if len(fields) != 2:
                raise ValueError('Expected two comma-separated values')
            pairs.append((float(fields[0]), float(fields[1])))
        except ValueError as error:
            raise ValueError(f'Unexpected RRUFF data on line {line_number}: {line}') from error
    if not pairs:
        raise ValueError('No numeric spectrum in RRUFF file.')
    x, y = validate_spectrum(*np.asarray(pairs).T)
    return x, y, {'header_lines': metadata}


def read_xrf(path):
    table = pd.read_excel(path, sheet_name='spectra data', usecols='A:C', skiprows=1, header=None)
    offset = float(table.iloc[2, 2])
    increment = float(table.iloc[3, 2])
    signal = pd.to_numeric(table.iloc[20:, 2], errors='raise')
    # Only blank trailing spreadsheet rows are excluded; internal missing values are rejected.
    last = signal.last_valid_index()
    if last is None:
        raise ValueError('XRF count column is empty.')
    y = signal.loc[:last].to_numpy(dtype=float)
    x = offset + increment * np.arange(y.size)
    x, y = validate_spectrum(x, y)
    return x, y, {'sheet': 'spectra data', 'usecols': 'A:C', 'skiprows': 1,
                  'column_position': 2, 'offset_row': 2, 'increment_row': 3,
                  'count_start_row': 20, 'offset_keV': offset, 'increment_keV': increment,
                  'calibration_requires_source_confirmation': True}


def synthetic_spectrum(seed=163):
    x = np.linspace(0, 1000, 2048)
    true_baseline = 15 + 0.012 * x + 14 * np.exp(-x / 300)
    peaks = sum(height * np.exp(-0.5 * ((x - centre) / width) ** 2)
                for centre, width, height in [(220, 12, 90), (510, 22, 65), (780, 15, 80)])
    noise = np.random.default_rng(seed).normal(0, 0.8, len(x))
    return x, true_baseline + peaks + noise, true_baseline, peaks


def wavelet_baseline(y, wavelet='db6', level=7):
    y = np.asarray(y, dtype=float)
    maximum = pywt.dwt_max_level(len(y), pywt.Wavelet(wavelet).dec_len)
    if not isinstance(level, int) or not 1 <= level <= maximum:
        raise ValueError(f'Wavelet level must be an integer in 1..{maximum} for this spectrum.')
    coefficients = pywt.wavedec(y, wavelet, level=level, mode='symmetric')
    # Reconstruct only the coarsest approximation; subtracting this equals zeroing it.
    baseline_coefficients = [coefficients[0]] + [np.zeros_like(c) for c in coefficients[1:]]
    baseline = pywt.waverec(baseline_coefficients, wavelet, mode='symmetric')[:len(y)]
    return baseline, {'level': level, 'wavelet': wavelet, 'extension_mode': 'symmetric',
                      'maximum_level': maximum}


def estimate_baseline(y, method, *, lam=1e6, p=0.1, max_iter=50, tol=1e-3,
                      wavelet='db6', level=7):
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or len(y) < 3 or not np.isfinite(y).all():
        raise ValueError('Expected a finite 1D spectrum with at least 3 points.')
    if method == 'Wavelet':
        return wavelet_baseline(y, wavelet, level)
    if not np.isfinite(lam) or lam <= 0 or max_iter < 1 or tol <= 0:
        raise ValueError('lambda, max_iter and tolerance must be positive.')
    fitter = Baseline()
    if method == 'AsLS':
        if not 0 < p < 0.5:
            raise ValueError('This positive-peak workshop uses 0 < p < 0.5.')
        baseline, info = fitter.asls(y, lam=lam, p=p, max_iter=max_iter, tol=tol)
    elif method == 'arPLS':
        baseline, info = fitter.arpls(y, lam=lam, max_iter=max_iter, tol=tol)
    else:
        raise ValueError(f'Unknown method: {method}')
    history = np.asarray(info['tol_history'])
    return baseline, {'lam': lam, 'p': p if method == 'AsLS' else None,
                      'max_iter': max_iter, 'tol': tol, 'tolerance_history': history.tolist(),
                      'iterations_reported': len(history),
                      'converged': bool(len(history) and history[-1] <= tol)}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
