# Randomized HD-sEMG v2 analysis design

## Scope

Update only the versioned analysis source `diabetes/analysis_v2.py` and the
native Google Doc `HDsEMG_rev_gdocs_v2`. Use `Response_to_Reviewers` as the
rationale source. Preserve the original notebook, original manuscript, and
unrelated dirty worktree files.

## Analysis contract

The simulation exposes every active motor unit (MU), so the subject-specific
mean across all active MUs is the sole true reference. The notebook will expose
one sampled analysis mode:

- **HD-sEMG mode:** apply the existing eligibility criteria
  (`5 < firing rate < 15 pps` and `ISI-CoV <= 0.3`), then use a seeded NumPy
  generator to draw 10 unique eligible MUs without replacement for each
  simulation and condition.
- **Simulation truth:** retain all active MUs and calculate one true mean per
  simulation and condition. This is a reference, not a sampling mode.

If an eligible pool contains fewer than 10 MUs, fail with a contextual error
instead of silently changing the sample size. Keep one simulation-level mean as
the inferential unit and retain MU-level values only for descriptive displays.

## Notebook changes

1. Replace the current lowest-rate HD-sEMG selector with the existing
   random-within-eligibility behavior, under a clear HD-sEMG name and fixed
   selection seed.
2. Remove the unrestricted Random mode from configuration, execution,
   statistics tables, CSV schemas, plots, prose, and returned cell values.
3. Remove the now-redundant HD-sEMG-versus-Filtered-Random section. Preserve
   shared helpers such as `print_statistics` and update their callers.
4. Reduce the primary comparison plot to HD-sEMG estimates plus the Normal and
   DPN simulation-truth reference lines.
5. Apply the same seeded HD-sEMG rule at 10% and 50% MVC; compare each only with
   its all-MU simulation truth.
6. Rework the threshold-sensitivity analysis so 1,000 reproducible selection
   seeds are evaluated at every threshold. Plot the median randomized 10-MU
   estimate and its central 95% across-seed envelope against the all-MU truth;
   do not plot an all-eligible curve as a competing strategy. Use the same seed
   set at every threshold and disclose that common-random-number design.
7. Keep descriptive all-MU analyses that answer separate questions, provided
   they are not labeled as a competing mode.
8. Preserve the unrestricted random sampler used by the descriptive 100-MU
   firing-rate/ISI-CoV scatter, but do not expose it as an inferential mode.
9. Add a 1,000-seed stability analysis at 20%, 10%, and 50% MVC. Keep the
   existing 10 paired subjects at 10% and 50% MVC and describe those analyses
   as exploratory and seed-sensitive when their across-seed distributions span
   zero; do not claim force-level consistency unsupported by the recomputation.

## Manuscript changes

Revise the abstract, Introduction, Methods/Analysis, Results, figure captions,
Discussion, and conclusion wherever they describe the removed Random mode,
lowest-rate prioritization, or the former three-way comparison. Report only
values recomputed from the v2 notebook. Explain that random selection within
the eligible pool avoids imposing an unsupported spatial, size, or depth-based
detection ordering; it does not simulate a volume conductor or spatial surface
EMG dependence. Preserve that limitation explicitly.

The article's main contrast will be the seeded 10-MU HD-sEMG-like estimate
versus the known subject-specific all-active-MU truth. The additional-force and
threshold-sensitivity text must describe the same rule.

## Verification

- Confirm the original `diabetes/analysis.py` is byte-for-byte unchanged by
  this task.
- Compile `analysis_v2.py`, run `marimo check`, and run focused synthetic tests
  proving eligibility, uniqueness, exact sample size, seed reproducibility, and
  failure on undersized eligible pools.
- Execute the data-dependent v2 analysis needed to recompute the primary,
  10%-MVC, 50%-MVC, and threshold-sensitivity results without overwriting the
  user's unrelated generated artifacts.
- Verify eligible-pool minima, medians, and maxima at every force level and
  verify the 1,000-seed distributions, rather than treating the invariant
  10-MU output count as evidence of robustness.
- Scan the notebook and manuscript for obsolete analytical uses of `Random`,
  `Filtered-Random`, `lowest-rate`, and `prioritization`.
- Edit the existing native v2 Google Doc with revision protection, preserve its
  tab topology and native objects, then verify changed text and neighboring
  structure by readback. Preflight the native batch-update capability before
  composing mutations. Update affected embedded figures when the connector
  supports a structure-preserving replacement; if text or image mutation is
  unavailable, create exact replacement prose as a companion deliverable and
  disclose the limitation rather than leaving an inconsistent figure silently.
