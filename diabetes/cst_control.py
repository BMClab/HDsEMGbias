"""Reference points for the CST result: cutoff sensitivity, and an unrestricted
random 10-MU sample (no eligibility filter) as a control for sample size.

Run from the repository root:

    python diabetes/cst_control.py
"""

import pathlib

import numpy as np
import pandas as pd
from scipy import stats, signal

# Reuse the constants and helpers from cst_analysis.py without triggering its
# own analysis, by executing only the preamble above its first section marker.
_PREAMBLE = (
    (pathlib.Path(__file__).resolve().parent / "cst_analysis.py")
    .read_text()
    .split("# ---------------------------------------------------------------- load once")[0]
)
exec(_PREAMBLE)

print("loading ...", flush=True)
subjects = {}
for trial in TRIALS:
    for condition in CONDITIONS:
        subjects[(condition, int(trial))] = load_subject(condition, trial)


def draw(seed, restrict):
    """restrict=True -> eligible pool (HD-sEMG-like); False -> any active MU."""
    rng = np.random.default_rng(seed)
    out = {}
    for trial in TRIALS:
        for condition in CONDITIONS:
            _, fr, cv, _ = subjects[(condition, int(trial))]
            pool = eligible_index(fr, cv) if restrict else np.where(fr >= 0.01)[0]
            out[(condition, int(trial))] = rng.choice(pool, size=N_SELECT, replace=False)
    return out


N_CTRL = 100
sel_elig = {s: draw(s, True) for s in np.arange(20261000, 20261000 + N_CTRL)}
sel_rand = {s: draw(s, False) for s in np.arange(20263000, 20263000 + N_CTRL)}

rows = []
for cutoff in (1.0, 2.0, 5.0):
    sos = signal.butter(4, cutoff / (FS / 2), btype="low", output="sos")
    acc = {(k, c): np.zeros((N_CTRL, len(TRIALS)))
           for k in ("eligible", "unrestricted") for c in CONDITIONS}

    for trial in TRIALS:
        for condition in CONDITIONS:
            _, fr, _, binned = subjects[(condition, int(trial))]
            filt = signal.sosfiltfilt(sos, binned, axis=1)[:, TRIM:-TRIM] * FS
            cst_all = filt[fr >= 0.01].mean(axis=0)
            for k, sels in (("eligible", sel_elig), ("unrestricted", sel_rand)):
                for j, seed in enumerate(sels):
                    sel = sels[seed][(condition, int(trial))]
                    acc[(k, condition)][j, trial] = stats.pearsonr(
                        filt[sel].mean(axis=0), cst_all)[0]

    for k in ("eligible", "unrestricted"):
        n = acc[(k, "normal")].mean(axis=1)
        d = acc[(k, "DPN")].mean(axis=1)
        diff = d - n
        rows.append(dict(cutoff_hz=cutoff, sample=k,
                         normal_r=np.median(n), dpn_r=np.median(d),
                         diff=np.median(diff),
                         lo=np.percentile(diff, 2.5), hi=np.percentile(diff, 97.5),
                         frac_negative=np.mean(diff < 0)))
        print(f"cutoff {cutoff:>3.0f} Hz  {k:<13s}  "
              f"Normal r={rows[-1]['normal_r']:.3f}  DPN r={rows[-1]['dpn_r']:.3f}  "
              f"diff={rows[-1]['diff']:+.3f} [{rows[-1]['lo']:+.3f},{rows[-1]['hi']:+.3f}]",
              flush=True)

pd.DataFrame(rows).to_csv(
    "diabetes/csv_results/cst_control_v2.csv", index=False)
