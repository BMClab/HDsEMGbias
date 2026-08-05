"""CST representativeness: r(CST_selected_10, CST_all_active) at 20% MVC.

Replicates the eligibility rule, selection RNG and steady-state definitions used
in diabetes/analysis_v2.py so the result is comparable with the published
firing-rate outcomes. Run from the repository root:

    python diabetes/cst_analysis.py
"""

import numpy as np
import pandas as pd
from scipy import stats, signal

PATH = "diabetes/results/"
BATCH = "variability"
CONDITIONS = ["normal", "DPN"]
TRIALS = np.arange(50)
T_START, T_END, FORCE_LEVEL = 4000, 10000, 20
FMIN, FMAX, ISICV, N_SELECT = 5, 15, 0.3, 10
PRIMARY_SEED = 20260102
STABILITY_SEEDS = np.arange(20261000, 20262000)
BOOTSTRAP_SEED = 20260115
N_RESAMPLES = 100_000

FS = 1000.0          # CST bin rate (Hz)
CUTOFF = 2.0         # low-pass cutoff (Hz)
TRIM = 500           # samples dropped at each end for filter transients

SOS = signal.butter(4, CUTOFF / (FS / 2), btype="low", output="sos")


def compute_mn_cv(spike_times, t_start):
    isi = np.diff(spike_times[spike_times > t_start])
    if len(isi) > 3:
        return isi.std(ddof=1) / isi.mean()
    return 1.0


def load_subject(condition, trial):
    """Return unit ids, firing rates, ISI-CoV and the 1 kHz binned spike matrix."""
    data = pd.read_csv(
        f"{PATH}spikedata_{condition}_{trial}_{BATCH}/cell_spike_ref_{FORCE_LEVEL}.csv",
        delimiter=",",
    ).values
    unit_ids = np.unique(data[:, 0])
    steady = data[(data[:, 1] >= T_START) & (data[:, 1] <= T_END)]

    n_bins = int((T_END - T_START) * FS / 1000)
    edges = np.linspace(T_START, T_END, n_bins + 1)
    firing_rate = np.zeros(len(unit_ids))
    isi_cov = np.zeros(len(unit_ids))
    binned = np.zeros((len(unit_ids), n_bins))

    window_s = (T_END - T_START) / 1000
    for i, unit in enumerate(unit_ids):
        times = steady[steady[:, 0] == unit, 1]
        firing_rate[i] = len(times) / window_s
        isi_cov[i] = compute_mn_cv(times, t_start=T_START)
        binned[i], _ = np.histogram(times, bins=edges)

    return unit_ids.astype(int), firing_rate, isi_cov, binned


def eligible_index(firing_rate, isi_cov):
    return np.where(
        (firing_rate >= 0.01)
        & (firing_rate > FMIN)
        & (firing_rate < FMAX)
        & (isi_cov <= ISICV)
    )[0]


# ---------------------------------------------------------------- load once
print("loading 100 subject-conditions ...", flush=True)
subjects = {}
for trial in TRIALS:
    for condition in CONDITIONS:
        subjects[(condition, int(trial))] = load_subject(condition, trial)

active_counts = {
    c: np.mean([(subjects[(c, t)][1] >= 0.01).sum() for t in TRIALS]) for c in CONDITIONS
}
print(f"mean active MUs  Normal {active_counts['normal']:.1f}   "
      f"DPN {active_counts['DPN']:.1f}   (paper: 174.5 / 161.8)")


# ------------------------------------------------- replicate the selections
def draw_selections(seed):
    """Shared-RNG draw over the trial x condition loop, as in analysis_v2.py."""
    rng = np.random.default_rng(seed)
    out = {}
    for trial in TRIALS:
        for condition in CONDITIONS:
            _, fr, cv, _ = subjects[(condition, int(trial))]
            out[(condition, int(trial))] = rng.choice(
                eligible_index(fr, cv), size=N_SELECT, replace=False
            )
    return out


primary = draw_selections(PRIMARY_SEED)

published = pd.read_csv("diabetes/csv_results/hdsemg_selected_motor_units_v2.csv")
mismatch = 0
for _, row in published.iterrows():
    ids, _, _, _ = subjects[(row["condition"], int(row["simulation_id"]))]
    mine = sorted(ids[primary[(row["condition"], int(row["simulation_id"]))]])
    theirs = sorted(int(x) for x in row["selected_motor_unit_ids"].split(";"))
    mismatch += mine != theirs
print(f"fixed-seed selection matches published IDs: "
      f"{len(published) - mismatch}/{len(published)} rows")


# --------------------------------------------------- filtered CSTs and r
print("computing correlations ...", flush=True)
all_selections = {s: draw_selections(s) for s in STABILITY_SEEDS}

r_primary = {c: np.zeros(len(TRIALS)) for c in CONDITIONS}
r_seeds = {c: np.zeros((len(STABILITY_SEEDS), len(TRIALS))) for c in CONDITIONS}

for trial in TRIALS:
    for condition in CONDITIONS:
        _, fr, _, binned = subjects[(condition, int(trial))]
        # Filtering is linear, so filter each unit once and average afterwards.
        filtered = signal.sosfiltfilt(SOS, binned, axis=1)[:, TRIM:-TRIM] * FS
        cst_all = filtered[fr >= 0.01].mean(axis=0)

        sel = primary[(condition, int(trial))]
        r_primary[condition][trial] = stats.pearsonr(
            filtered[sel].mean(axis=0), cst_all
        )[0]

        for k, seed in enumerate(STABILITY_SEEDS):
            sel = all_selections[seed][(condition, int(trial))]
            r_seeds[condition][k, trial] = stats.pearsonr(
                filtered[sel].mean(axis=0), cst_all
            )[0]


# ------------------------------------------------------------------ stats
def paired_report(first, second, label):
    difference = second - first
    boot = stats.bootstrap(
        (first, second),
        lambda a, b, axis=-1: np.mean(b, axis=axis) - np.mean(a, axis=axis),
        paired=True,
        n_resamples=N_RESAMPLES,
        confidence_level=0.95,
        method="BCa",
        vectorized=True,
        rng=np.random.default_rng(BOOTSTRAP_SEED + 2),
    )
    w, p = stats.wilcoxon(first, second)
    print(f"\n{label}")
    print(f"  Normal  r = {first.mean():.3f} +/- {first.std(ddof=1):.3f}")
    print(f"  DPN     r = {second.mean():.3f} +/- {second.std(ddof=1):.3f}")
    print(f"  paired difference (DPN - Normal) = {difference.mean():+.3f}  "
          f"95% BCa CI [{boot.confidence_interval.low:+.3f}, "
          f"{boot.confidence_interval.high:+.3f}]")
    print(f"  Wilcoxon W = {w:.1f}, p = {p:.3g}")
    return difference.mean()


paired_report(r_primary["normal"], r_primary["DPN"],
              f"Fixed primary seed ({PRIMARY_SEED}), 20% MVC")

per_seed_diff = r_seeds["DPN"].mean(axis=1) - r_seeds["normal"].mean(axis=1)
lo, hi = np.percentile(per_seed_diff, [2.5, 97.5])
print(f"\nAcross {len(STABILITY_SEEDS)} selection seeds")
print(f"  Normal  r: median {np.median(r_seeds['normal'].mean(axis=1)):.3f}")
print(f"  DPN     r: median {np.median(r_seeds['DPN'].mean(axis=1)):.3f}")
print(f"  paired difference: median {np.median(per_seed_diff):+.3f}, "
      f"central 95% [{lo:+.3f}, {hi:+.3f}]")
print(f"  fraction of seeds with difference < 0: "
      f"{np.mean(per_seed_diff < 0):.3f}")

out = pd.DataFrame({
    "simulation_id": np.tile(TRIALS, 2),
    "condition": np.repeat(CONDITIONS, len(TRIALS)),
    "r_cst_selected_vs_all_active": np.concatenate(
        [r_primary["normal"], r_primary["DPN"]]
    ),
})
dest = "diabetes/csv_results/cst_representativeness_v2.csv"
out.to_csv(dest, index=False)
print(f"\nper-subject values written to {dest}")
