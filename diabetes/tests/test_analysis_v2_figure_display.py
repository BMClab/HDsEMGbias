from __future__ import annotations

import ast
from contextlib import chdir
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
import warnings

import matplotlib
import marimo as mo
from matplotlib import colors as mcolors
from matplotlib.ticker import MaxNLocator

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


NOTEBOOK = Path(__file__).parents[2] / "diabetes" / "analysis_v2.py"


def load_notebook_function(name, extra_namespace=None):
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
    namespace = {"np": np}
    if extra_namespace is not None:
        namespace.update(extra_namespace)
    exec(compile(module, str(NOTEBOOK), "exec"), namespace)
    return namespace[name]


def load_notebook_functions(*names):
    tree = ast.parse(NOTEBOOK.read_text())
    definitions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name in names
    }
    missing = set(names) - set(definitions)
    if missing:
        raise AssertionError(f"missing notebook functions: {sorted(missing)}")
    module = ast.Module(body=[definitions[name] for name in names], type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {"np": np}
    exec(compile(module, str(NOTEBOOK), "exec"), namespace)
    return tuple(namespace[name] for name in names)


class ProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.collect_provenance = load_notebook_function("collect_provenance")
        self.format_provenance_markdown = load_notebook_function(
            "format_provenance_markdown"
        )
        self.executed_at = datetime(2026, 8, 4, 22, 42, 41, tzinfo=timezone.utc)

    def test_collects_versions_clean_git_state_and_source_digest(self):
        versions = {
            "marimo": "0.23.16",
            "numpy": "1.26.0",
            "pandas": "3.0.5",
            "matplotlib": "3.11.1",
            "scipy": "1.16.3",
        }

        def package_version(name):
            return versions[name]

        with TemporaryDirectory() as directory:
            source = Path(directory) / "diabetes" / "analysis_v2.py"
            source.parent.mkdir()
            source.write_text("print('analysis')\n")

            def run_git(_repo_root, *arguments):
                if arguments == ("rev-parse", "--show-toplevel"):
                    self.assertEqual(Path(_repo_root).resolve(), source.parent.resolve())
                    return directory
                if arguments == ("rev-parse", "HEAD"):
                    return "0123456789abcdef"
                if arguments == ("status", "--porcelain"):
                    return ""
                raise AssertionError(arguments)

            result = self.collect_provenance(
                source,
                now=self.executed_at,
                package_version=package_version,
                run_git=run_git,
            )

        self.assertEqual(result["Executed at"], "2026-08-04T22:42:41+00:00")
        self.assertEqual(result["marimo"], "0.23.16")
        self.assertEqual(result["NumPy"], "1.26.0")
        self.assertEqual(result["pandas"], "3.0.5")
        self.assertEqual(result["Matplotlib"], "3.11.1")
        self.assertEqual(result["SciPy"], "1.16.3")
        self.assertEqual(result["Git commit"], "0123456789abcdef")
        self.assertEqual(result["Git state"], "clean")
        self.assertEqual(
            result["Notebook SHA-256"],
            hashlib.sha256(b"print('analysis')\n").hexdigest(),
        )

    def test_marks_a_dirty_worktree(self):
        def run_git(_repo_root, *arguments):
            if arguments == ("rev-parse", "--show-toplevel"):
                return str(NOTEBOOK.parents[1])
            if arguments == ("rev-parse", "HEAD"):
                return "0123456789abcdef"
            if arguments == ("status", "--porcelain"):
                return " M uv.lock"
            raise AssertionError(arguments)

        result = self.collect_provenance(
            NOTEBOOK,
            now=self.executed_at,
            package_version=lambda _name: "test-version",
            run_git=run_git,
        )

        self.assertEqual(result["Git state"], "dirty")

    def test_formats_a_real_unindented_markdown_table(self):
        markdown = self.format_provenance_markdown(
            {"Executed at": "2026-08-04T22:42:41+00:00", "Git state": "clean"}
        )
        rendered = mo.md(markdown)

        self.assertTrue(
            all(not line.startswith("    ") for line in markdown.splitlines())
        )
        self.assertIn("<table>", rendered.text)
        self.assertIn("<td><code>clean</code></td>", rendered.text)
        self.assertEqual(rendered.text.count("<tr>"), 3)

    def test_degrades_when_package_git_and_source_metadata_are_unavailable(self):
        def unavailable_version(_name):
            raise RuntimeError("metadata unavailable")

        def unavailable_git(_repo_root, *_arguments):
            raise OSError("git unavailable")

        result = self.collect_provenance(
            NOTEBOOK.with_name("missing.py"),
            now=self.executed_at,
            package_version=unavailable_version,
            run_git=unavailable_git,
        )

        for label in ("marimo", "NumPy", "pandas", "Matplotlib", "SciPy"):
            self.assertEqual(result[label], "unavailable")
        self.assertEqual(result["Git commit"], "unavailable")
        self.assertEqual(result["Git state"], "unavailable")
        self.assertEqual(result["Notebook SHA-256"], "unavailable")


class FigureDisplayTest(unittest.TestCase):
    def test_isi_cov_histograms_do_not_emit_empty_legend_warning(self):
        conditions = ("normal", "DPN")
        frame = SimpleNamespace(
            values=np.array(
                [
                    [0, 0.0],
                    [0, 5000.0],
                    [1, 0.0],
                    [1, 5000.0],
                ]
            )
        )
        fake_pandas = SimpleNamespace(read_csv=lambda *_args, **_kwargs: frame)

        def compute_cv(_neurons, _data, _t_start, _t_end):
            return np.array([0.1, 1.0]), np.array([100.0, 0.0])

        isi_cov_histograms = load_notebook_function(
            "isi_cov_histograms",
            {
                "MaxNLocator": MaxNLocator,
                "batch_name": "variability",
                "compute_cv": compute_cv,
                "conditions": conditions,
                "fontweight": "normal",
                "fs_label": 10,
                "fs_legend": 8,
                "fs_ticklabels": 8,
                "fs_title": 10,
                "path": "unused/",
                "pd": fake_pandas,
                "plt": plt,
                "t_end": 10000,
                "t_start": 4000,
            },
        )

        with TemporaryDirectory() as directory, chdir(directory):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                isi_cov_histograms([0])

        empty_legend_warnings = [
            warning
            for warning in caught
            if "No artists with labels found" in str(warning.message)
        ]
        self.assertEqual(empty_legend_warnings, [])

    def test_primary_axis_uses_requested_range_with_visible_annotation(self):
        configure_primary_fr_axis = load_notebook_function(
            "configure_primary_fr_axis"
        )
        figure, axis = plt.subplots()
        self.addCleanup(plt.close, figure)

        significance_y = configure_primary_fr_axis(axis, tick_fontsize=12)

        self.assertEqual(tuple(axis.get_ylim()), (8.0, 16.0))
        self.assertEqual(axis.get_yticks().tolist(), [8, 10, 12, 14, 16])
        self.assertEqual(significance_y, 15)
        self.assertGreater(significance_y - 0.5, axis.get_ylim()[0])
        self.assertLess(significance_y + 0.1, axis.get_ylim()[1])

    def test_primary_summaries_are_distinct_from_blue_subject_markers(self):
        add_primary_fr_summaries = load_notebook_function(
            "add_primary_fr_summaries"
        )
        figure, axis = plt.subplots()
        self.addCleanup(plt.close, figure)
        subject_markers = axis.scatter([1], [12], color="tab:blue")

        estimate_handle, truth_handle = add_primary_fr_summaries(
            axis,
            mean_fr=np.array([12.0, 11.5]),
            yerr=np.array([[0.2, 0.2], [0.3, 0.3]]),
            truth_mean_fr=np.array([13.0, 12.5]),
            normal_jitter=np.array([0.9, 1.1]),
            truth_line_width=0.2,
        )

        mean_line, cap_lines, interval_collections = estimate_handle.lines
        self.assertEqual(mean_line.get_marker(), "o")
        self.assertEqual(mean_line.get_color(), "red")
        self.assertEqual(mean_line.get_markersize(), 8)
        self.assertGreater(
            mean_line.get_markersize(),
            np.sqrt(subject_markers.get_sizes()[0]),
        )
        self.assertGreater(mean_line.get_zorder(), subject_markers.get_zorder())
        for cap_line in cap_lines:
            self.assertEqual(cap_line.get_color(), "red")
            self.assertGreater(cap_line.get_zorder(), mean_line.get_zorder())
        for interval_collection in interval_collections:
            np.testing.assert_allclose(
                interval_collection.get_colors()[0, :3],
                mcolors.to_rgb("red"),
            )
            self.assertGreater(
                interval_collection.get_zorder(),
                mean_line.get_zorder(),
            )
        np.testing.assert_allclose(
            truth_handle.get_colors()[0, :3],
            mcolors.to_rgb("green"),
        )

    def test_primary_significance_annotation_matches_red_hdemg_summary(self):
        add_primary_fr_significance = load_notebook_function(
            "add_primary_fr_significance"
        )
        figure, axis = plt.subplots()
        self.addCleanup(plt.close, figure)

        bracket_lines, significance_text = add_primary_fr_significance(
            axis,
            p_value=0.0008,
            significance_y=17,
        )

        self.assertEqual(len(bracket_lines), 3)
        for bracket_line in bracket_lines:
            self.assertEqual(bracket_line.get_color(), "red")
        self.assertEqual(significance_text.get_text(), "***")
        self.assertEqual(significance_text.get_color(), "red")

    def test_threshold_truth_reference_is_green_and_emphasized(self):
        add_threshold_truth_reference = load_notebook_function(
            "add_threshold_truth_reference"
        )
        figure, axis = plt.subplots()
        self.addCleanup(plt.close, figure)
        (randomized_line,) = axis.plot(
            [0.15, 0.30],
            [-0.6, -0.5],
            color="tab:blue",
            linewidth=2,
        )

        truth_line = add_threshold_truth_reference(
            axis,
            truth_difference=1.03,
        )

        self.assertEqual(truth_line.get_color(), "green")
        self.assertEqual(truth_line.get_linestyle(), "--")
        self.assertGreater(
            truth_line.get_linewidth(),
            randomized_line.get_linewidth(),
        )


class ForceLevelRobustnessTest(unittest.TestCase):
    def test_force_robustness_title_and_legend_do_not_overlap(self):
        finalize_force_robustness_figure = load_notebook_function(
            "finalize_force_robustness_figure"
        )
        figure, axes = plt.subplots(1, 2, figsize=(14, 6))
        self.addCleanup(plt.close, figure)
        (first_handle,) = axes[0].plot([10, 20], [0, 1], label="Estimate")
        (second_handle,) = axes[0].plot([10, 20], [1, 0], label="Truth")

        title, legend = finalize_force_robustness_figure(
            figure,
            [first_handle, second_handle],
            ["Estimate", "Truth"],
            legend_fontsize=16,
            title_fontsize=20,
            title_fontweight="normal",
        )
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()

        self.assertGreater(
            title.get_window_extent(renderer).y0,
            legend.get_window_extent(renderer).y1,
        )

    def test_paired_subject_effects_preserve_ids_and_use_dpn_minus_normal(self):
        paired_subject_effects = load_notebook_function("paired_subject_effects")
        data = {
            "mn_rate_trial_mean": {
                "normal": np.array([10.0, 11.0, 12.0]),
                "DPN": np.array([11.0, 10.0, 14.0]),
            },
            "simulation_ids": {
                "normal": np.array([0, 1, 2]),
                "DPN": np.array([0, 1, 2]),
            },
        }

        result = paired_subject_effects(
            data, "mn_rate_trial_mean", ("normal", "DPN")
        )

        np.testing.assert_array_equal(result["simulation_ids"], [0, 1, 2])
        np.testing.assert_allclose(result["effect"], [1.0, -1.0, 2.0])

    def test_paired_subject_effects_reject_misaligned_condition_ids(self):
        paired_subject_effects = load_notebook_function("paired_subject_effects")
        data = {
            "mn_rate_trial_mean": {
                "normal": np.array([10.0, 11.0]),
                "DPN": np.array([11.0, 12.0]),
            },
            "simulation_ids": {
                "normal": np.array([0, 1]),
                "DPN": np.array([1, 0]),
            },
        }

        with self.assertRaisesRegex(ValueError, "simulation IDs"):
            paired_subject_effects(
                data, "mn_rate_trial_mean", ("normal", "DPN")
            )

    def test_holm_adjustment_is_monotone_in_sorted_p_values(self):
        holm_adjust_pvalues = load_notebook_function("holm_adjust_pvalues")

        adjusted = holm_adjust_pvalues([0.01, 0.04, 0.03])

        np.testing.assert_allclose(adjusted, [0.03, 0.06, 0.06])

    def test_force_dependence_uses_primary_reference_and_all_pairwise_contrasts(self):
        holm_adjust_pvalues, summarize_force_level_dependence = (
            load_notebook_functions(
                "holm_adjust_pvalues", "summarize_force_level_dependence"
            )
        )

        def simple_paired_summary(first, second, seed, n_resamples):
            del seed, n_resamples
            difference = np.asarray(second) - np.asarray(first)
            wilcoxon = stats.wilcoxon(first, second, method="auto")
            return {
                "n_pairs": len(difference),
                "difference": float(difference.mean()),
                "difference_ci": (
                    float(difference.min()),
                    float(difference.max()),
                ),
                "wilcoxon_statistic": float(wilcoxon.statistic),
                "p_value": float(wilcoxon.pvalue),
            }

        simulation_ids = np.arange(4)
        effects = {
            10: {
                "simulation_ids": simulation_ids,
                "effect": np.array([-1.0, 0.0, 1.0, 2.0]),
            },
            20: {
                "simulation_ids": simulation_ids,
                "effect": np.array([0.0, 1.0, 2.0, 3.0]),
            },
            50: {
                "simulation_ids": simulation_ids,
                "effect": np.array([2.0, 3.0, 4.0, 5.0]),
            },
        }

        result = summarize_force_level_dependence(
            effects,
            simple_paired_summary,
            stats,
            holm_adjust_pvalues,
            seed=123,
            n_resamples=100,
            reference_force=20,
        )

        self.assertEqual(result["n_subjects"], 4)
        self.assertEqual(result["force_levels_mvc"], [10, 20, 50])
        self.assertEqual(
            [
                (row["first_force_mvc"], row["second_force_mvc"])
                for row in result["contrasts"]
            ],
            [(20, 10), (20, 50), (10, 50)],
        )
        np.testing.assert_allclose(
            [row["effect_contrast"] for row in result["contrasts"]],
            [-1.0, 2.0, 3.0],
        )
        self.assertTrue(
            all(
                row["holm_adjusted_p_value"] >= row["raw_p_value"]
                for row in result["contrasts"]
            )
        )


if __name__ == "__main__":
    unittest.main()
