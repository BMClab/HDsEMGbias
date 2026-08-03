# Figure 2 and Figure 3 Display Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten Figure 2 to an 8–18 pps y-axis, make its summary artists visually distinct from the subject observations, and verify that Figure 3 contains no lowest-rate or eligibility-only comparison.

**Architecture:** Extract Figure 2's vertical-axis configuration into one small plotting helper that operates on a real Matplotlib `Axes` and returns the in-bounds significance-bracket height. The primary plotting function consumes that helper; the deterministic analysis and Figure 3 implementation remain unchanged. A focused test executes the production helper against a real `Axes`, followed by full notebook execution and original-resolution inspection of both PNGs.

**Tech Stack:** Python 3.12, marimo 0.17.8, Matplotlib, standard-library `ast` and `unittest`.

## Global Constraints

- Modify only `diabetes/analysis_v2.py`, its two requested v2 PNGs, and the focused regression test.
- Figure 2 must use an 8–18 pps y-axis with ticks every 2 pps at 8, 10, 12, 14, 16, and 18 pps.
- Figure 2's significance bracket and label must remain fully visible inside the axes at 17 pps.
- Figure 2's simulation-truth segments must be green.
- Figure 2's HD-sEMG mean must be a red 8-point circle, still larger than the default 6-point blue subject markers, with its 95% BCa interval and caps red and drawn above the mean marker and blue observations.
- Figure 2's significance bracket and asterisks must be red, matching the HD-sEMG inferential summary they describe.
- Figure 3 must retain the randomized 10-eligible-MU median, central 95% across-selection-seed band, and all-active-MU truth.
- Figure 3's all-active-MU truth must be a green dashed 3-point line, thicker than the blue 2-point randomized median curve.
- Figure 3 must not contain a lowest-rate or eligibility-only comparison curve; its only green line is the truth reference.
- Do not alter simulations, selections, statistics, CSV values, manuscript prose, or `diabetes/analysis.py`.
- Leave changes uncommitted unless the user explicitly requests a commit.

---

### Task 1: Lock the Figure 2 vertical display behavior

**Files:**
- Create: `diabetes/tests/test_analysis_v2_figure_display.py`
- Verify: `diabetes/analysis_v2.py:437-578`

**Interfaces:**
- Consumes: a nested notebook helper named `configure_primary_fr_axis(ax, tick_fontsize)`.
- Produces: a real Matplotlib `Axes` configured to 8–18 pps with ticks every 2 pps; returns the significance y-position as `float`.

- [ ] **Step 1: Write the failing behavior test**

```python
from __future__ import annotations

import ast
from pathlib import Path
import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


NOTEBOOK = Path(__file__).parents[2] / "diabetes" / "analysis_v2.py"


def load_notebook_function(name):
    tree = ast.parse(NOTEBOOK.read_text())
    definitions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    }
    if name not in definitions:
        raise AssertionError(f"missing notebook function: {name}")
    module = ast.Module(body=[definitions[name]], type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, str(NOTEBOOK), "exec"), namespace)
    return namespace[name]


class FigureDisplayTest(unittest.TestCase):
    def test_primary_axis_uses_requested_range_with_visible_annotation(self):
        configure_primary_fr_axis = load_notebook_function(
            "configure_primary_fr_axis"
        )
        figure, axis = plt.subplots()
        self.addCleanup(plt.close, figure)

        significance_y = configure_primary_fr_axis(axis, tick_fontsize=12)

        self.assertEqual(tuple(axis.get_ylim()), (8.0, 18.0))
        self.assertEqual(axis.get_yticks().tolist(), [8, 10, 12, 14, 16, 18])
        self.assertEqual(significance_y, 17)
        self.assertGreater(significance_y - 0.5, axis.get_ylim()[0])
        self.assertLess(significance_y + 0.1, axis.get_ylim()[1])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```bash
.venv/bin/python -m unittest diabetes.tests.test_analysis_v2_figure_display -v
```

Expected: FAIL with `missing notebook function: configure_primary_fr_axis`.

---

### Task 2: Configure Figure 2 through the tested helper

**Files:**
- Modify: `diabetes/analysis_v2.py:437-558`
- Test: `diabetes/tests/test_analysis_v2_figure_display.py`

**Interfaces:**
- Consumes: `configure_primary_fr_axis(ax, tick_fontsize)` from the same marimo cell.
- Produces: the unchanged `plot_mn_fr_combined_data(data_hdemg, data_truth, conditions, pd)` interface and output path.

- [ ] **Step 1: Add the minimal production helper immediately before the primary plotting function**

```python
    def configure_primary_fr_axis(ax, tick_fontsize):
        """Set Figure 2's vertical display and return its bracket height."""
        ax.set_ylim(8, 18)
        ax.set_yticks([8, 10, 12, 14, 16, 18])
        ax.set_yticklabels([8, 10, 12, 14, 16, 18], fontsize=tick_fontsize)
        return 17
```

- [ ] **Step 2: Consume the helper in `plot_mn_fr_combined_data`**

Immediately after creating `fig, ax`, call:

```python
        significance_y = configure_primary_fr_axis(ax, fs_ticklabels)
```

Use the returned position in the significance block:

```python
        if p_value < 0.05:
            y_pos = significance_y
```

Remove the old `ax.set_ylim(0, 22)`, `ax.set_yticks([0, 5, 10, 15, 20])`, and matching `set_yticklabels` calls. Do not change other plot logic.

- [ ] **Step 3: Run the focused test and verify it passes**

Run:

```bash
.venv/bin/python -m unittest diabetes.tests.test_analysis_v2_figure_display -v
```

Expected: 1 test passes.

- [ ] **Step 4: Run the existing primary and sensitivity tests**

Run:

```bash
.venv/bin/python -m unittest discover -s /tmp -p 'test_analysis_v2_primary_source.py' -v
.venv/bin/python -m unittest discover -s /tmp -p 'test_analysis_v2_sensitivity.py' -v
```

Expected: all existing Figure 2 and Figure 3 structure checks pass.

---

### Task 3: Regenerate and verify the v2 figures

**Files:**
- Generate: `diabetes/figures/mn_firing_rate_comparison_combined_v2.png`
- Generate: `diabetes/figures/selection_threshold_sensitivity_v2.png`
- Verify: `diabetes/csv_results/mn_firing_rate_p_values_combined_v2.csv`
- Verify: `diabetes/csv_results/selection_threshold_sensitivity_summary_v2.csv`
- Verify: `diabetes/analysis.py`

**Interfaces:**
- Consumes: existing simulation CSV inputs and deterministic seeds in `analysis_v2.py`.
- Produces: refreshed Figure 2 and Figure 3 PNGs with unchanged numerical CSV evidence.

- [ ] **Step 1: Record the pre-execution numerical hashes**

Run:

```bash
sha256sum \
  diabetes/csv_results/mn_firing_rate_p_values_combined_v2.csv \
  diabetes/csv_results/selection_threshold_sensitivity_summary_v2.csv \
  diabetes/analysis.py
```

Retain all three hashes for the post-execution comparison.

- [ ] **Step 2: Run static notebook checks**

Run:

```bash
.venv/bin/python -m py_compile diabetes/analysis_v2.py
timeout 5 strace -f -o /tmp/marimo-figure-check.strace \
  .venv/bin/marimo check --strict --format json diabetes/analysis_v2.py
```

Expected: compilation exits 0 and Marimo reports zero issues.

- [ ] **Step 3: Execute the data-dependent notebook**

Run:

```bash
env MPLBACKEND=Agg .venv/bin/python diabetes/analysis_v2.py
```

Expected: execution exits 0 and overwrites both requested `_v2.png` files.

- [ ] **Step 4: Verify numerical isolation**

Repeat the Step 1 `sha256sum` command. Expected: all three hashes are identical to their pre-execution values.

- [ ] **Step 5: Inspect both figures at original resolution**

Verify:

- Figure 2 spans 8–18 pps with 2-pps ticks and its bracket and label are not clipped.
- Figure 3 contains one blue randomized median curve, its blue seed band, and a thicker green dashed truth line.
- Figure 3 contains no additional green, lowest-rate, or eligibility-only comparison curve.

- [ ] **Step 6: Run final worktree checks**

Run:

```bash
.venv/bin/python -m unittest discover -s diabetes/tests -p 'test_*.py' -v
git diff --check
git status --short --branch
```

Expected: all focused tests pass, no whitespace errors are reported, and no original or non-v2 analysis artifact is newly modified by this task.

---

### Task 4: Distinguish Figure 2's summary artists

**Files:**
- Modify: `diabetes/tests/test_analysis_v2_figure_display.py`
- Modify: `diabetes/analysis_v2.py`
- Generate: `diabetes/figures/mn_firing_rate_comparison_combined_v2.png`

**Interfaces:**
- Adds a nested helper named `add_primary_fr_summaries(...)` that returns the
  Matplotlib error-bar container and truth-line collection used by the legend.
- Leaves numerical inputs, results, axis settings, labels, and output path
  unchanged.

- [ ] **Step 1: Add a rendering-level failing test**

Use a real Matplotlib `Axes` to assert that the production helper draws a red
circle for the HD-sEMG mean, red BCa bars and caps, and green simulation-truth
segments. Assert that the 8-point mean marker is larger than the default blue
scatter marker, while the interval is layered above it. Exercise the significance helper on
the same kind of real axis and assert that its bracket lines and asterisks are
red.

- [ ] **Step 2: Run the focused test and confirm the expected missing-helper failure**

- [ ] **Step 3: Add the minimal helper and route Figure 2 through it**

Keep the blue subject scatters unchanged. Add the summary artists after them,
using their explicit z-orders to guarantee visibility.

- [ ] **Step 4: Regenerate and verify Figure 2**

Run the focused and existing notebook tests, compile and check the notebook,
execute it, confirm numerical hashes are unchanged, and inspect the exported
PNG at original resolution.

---

### Task 5: Emphasize Figure 3's simulation-truth reference

**Files:**
- Modify: `diabetes/tests/test_analysis_v2_figure_display.py`
- Modify: `diabetes/analysis_v2.py`
- Generate: `diabetes/figures/selection_threshold_sensitivity_v2.png`

**Interfaces:**
- Adds `add_threshold_truth_reference(ax, truth_difference)`, returning the
  real Matplotlib `Line2D` used for Figure 3's truth reference.
- Leaves the threshold sweep, randomized median, seed band, labels, axis
  limits, numerical exports, and output path unchanged.

- [ ] **Step 1: Add a real-Matplotlib failing test**

Draw a 2-point blue randomized line and call the intended production helper.
Assert that the returned truth line is green, dashed, and thicker than the blue
line. The test must fail because the helper is absent.

- [ ] **Step 2: Add the minimal truth-reference helper**

Use `ax.axhline(...)` with `color="green"`, `linestyle="--"`, and
`linewidth=3`, retaining the existing dynamic label.

- [ ] **Step 3: Route Figure 3 through the helper and verify**

Run the focused test, existing notebook tests, compilation, Marimo check, and
full deterministic notebook execution. Confirm the numerical CSV hashes and
Figure 2 hash are unchanged, then inspect Figure 3 at original resolution.
