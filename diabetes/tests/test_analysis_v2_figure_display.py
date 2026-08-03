from __future__ import annotations

import ast
from pathlib import Path
import unittest

import matplotlib
from matplotlib import colors as mcolors

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


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


if __name__ == "__main__":
    unittest.main()
