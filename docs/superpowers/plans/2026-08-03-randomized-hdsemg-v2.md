# Randomized HD-sEMG v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make seeded random selection of 10 eligible MUs the sole HD-sEMG sampling mode in the v2 notebook, compare it only with the known all-active-MU simulation truth, and synchronize the v2 manuscript, additional-force analyses, and threshold sensitivities.

**Architecture:** Keep the marimo notebook as the single analysis implementation. Consolidate eligibility plus random sampling in one selector, route the primary and additional-force analyses through it, and keep the full active-MU population as a non-sampled reference. Recompute v2-tagged artifacts before making revision-protected, source-grounded edits to the existing native Google Doc.

**Tech Stack:** Python 3, marimo 0.17.8, NumPy, pandas, SciPy, Matplotlib, pytest-style synthetic assertions, Google Docs API batch updates.

## Global Constraints

- Modify analysis logic only in `diabetes/analysis_v2.py`; do not edit `diabetes/analysis.py`.
- Modify only the native Google Doc `HDsEMG_rev_gdocs_v2`; treat `Response_to_Reviewers` and the original article as read-only sources.
- HD-sEMG eligibility remains exactly `5 < firing rate < 15 pps` and `ISI-CoV <= 0.3`.
- Select exactly 10 unique eligible MUs without replacement using an explicit seed; raise a contextual error if fewer than 10 are eligible.
- Use one per-simulation mean as the inferential unit; MU-level values remain descriptive only.
- The all-active-MU mean is the sole true reference and is not called a sampling mode.
- Apply the same HD-sEMG selection contract at 20%, 10%, and 50% MVC and throughout the threshold-sensitivity analysis.
- Retain the existing 10 paired subjects at 10% and 50% MVC; report these analyses as exploratory and do not claim force-level consistency when the across-seed evidence does not support it.
- Evaluate 1,000 fixed selection seeds at every force level and every threshold; distinguish across-seed selection ranges from bootstrap confidence intervals.
- Preserve the `print_statistics` API and unrelated user changes.
- Suffix every file written by the v2 notebook with `_v2` so verification cannot overwrite existing generated artifacts.
- Do not commit or push unless the user explicitly requests it.

---

### Task 1: Lock the random-within-eligibility selector contract

**Files:**
- Modify: `diabetes/analysis_v2.py:55-230`
- Test: `/tmp/test_analysis_v2_selection.py`

**Interfaces:**
- Consumes: spike array columns `[motor_unit_id, spike_time_ms]`, `criteria: dict[str, float]`, `mn_number: int`, and `rng: numpy.random.Generator`.
- Produces: `select_mns_hdemg(data, t_start, t_end, column_spikes=1, criteria=criteria, mn_number=mn_number, rng=None) -> numpy.ndarray` containing exactly `mn_number` unique integer IDs.

- [ ] **Step 1: Record the original-notebook baseline**

Run:

```bash
sha256sum diabetes/analysis.py
git status --short --branch
```

Save the hash in the working notes and use it again in Task 5.

- [ ] **Step 2: Write a failing synthetic selector test**

Create `/tmp/test_analysis_v2_selection.py` with an AST helper that loads the
nested `select_mns_hdemg` definition from the notebook and stubs `compute_fr`
and `compute_cv`. Assert all of the following:

```python
assert selected.size == 10
assert np.unique(selected).size == 10
assert set(selected) <= set(eligible_ids)
assert np.array_equal(selected, selected_again_with_same_seed)
assert not np.array_equal(selected, selected_with_different_seed)
with pytest.raises(ValueError, match="10.*eligible"):
    select_mns_hdemg(undersized_data, 4000, 10000, rng=np.random.default_rng(1))
```

- [ ] **Step 3: Run the test to verify the missing selector fails**

Run:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q /tmp/test_analysis_v2_selection.py
```

Expected: failure because `select_mns_hdemg` is not yet defined.

- [ ] **Step 4: Implement the consolidated selector**

Replace `select_mns_regular` and `select_mns_filtered_random` with one helper
whose selection tail is:

```python
eligible_ids = unique_neurons[selection_criteria].astype(int)
if eligible_ids.size < mn_number:
    raise ValueError(
        f"Cannot select {mn_number} HD-sEMG motor units from "
        f"{eligible_ids.size} eligible units."
    )
return rng.choice(eligible_ids, size=mn_number, replace=False)
```

Require `rng` and retain the current steady-state firing-rate and ISI-CoV
calculations. Preserve `select_mns_randomly` for the descriptive 100-MU
firing-rate/ISI-CoV scatter; it is not an inferential mode.

- [ ] **Step 5: Simplify seeds and mode dispatch**

Use these stable selection keys:

```python
selection_seeds = {
    "hdsemg": 20260102,
    "fr_cv": 20260103,
    "mvc10_hdsemg": 20260104,
    "mvc50_hdsemg": 20260105,
    "threshold_sensitivity": 20260116,
    "seed_stability_start": 20261000,
}
```

In `calculate_fr_data`, recognize `"hdsemg"` and `"all"` only for inferential
analysis. Construct the seeded generator for `"hdsemg"`; remove `"randomly"`,
`"regular"`, and `"filtered_random"` dispatch branches.

- [ ] **Step 6: Run the selector test to verify it passes**

Run the Task 1 pytest command. Expected: all assertions pass.

---

### Task 2: Reduce the primary analysis to HD-sEMG versus truth

**Files:**
- Modify: `diabetes/analysis_v2.py:475-1260`
- Test: `/tmp/test_analysis_v2_primary_source.py`

**Interfaces:**
- Consumes: `data_hdemg` and `data_truth` dictionaries returned by `calculate_fr_data`.
- Produces: a one-panel primary figure, simulation-level v2 CSVs, and a single-row HD-sEMG inferential summary.

- [ ] **Step 1: Write failing structural assertions**

Create a source-level test that asserts:

```python
source = Path("diabetes/analysis_v2.py").read_text()
assert 'modes = ["HD-sEMG"]' in source
assert "data_random" not in source
assert "Filtered-Random" not in source
assert "RANDOM MODE" not in source
assert "HD-sEMG vs filtered-random" not in source
```

Also assert the primary plot signature is exactly:

```python
def plot_mn_fr_combined_data(data_hdemg, data_truth, conditions, pd):
```

- [ ] **Step 2: Run the structural test and confirm failure**

Run:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q /tmp/test_analysis_v2_primary_source.py
```

Expected: failures identify current Random/Filtered-Random dependencies.

- [ ] **Step 3: Rewrite the primary plot and exports**

Use one `matplotlib` axis. Plot the 50 simulation-level HD-sEMG means for
Normal and DPN, one black mean/BCa interval per condition, and one red
simulation-truth mean line per condition. Export:

```text
diabetes/figures/mn_firing_rate_comparison_combined_v2.png
diabetes/csv_results/mn_firing_rate_normal_hdsemg_v2.csv
diabetes/csv_results/mn_firing_rate_DPN_hdsemg_v2.csv
diabetes/csv_results/mn_firing_rate_p_values_combined_v2.csv
```

The summary CSV must contain `hdsemg_selection_seed`, `bootstrap_seed`,
`n_resamples`, `n_simulations`, Wilcoxon statistic/p-value, paired mean
difference, BCa bounds, and the ISI-CoV counterparts. Remove every Random
column.

- [ ] **Step 4: Rewrite the primary execution cells**

Calculate `data_truth` with `mode="all"`, calculate `data_hdemg` with
`mode="hdsemg"` and `selection_seeds["hdsemg"]`, then call:

```python
plot_mn_fr_combined_data(data_hdemg, data_truth, conditions, pd)
print_statistics(
    data_hdemg,
    stats,
    mode="HD-sEMG",
    seed=bootstrap_seeds["HD-sEMG"],
)
```

Delete the two-mode bootstrap table and the entire filtered-random comparison
section. Keep `print_statistics` unchanged.

- [ ] **Step 5: Make every remaining notebook write v2-specific**

Append `_v2` before extensions in every `savefig` and `to_csv` destination,
including descriptive FR/ISI-CoV, selection visualization, histogram, and
threshold-sensitivity artifacts. Update printed paths to match.

- [ ] **Step 6: Run the primary structural test**

Expected: all assertions pass.

---

### Task 3: Apply the same rule and seed-stability analysis at every force level

**Files:**
- Modify: `diabetes/analysis_v2.py:2080-2265`
- Test: `/tmp/test_analysis_v2_additional_forces.py`

**Interfaces:**
- Consumes: `calculate_fr_data(..., mode="hdsemg", selection_seed=...)` and `calculate_fr_data(..., mode="all")`.
- Produces: fixed-seed HD-sEMG and truth results plus 1,000-seed selection distributions; the primary level has 50 pairs and each additional level retains its existing 10 pairs.

- [ ] **Step 1: Write failing source assertions**

Assert each force level contains exactly one `"hdsemg"` calculation and one
`"all"` calculation; assert the section contains none of `data_mvc10_random`,
`data_mvc50_random`, `10% MVC Random`, or `50% MVC Random`. Assert a shared
`selection_seed_stability` helper evaluates exactly 1,000 seeds and returns the
paired-difference distribution and eligible-pool summary.

- [ ] **Step 2: Verify the assertions fail against the current notebook**

Run the test with project-managed pytest.

- [ ] **Step 3: Update both force-level blocks**

For 10% MVC use `selection_seeds["mvc10_hdsemg"]`; for 50% MVC use
`selection_seeds["mvc50_hdsemg"]`. Retain the all-MU calculations and label
them `Simulation truth (all active MUs)`. Print the selection seed and criteria
for each HD-sEMG block. Do not catch selector-contract failures as “data not yet
available”; catch only missing-file errors, allowing analysis errors to surface.

Implement `selection_seed_stability` over the contiguous seed set
`20261000..20261999`. For each force level export every seed's Normal mean, DPN
mean, paired difference, Wilcoxon statistic, and p-value plus the eligible-pool
minimum, median, and maximum. Summarize the mean, SD, median, 2.5th and 97.5th
percentiles, fraction of nonnegative estimates, and fraction with nominal
`p < 0.05`. Label these percentiles as an across-seed selection range, never a
confidence interval.

Write `selection_seed_stability_20mvc_v2.csv`,
`selection_seed_stability_10mvc_v2.csv`, and
`selection_seed_stability_50mvc_v2.csv`. The manuscript must describe the two
10-pair levels as exploratory and seed-sensitive if their central selection
range crosses zero.

- [ ] **Step 4: Run the additional-force assertions**

Expected: all assertions pass.

---

### Task 4: Align threshold sensitivity with randomized HD-sEMG selection

**Files:**
- Modify: `diabetes/analysis_v2.py:2268-2545`
- Test: `/tmp/test_analysis_v2_sensitivity.py`

**Interfaces:**
- Consumes: cached per-MU firing rate and ISI-CoV arrays plus the shared set of 1,000 selection seeds.
- Produces: one median randomized 10-MU HD-sEMG curve with a central 95% across-seed envelope and the all-active-MU truth line.

- [ ] **Step 1: Write failing sensitivity assertions**

Assert that `selection_paired_difference` accepts `selection_seed`; the source
contains `rng.choice(..., replace=False)`; the threshold table contains 1,000
rows per threshold; and no code or prose contains `lowest_rate_first`,
`lowest-rate prioritization`, or `10 lowest-rate eligible MUs`.

- [ ] **Step 2: Verify failure against the former lowest-rate sweep**

Run the test with project-managed pytest.

- [ ] **Step 3: Implement the across-seed randomized strategy**

For each threshold and each of the 1,000 shared seeds, calculate eligible
indices, raise if any pool is undersized, and sample 10 without replacement
from a generator created from the explicit seed. Return fields:

```python
{
    "selection_strategy": "seeded_random_10",
    "selection_seed": int,
    "sample_size": 10,
    "normal_mean": float,
    "dpn_mean": float,
    "difference": float,
    "p_value": float,
    "n_pairs": int,
    "min_eligible_pool": int,
}
```

Use the identical ordered seed set at every threshold so threshold-to-threshold
changes use common random numbers and avoid unnecessary Monte Carlo roughness.
Document this correlation in notebook prose, exported metadata, the figure
caption, and the manuscript. State that this is a random-draw sensitivity, not
a spatial EMG simulation.

- [ ] **Step 4: Update outputs and narrative**

Write all 1,000 draws per threshold to
`selection_threshold_sensitivity_v2.csv` and the per-threshold summaries to
`selection_threshold_sensitivity_summary_v2.csv`. In
`selection_threshold_sensitivity_v2.png`, plot the across-seed median as one
blue curve, shade its 2.5th-to-97.5th percentile selection envelope, and retain
the red all-MU truth line. Do not plot an all-eligible curve as a competing
strategy. Remove the former upper-bound argument that depended on the ten
lowest-rate units; summarize each retained threshold only under the randomized
HD-sEMG rule.

- [ ] **Step 5: Run the sensitivity assertions**

Expected: all assertions pass.

---

### Task 5: Validate and execute the v2 notebook

**Files:**
- Verify: `diabetes/analysis_v2.py`
- Generate: only files whose names end in `_v2`

**Interfaces:**
- Consumes: completed Tasks 1-4 and existing simulation CSV inputs.
- Produces: current numerical evidence and figures used by the manuscript edit.

- [ ] **Step 1: Run static verification**

Run:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile diabetes/analysis_v2.py
env UV_CACHE_DIR=/tmp/uv-cache uv run marimo check diabetes/analysis_v2.py
git diff --check -- diabetes/analysis_v2.py
```

Expected: all commands exit 0.

- [ ] **Step 2: Run all focused synthetic/source tests together**

Run:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q \
  /tmp/test_analysis_v2_selection.py \
  /tmp/test_analysis_v2_primary_source.py \
  /tmp/test_analysis_v2_additional_forces.py \
  /tmp/test_analysis_v2_sensitivity.py
```

Expected: all tests pass.

- [ ] **Step 3: Execute the data-dependent notebook**

Run:

```bash
env UV_CACHE_DIR=/tmp/uv-cache MPLBACKEND=Agg uv run python diabetes/analysis_v2.py
```

Capture the output log under `/tmp`. Confirm the eligible-pool minimum, median,
and maximum at 20%, 10%, and 50% MVC, exact uniqueness of every 10-MU draw,
and all three 1,000-seed result counts. If execution exposes an undersized pool
or data error, stop and repair the analysis rather than using partial
manuscript numbers.

- [ ] **Step 4: Extract the manuscript evidence table**

Read the v2 CSVs and record, for 20%, 10%, and 50% MVC: Normal and DPN
simulation-level mean/SD/BCa CI, DPN-minus-Normal paired difference/BCa CI,
Wilcoxon statistic and p-value, selection seed, and sample count. Record the
all-MU truth values from the same execution. Read the threshold CSV for all
values described in manuscript prose and Figure 3. Record the across-seed
selection summaries separately from BCa confidence intervals and remove any
claim of force-level consistency that is not supported at 10% or 50% MVC.

- [ ] **Step 5: Prove isolation**

Re-run `sha256sum diabetes/analysis.py` and compare with Task 1. Run:

```bash
git status --short
git diff -- diabetes/analysis.py
```

Expected: the original-notebook hash is unchanged and its pre-existing diff is
unchanged; no non-v2 generated artifact has been newly modified by execution.

---

### Task 6: Synchronize `HDsEMG_rev_gdocs_v2`

**Files:**
- Modify in place: Google Doc `HDsEMG_rev_gdocs_v2` (`1nHSJ8t90oEvxLQ1dZhF-E8HsKcfKzIktMI5ZSNZNU08`, tab `t.0`)
- Read only: Google Doc `Response_to_Reviewers` (`1__DOZhSZ2u_hhE2HZ67mge-K_UleTmPrEELqzogfvYE`)

**Interfaces:**
- Consumes: Task 5 evidence table and v2 Figure 2/Figure 3 PNGs.
- Produces: a revision-protected native manuscript whose methods, numbers, interpretations, captions, and figures match `analysis_v2.py`.

- [ ] **Step 1: Perform the required trusted read and target inventory**

Preflight that `google_drive_batch_update_document` is callable and accepts
`requiredRevisionId`. If native text mutation is unavailable, do not attempt a
partial in-place edit: generate exact, source-grounded replacement prose in a
companion document for manual paste and disclose the limitation.

Use the file-backed trusted-read wrapper on the v2 article immediately before
the first write. Confirm title, document ID, tab tree (`t.0` only), revision ID,
target paragraph anchors, heading styles, relevant inline-object indexes, and
neighboring text. Re-read `Response_to_Reviewers` major issue 1, major issue 2,
and Reviewer 2 comment 2a as the rationale source.

- [ ] **Step 2: Build exact replacements from current evidence**

Replace only paragraphs that describe one of these superseded claims:

```text
three representations / two sampling modes
unrestricted Random mode
ten lowest-rate eligible MUs
Filtered-Random or eligibility-restricted random as a separate analysis
lowest-rate prioritization and its alleged amplification
Random-mode results at 20%, 10%, or 50% MVC
```

The replacement prose must state: the simulation truth is known for each
subject; HD-sEMG eligibility is unchanged; 10 eligible MUs are selected
randomly without replacement with fixed seeds; this avoids imposing an
unsupported spatial/size/depth ordering but does not simulate spatial surface
EMG dependence. Insert only Task 5 numerical results.

- [ ] **Step 3: Apply revision-protected paragraph replacements**

Issue targeted `deleteContentRange` plus `insertText` requests from the end of
the document toward the beginning, with `requiredRevisionId` from the fresh
read. Preserve paragraph style and text style from each replaced paragraph.
Re-read after each index-shifting batch and refresh the revision ID.

- [ ] **Step 4: Update affected figures and captions**

Change Figure 2 to the single-panel HD-sEMG-versus-truth v2 image and Figure 3
to the seeded-random threshold-sensitivity v2 image. Replace each image only
after resolving its exact inline-object range and sampled size/alignment. If
the connector cannot safely replace the bitmap, keep the text edit internally
consistent, report that exact limitation, and do not claim the manuscript is
fully synchronized.

- [ ] **Step 5: Verify the native document by readback**

Confirm:

```text
correct document ID and revision
one retained tab with unchanged topology
no analytical Random-mode or Filtered-Random references
no lowest-rate-prioritization claims
20%, 10%, 50%, across-seed stability, and threshold values match v2 outputs
simulation truth is the sole reference
spatial limitation remains explicit
additional-force prose is exploratory and makes no unsupported consistency claim
neighboring headings, tables, equations, citations, and unrelated figures remain unchanged
```

Export a PDF for final visual QA if the connector supports it and inspect the
affected pages for figure/caption mismatch, overflow, or broken pagination.

---

### Task 7: Final cross-artifact reconciliation

**Files:**
- Verify: `diabetes/analysis_v2.py`
- Verify: Google Doc `HDsEMG_rev_gdocs_v2`

**Interfaces:**
- Consumes: verified notebook and manuscript.
- Produces: final handoff evidence.

- [ ] **Step 1: Scan both artifacts for stale concepts**

Run a case-insensitive notebook scan for `Random mode`, `Filtered-Random`,
`lowest-rate`, and `prioritization`. Run the equivalent paragraph-text scan on
the Google Doc. Allow ordinary uses of random number generation and explanatory
sentences that explicitly say spatial dependence was not simulated.

- [ ] **Step 2: Re-run final notebook checks**

Repeat compilation, `marimo check`, focused tests, and `git diff --check` after
all repairs.

- [ ] **Step 3: Report exact completion scope**

List the modified v2 notebook, v2 generated evidence files, v2 Google Doc URL,
verification commands, and any connector limitation. Explicitly state that the
original notebook, original article, reviewer response, and unrelated dirty
files were preserved.
