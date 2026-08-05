import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lower apparent motor-unit discharge rates in simulated diabetic peripheral neuropathy reflect HD-sEMG-like selection rather than lower population rates

    > Renato Naville Watanabe and Marcos Duarte, Federal University of ABC, Brazil
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependencies
    """)
    return


@app.cell
def _():
    import os
    import sys

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.ticker import MaxNLocator
    from scipy import stats
    from scipy.signal import butter, filtfilt
    return MaxNLocator, butter, filtfilt, mo, np, os, pd, plt, stats, sys


@app.cell(hide_code=True)
def _(mo):
    def collect_provenance(
        notebook_path,
        *,
        now=None,
        package_version=None,
        run_git=None,
    ):
        from datetime import datetime
        import hashlib
        from importlib import metadata
        from pathlib import Path
        import platform
        import subprocess

        if now is None:
            now = datetime.now().astimezone()
        if package_version is None:
            package_version = metadata.version

        if run_git is None:
            def run_git(repo_root, *arguments):
                completed = subprocess.run(
                    ["git", *arguments],
                    cwd=repo_root,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return completed.stdout.strip()

        source_path = Path(notebook_path).resolve()

        try:
            repo_root = Path(
                run_git(source_path.parent, "rev-parse", "--show-toplevel")
            ).resolve()
        except (OSError, subprocess.CalledProcessError):
            repo_root = None

        provenance = {
            "Executed at": now.isoformat(timespec="seconds"),
            "Python": platform.python_version(),
        }
        packages = {
            "marimo": "marimo",
            "NumPy": "numpy",
            "pandas": "pandas",
            "Matplotlib": "matplotlib",
            "SciPy": "scipy",
        }
        for label, distribution in packages.items():
            try:
                provenance[label] = package_version(distribution)
            except Exception:
                provenance[label] = "unavailable"

        try:
            if repo_root is None:
                raise OSError("repository root unavailable")
            provenance["Git commit"] = run_git(repo_root, "rev-parse", "HEAD")
            status = run_git(repo_root, "status", "--porcelain")
            provenance["Git state"] = "dirty" if status else "clean"
        except (OSError, subprocess.CalledProcessError):
            provenance["Git commit"] = "unavailable"
            provenance["Git state"] = "unavailable"

        try:
            provenance["Notebook SHA-256"] = hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest()
        except OSError:
            provenance["Notebook SHA-256"] = "unavailable"

        return provenance

    def format_provenance_markdown(provenance):
        rows = "\n".join(
            f"| {label} | `{value}` |" for label, value in provenance.items()
        )
        return (
            "### Execution provenance\n\n"
            "| Item | Value |\n"
            "|---|---|\n"
            f"{rows}"
        )

    _provenance = collect_provenance(__file__)
    mo.md(format_provenance_markdown(_provenance))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analysis configuration
    """)
    return


@app.cell
def _(np, sys):
    # Parameters
    sys.path.append("./../")
    path = "diabetes/results/"
    batch_name = "variability"
    trials = np.arange(50)

    conditions = ["normal", "DPN"]

    modes = ["HD-sEMG"]
    color = {conditions[0]: "tab:blue", conditions[1]: "tab:orange"}

    fs_ticklabels = 16
    fs_label = 16
    fs_legend = 16
    fs_title = 20
    markersize = 12
    fontweight = "normal"

    t_start = 4000
    t_end = 10000

    criteria = {"fmin": 5, "fmax": 15, "isicv": 0.3}
    # criteria = {"fmin": 0, "fmax": np.inf, "isicv": 0.3}

    mn_number = 10
    selection_seeds = {
        "hdsemg": 20260102,
        "fr_cv": 20260103,
        "mvc10_hdsemg": 20260104,
        "mvc50_hdsemg": 20260105,
        "threshold_sensitivity": 20260116,
        "seed_stability_start": 20261000,
    }
    n_selection_seeds = 1_000
    n_resamples = 100_000
    bootstrap_seeds = {
        "HD-sEMG": 20260106,
        "All motor units": 20260109,
        "10% MVC HD-sEMG": 20260110,
        "10% MVC all motor units": 20260111,
        "50% MVC HD-sEMG": 20260113,
        "50% MVC all motor units": 20260114,
        "Force-level robustness": 20260117,
    }
    return (
        batch_name,
        bootstrap_seeds,
        color,
        conditions,
        criteria,
        fontweight,
        fs_label,
        fs_legend,
        fs_ticklabels,
        fs_title,
        mn_number,
        modes,
        n_resamples,
        n_selection_seeds,
        path,
        selection_seeds,
        t_end,
        t_start,
        trials,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analysis helpers
    """)
    return


@app.cell
def _(
    bootstrap_seeds,
    butter,
    color,
    criteria,
    filtfilt,
    fs_label,
    fs_ticklabels,
    fs_title,
    mn_number,
    modes,
    n_resamples,
    np,
    os,
    plt,
    stats,
):
    def select_mns_randomly(data, t_start, t_end, size=mn_number, column_spikes=1, rng=None):
        """Select a reproducible sample of unique active motor units."""
        if rng is None:
            raise ValueError("A seeded NumPy Generator is required for random selection.")

        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        active_neurons = np.unique(steady_data[:, 0])
        if active_neurons.size < size:
            raise ValueError(
                f"Cannot select {size} unique motor units from "
                f"{active_neurons.size} active units."
            )
        selected_neurons = rng.choice(active_neurons, size=size, replace=False)

        return selected_neurons


    def select_all_mns(data, t_start, t_end, column_spikes=1):
        """Select all motor units (no filtering criteria)."""
        unique_neurons = np.unique(data[:, 0])
        return unique_neurons.astype(int)


    def select_mns_hdemg(
        data,
        t_start,
        t_end,
        column_spikes=1,
        criteria=criteria,
        mn_number=mn_number,
        rng=None,
    ):
        """Select a seeded random sample from HD-sEMG-eligible motor units."""
        if rng is None:
            raise ValueError("A seeded NumPy Generator is required for random selection.")

        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        unique_neurons = np.unique(data[:, 0])
        ISI_CV, _ = compute_cv(
            unique_neurons, steady_data, t_start, t_end, column_spikes=column_spikes
        )
        fr = compute_fr(unique_neurons, data, t_start, t_end, column_spikes=column_spikes)
        # Apply the HD-sEMG-like eligibility criteria.
        selection_criteria = np.where(
            (fr > criteria["fmin"]) & (fr < criteria["fmax"]) & (ISI_CV <= criteria["isicv"])
        )[0]
        eligible_neurons = unique_neurons[selection_criteria].astype(int)
        if eligible_neurons.size < mn_number:
            raise ValueError(
                f"Cannot select {mn_number} HD-sEMG motor units from "
                f"{eligible_neurons.size} eligible units."
            )
        return rng.choice(eligible_neurons, size=mn_number, replace=False)


    def compute_fr(selected_neurons, data, t_start, t_end, column_spikes=1):
        """Compute steady-state firing rates for the selected motor units."""
        window_duration = (t_end - t_start) / 1000  # s
        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        firing_rates = np.zeros(len(selected_neurons))
        i = 0
        for neuron in selected_neurons:
            n_spikes = np.sum(steady_data[:, 0] == neuron)
            fr = n_spikes / window_duration
            firing_rates[i] = fr
            i = i + 1
        return firing_rates


    def compute_mn_cv(spike_times, t_start):
        """Compute the interspike-interval mean and coefficient of variation."""
        ISI = np.diff(spike_times[spike_times > t_start])
        if len(ISI) > 3:
            ISI_SD = ISI.std(ddof=1)
            ISI_mean = ISI.mean()
            ISI_CV = ISI_SD / ISI_mean
        else:
            ISI_mean = 0
            ISI_CV = 1
        return ISI_CV, ISI_mean


    def compute_cv(selected_neurons, data, t_start, t_end, column_spikes=1):
        """Compute ISI statistics for each selected motor unit."""
        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        ISI_CV = np.zeros(len(selected_neurons))
        ISI_mean = np.zeros(len(selected_neurons))
        i = 0
        for neuron in selected_neurons:
            ISI_CV[i], ISI_mean[i] = compute_mn_cv(
                steady_data[steady_data[:, 0] == neuron, column_spikes], t_start=t_start
            )
            i = i + 1

        return ISI_CV, ISI_mean


    def plot_mn_fr(
        fr_data,
        conditions,
        pd,
        mode,
        jitter_seed=20260728,
    ):
        """Plot and export simulation-level firing-rate summaries."""
        os.makedirs("diabetes", exist_ok=True)
        jitter_rng = np.random.default_rng(jitter_seed)
        simulation_fr = fr_data["mn_rate_trial_mean"]
        simulation_isi_cv = fr_data["isi_cv_trial_mean"]
        simulation_mu_counts = fr_data["n_motor_units"]
        mean_fr = np.hstack(
            (
                np.mean(simulation_fr[conditions[0]]),
                np.mean(simulation_fr[conditions[1]]),
            )
        )
        sd_fr = np.hstack(
            (
                simulation_fr[conditions[0]].std(ddof=1),
                simulation_fr[conditions[1]].std(ddof=1),
            )
        )

        fig, ax = plt.subplots()
        ax.errorbar([1, 2], mean_fr, fmt=".", yerr=sd_fr, capsize=5, color="black")
        # ax.grid()
        ax.scatter(
            1 + 0.1 * jitter_rng.normal(size=len(simulation_fr[conditions[0]])),
            simulation_fr[conditions[0]],
        )
        ax.scatter(
            2 + 0.1 * jitter_rng.normal(size=len(simulation_fr[conditions[1]])),
            simulation_fr[conditions[1]],
        )
        ax.set_xticks([1, 2])
        ax.set_xticklabels([conditions[0], conditions[1]])
        ax.set_ylabel("Mean MU firing rate per simulated subject (pps)")
        fig.tight_layout()
        fig.savefig(f"diabetes/mn_firing_rate_comparison_{mode}_v2.png")
        plt.close(fig)
        # Export one observation per simulation/subject.
        for cond in conditions:
            df = pd.DataFrame(
                {
                    "simulation_id": fr_data["simulation_ids"][cond],
                    "mean_firing_rate": simulation_fr[cond],
                    "mean_ISI_CV": simulation_isi_cv[cond],
                    "n_motor_units": simulation_mu_counts[cond],
                }
            )
            df.to_csv(f"diabetes/mn_firing_rate_{cond}_{mode}_v2.csv", index=False)

        df_mean = pd.DataFrame(
            {
                "condition": conditions,
                "n_simulations": [len(simulation_fr[cond]) for cond in conditions],
                "mean_firing_rate": mean_fr,
                "sd_firing_rate": sd_fr,
            }
        )
        df_mean.to_csv(f"diabetes/mn_firing_rate_summary_{mode}_v2.csv", index=False)


    def calculate_fr_data(
        trials,
        mode,
        pd,
        force_level,
        conditions_param,
        path_param,
        batch_name_param,
        t_start_param,
        t_end_param,
        criteria=criteria,
        mn_number=mn_number,
        selection_seed=None,
    ):
        """Calculate firing-rate and ISI statistics for one selection mode."""

        if mode == "hdsemg" and selection_seed is None:
            raise ValueError(f"selection_seed is required for mode '{mode}'.")
        selection_rng = np.random.default_rng(selection_seed) if mode == "hdsemg" else None

        mn_rate_mean_mean = {}
        mn_rate_mean_CV = {}
        mn_rate_trial_mean = {}
        isi_cv_trial_mean = {}
        simulation_ids = {}
        n_motor_units = {}
        for condition in conditions_param:
            mn_rate_mean_mean[condition] = np.array([]).reshape(-1, 1)
            mn_rate_mean_CV[condition] = np.array([]).reshape(-1, 1)
            mn_rate_trial_mean[condition] = []
            isi_cv_trial_mean[condition] = []
            simulation_ids[condition] = []
            n_motor_units[condition] = []

        force_mean = 0
        CV_mean = 0
        n = 0

        for trial in trials:
            for condition in conditions_param:
                data = pd.read_csv(
                    f"{path_param}spikedata_{condition}_{trial}_{batch_name_param}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )
                force = pd.read_csv(
                    f"{path_param}force_{condition}_{trial}_{batch_name_param}/force_ref{force_level}.csv",
                    delimiter=",",
                ).values
                data = data.values

                if condition == "DPN":
                    force = force[force[:, 0] > t_start_param, 1]
                    force_mean = force_mean + force
                    CV_mean = CV_mean + force.std(ddof=1) / force.mean()
                    n = n + 1

                # Select motor units according to the requested mode.
                if mode == "hdsemg":
                    selected_neurons = select_mns_hdemg(
                        data,
                        t_start=t_start_param,
                        t_end=t_end_param,
                        criteria=criteria,
                        mn_number=mn_number,
                        rng=selection_rng,
                    )
                elif mode == "all":
                    selected_neurons = np.unique(data[:, 0]).astype(int)
                else:
                    raise ValueError(f"Mode '{mode}' not recognized.")

                mns_rate_mean = compute_fr(
                    selected_neurons, data, t_start_param, t_end_param
                )
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start_param, t_end_param)
                ISI_CV = ISI_CV[mns_rate_mean >= 0.01].reshape(-1, 1)
                mns_rate_mean = mns_rate_mean[mns_rate_mean >= 0.01].reshape(-1, 1)
                mn_rate_trial_mean[condition].append(
                    float(mns_rate_mean.mean()) if mns_rate_mean.size else np.nan
                )
                isi_cv_trial_mean[condition].append(
                    float(ISI_CV.mean()) if ISI_CV.size else np.nan
                )
                simulation_ids[condition].append(int(trial))
                n_motor_units[condition].append(int(mns_rate_mean.size))
                mn_rate_mean_mean[condition] = np.vstack(
                    (mn_rate_mean_mean[condition], mns_rate_mean)
                )
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))

        return {
            "mn_rate_mean_mean": mn_rate_mean_mean,
            "mn_rate_mean_CV": mn_rate_mean_CV,
            "mn_rate_trial_mean": {
                condition: np.asarray(values, dtype=float)
                for condition, values in mn_rate_trial_mean.items()
            },
            "isi_cv_trial_mean": {
                condition: np.asarray(values, dtype=float)
                for condition, values in isi_cv_trial_mean.items()
            },
            "simulation_ids": {
                condition: np.asarray(values, dtype=int)
                for condition, values in simulation_ids.items()
            },
            "n_motor_units": {
                condition: np.asarray(values, dtype=int)
                for condition, values in n_motor_units.items()
            },
            "selection_seed": selection_seed,
            "force_mean": force_mean / n if n > 0 else 0,
            "CV_mean": CV_mean / n if n > 0 else 0,
        }


    def configure_primary_fr_axis(ax, tick_fontsize):
        """Set Figure 2's vertical display and return its bracket height."""
        ticks = [8, 10, 12, 14, 16]
        ax.set_ylim(8, 16)
        ax.set_yticks(ticks)
        ax.set_yticklabels(ticks, fontsize=tick_fontsize)
        return 15


    def add_primary_fr_summaries(
        ax,
        mean_fr,
        yerr,
        truth_mean_fr,
        normal_jitter,
        truth_line_width,
        mean_marker_size=8,
    ):
        """Add visually distinct HD-sEMG and simulation-truth summaries."""
        estimate_handle = ax.errorbar(
            [1, 2],
            mean_fr,
            marker="o",
            linestyle="",
            color="red",
            markersize=mean_marker_size,
            markeredgewidth=2,
            yerr=yerr,
            capsize=5,
            barsabove=True,
            zorder=6,
        )
        truth_handle = ax.hlines(
            truth_mean_fr,
            xmin=[normal_jitter.min(), 2 - truth_line_width / 2],
            xmax=[normal_jitter.max(), 2 + truth_line_width / 2],
            colors="green",
            linewidths=3,
            zorder=5,
        )
        return estimate_handle, truth_handle


    def add_primary_fr_significance(ax, p_value, significance_y):
        """Add the red significance annotation for the HD-sEMG comparison."""
        if p_value >= 0.05:
            return (), None

        bracket_lines = (
            ax.plot(
                [1, 2],
                [significance_y, significance_y],
                color="red",
                linewidth=2,
            )[0],
            ax.plot(
                [1, 1],
                [significance_y - 0.5, significance_y],
                color="red",
                linewidth=2,
            )[0],
            ax.plot(
                [2, 2],
                [significance_y - 0.5, significance_y],
                color="red",
                linewidth=2,
            )[0],
        )
        significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*"
        significance_text = ax.text(
            1.5,
            significance_y + 0.1,
            significance,
            color="red",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize="xx-large",
        )
        return bracket_lines, significance_text


    def plot_mn_fr_combined_data(data_hdemg, data_truth, conditions, pd):
        """Plot randomized HD-sEMG estimates against the all-MU simulation truth."""
        os.makedirs("diabetes/figures", exist_ok=True)
        os.makedirs("diabetes/csv_results", exist_ok=True)

        for condition in conditions:
            if not np.array_equal(
                data_hdemg["simulation_ids"][condition],
                data_truth["simulation_ids"][condition],
            ):
                raise ValueError(f"HD-sEMG and simulation-truth IDs differ for {condition}.")

        bootstrap_hdemg = bootstrap_mode(
            data_hdemg,
            "HD-sEMG",
            bootstrap_seeds["HD-sEMG"],
            n_resamples,
        )
        isi_cv_hdemg = bootstrap_isi_cv(
            data_hdemg,
            "HD-sEMG",
            bootstrap_seeds["HD-sEMG"],
            n_resamples,
        )
        bootstrap_truth = bootstrap_mode(
            data_truth,
            "Simulation truth (all motor units)",
            bootstrap_seeds["All motor units"],
            n_resamples,
        )

        simulation_rates = data_hdemg["mn_rate_trial_mean"]
        mean_fr = np.asarray(
            [bootstrap_hdemg["normal_mean_pps"], bootstrap_hdemg["DPN_mean_pps"]]
        )
        confidence_intervals = np.asarray(
            [
                [bootstrap_hdemg["normal_ci_low"], bootstrap_hdemg["normal_ci_high"]],
                [bootstrap_hdemg["DPN_ci_low"], bootstrap_hdemg["DPN_ci_high"]],
            ]
        )
        yerr = np.vstack(
            (
                mean_fr - confidence_intervals[:, 0],
                confidence_intervals[:, 1] - mean_fr,
            )
        )
        truth_mean_fr = np.asarray(
            [bootstrap_truth["normal_mean_pps"], bootstrap_truth["DPN_mean_pps"]]
        )

        jitter_rng = np.random.default_rng(bootstrap_seeds["HD-sEMG"] + 10_000)
        normal_jitter = 1 + 0.1 * jitter_rng.normal(
            size=simulation_rates[conditions[0]].size
        )
        dpn_jitter = 2 + 0.1 * jitter_rng.normal(size=simulation_rates[conditions[1]].size)
        truth_line_width = float(np.ptp(normal_jitter))

        fig, ax = plt.subplots(figsize=(7, 6))
        significance_y = configure_primary_fr_axis(ax, fs_ticklabels)
        ax.scatter(
            normal_jitter,
            simulation_rates[conditions[0]].ravel(),
            alpha=0.6,
            color=color[conditions[0]],
        )
        ax.scatter(
            dpn_jitter,
            simulation_rates[conditions[1]].ravel(),
            alpha=0.6,
            color=color[conditions[0]],
        )
        estimate_handle, truth_handle = add_primary_fr_summaries(
            ax,
            mean_fr,
            yerr,
            truth_mean_fr,
            normal_jitter,
            truth_line_width,
        )

        p_value = bootstrap_hdemg["p_value"]
        add_primary_fr_significance(ax, p_value, significance_y)

        ax.set_xticks([1, 2])
        ax.set_xticklabels(
            [
                cond.replace("_", " ").title() if cond != "DPN" else "DPN"
                for cond in conditions
            ],
            fontsize=fs_ticklabels,
        )
        ax.set_ylabel(
            "Mean MU firing rate per simulated subject (pps)",
            fontsize=fs_label,
        )
        ax.set_title(f"{modes[0]} mode", fontsize=fs_title)
        ax.legend(
            handles=[estimate_handle, truth_handle],
            labels=[
                "HD-sEMG mean (95% BCa CI)",
                "Mean simulation truth (all MUs)",
            ],
            loc="lower center",
            frameon=False,
            fontsize=fs_ticklabels,
        )
        fig.tight_layout()

        figure_path = "diabetes/figures/mn_firing_rate_comparison_combined_v2.png"
        fig.savefig(figure_path, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        for condition in conditions:
            pd.DataFrame(
                {
                    "simulation_id": data_hdemg["simulation_ids"][condition],
                    "mean_firing_rate": data_hdemg["mn_rate_trial_mean"][condition],
                    "mean_ISI_CV": data_hdemg["isi_cv_trial_mean"][condition],
                    "n_motor_units": data_hdemg["n_motor_units"][condition],
                }
            ).to_csv(
                f"diabetes/csv_results/mn_firing_rate_{condition}_hdsemg_v2.csv",
                index=False,
            )

        summary = {
            "comparison": "normal_vs_DPN",
            "unit_of_analysis": "simulation/subject",
            "test": "paired Wilcoxon signed-rank",
            "hdsemg_selection_seed": data_hdemg["selection_seed"],
            "bootstrap_seed": bootstrap_seeds["HD-sEMG"],
            "n_resamples": n_resamples,
            "n_simulations": bootstrap_hdemg["n_simulations"],
            "wilcoxon_statistic": bootstrap_hdemg["wilcoxon_statistic"],
            "p_value": bootstrap_hdemg["p_value"],
            "mean_difference": bootstrap_hdemg["DPN_minus_normal_pps"],
            "ci_low": bootstrap_hdemg["difference_ci_low"],
            "ci_high": bootstrap_hdemg["difference_ci_high"],
            "isi_cv_wilcoxon_statistic": isi_cv_hdemg["wilcoxon_statistic"],
            "isi_cv_p_value": isi_cv_hdemg["p_value"],
            "isi_cv_mean_difference": isi_cv_hdemg["DPN_minus_normal"],
            "isi_cv_ci_low": isi_cv_hdemg["difference_ci_low"],
            "isi_cv_ci_high": isi_cv_hdemg["difference_ci_high"],
        }
        for prefix, result in (
            ("hdsemg", bootstrap_hdemg),
            ("truth", bootstrap_truth),
        ):
            for key in (
                "normal_mean_pps",
                "normal_sd_pps",
                "normal_ci_low",
                "normal_ci_high",
                "DPN_mean_pps",
                "DPN_sd_pps",
                "DPN_ci_low",
                "DPN_ci_high",
                "DPN_minus_normal_pps",
                "difference_ci_low",
                "difference_ci_high",
                "wilcoxon_statistic",
                "p_value",
            ):
                summary[f"{prefix}_{key}"] = result[key]
        pd.DataFrame([summary]).to_csv(
            "diabetes/csv_results/mn_firing_rate_p_values_combined_v2.csv",
            index=False,
        )

        print(f"Primary comparison figure saved to: {figure_path}")
        print(
            "Statistical results saved to: "
            "diabetes/csv_results/mn_firing_rate_p_values_combined_v2.csv"
        )


    def print_statistics(
        fr_data,
        stats_module,
        mode="",
        seed=20260728,
    ):
        """Print simulation-level firing-rate and ISI-CoV statistics."""
        result = bootstrap_mode(fr_data, mode, seed, n_resamples, stats_module=stats_module)
        isi_cv_result = bootstrap_isi_cv(
            fr_data, mode, seed, n_resamples, stats_module=stats_module
        )
        print(
            f"FR simulation means (n={result['n_simulations']} paired "
            f"simulations/subjects): normal {result['normal_mean_pps']:.2f} ± "
            f"{result['normal_sd_pps']:.2f} "
            f"[95% BCa CI {result['normal_ci_low']:.2f}, "
            f"{result['normal_ci_high']:.2f}]; DPN {result['DPN_mean_pps']:.2f} ± "
            f"{result['DPN_sd_pps']:.2f} [95% BCa CI "
            f"{result['DPN_ci_low']:.2f}, {result['DPN_ci_high']:.2f}]"
        )
        print(
            f"Paired comparison ({result['mode']}): DPN - normal = "
            f"{result['DPN_minus_normal_pps']:.2f} pps "
            f"[95% BCa CI {result['difference_ci_low']:.2f}, "
            f"{result['difference_ci_high']:.2f}]; Wilcoxon signed-rank "
            f"W={result['wilcoxon_statistic']:.1f}, p={result['p_value']:.4e}"
        )
        print(
            f"ISI-CoV simulation means (n={isi_cv_result['n_simulations']} paired "
            f"simulations/subjects): normal {isi_cv_result['normal_mean']:.3f} ± "
            f"{isi_cv_result['normal_sd']:.3f} [95% BCa CI "
            f"{isi_cv_result['normal_ci_low']:.3f}, "
            f"{isi_cv_result['normal_ci_high']:.3f}]; DPN "
            f"{isi_cv_result['DPN_mean']:.3f} ± {isi_cv_result['DPN_sd']:.3f} "
            f"[95% BCa CI "
            f"{isi_cv_result['DPN_ci_low']:.3f}, "
            f"{isi_cv_result['DPN_ci_high']:.3f}]"
        )
        print(
            f"Paired ISI-CoV comparison ({isi_cv_result['mode']}): DPN - normal = "
            f"{isi_cv_result['DPN_minus_normal']:.3f} [95% BCa CI "
            f"{isi_cv_result['difference_ci_low']:.3f}, "
            f"{isi_cv_result['difference_ci_high']:.3f}]; Wilcoxon signed-rank "
            f"W={isi_cv_result['wilcoxon_statistic']:.1f}, "
            f"p={isi_cv_result['p_value']:.4e}"
        )
        mu_counts = fr_data["n_motor_units"]
        print(
            "Analyzed MUs per simulation/subject (mean ± SD [range]): "
            f"normal {mu_counts['normal'].mean():.1f} ± "
            f"{mu_counts['normal'].std(ddof=1):.1f} "
            f"[{mu_counts['normal'].min()}, {mu_counts['normal'].max()}]; DPN "
            f"{mu_counts['DPN'].mean():.1f} ± {mu_counts['DPN'].std(ddof=1):.1f} "
            f"[{mu_counts['DPN'].min()}, {mu_counts['DPN'].max()}]"
        )
        result["isi_cv"] = isi_cv_result
        return result


    def firing_rate(
        spiketrains,
        delta_t=0.00005,
        filter_order=4,
        cutoff_frequency=0.001,
        max_time=1000,
    ):
        """Create and low-pass filter a firing-rate impulse train."""

        # Create the time vector.
        t = np.arange(0, max_time, delta_t)
        fr = np.zeros_like(t)

        # Add a Dirac impulse at each motor-unit discharge time.
        idx = np.searchsorted(t, spiketrains / 1000)
        idx = idx[idx < len(fr)]
        fr[idx] = 1 / delta_t
        # Design the Butterworth low-pass filter.
        fs = 1 / delta_t
        b, a = butter(filter_order, cutoff_frequency / (fs / 2))

        # Filter the impulse train and clip numerical undershoot.
        fr = filtfilt(b, a, fr)
        fr[fr < 0] = 0
        return fr, t


    def bootstrap_mode(
        data, mode, seed=20260728, n_resamples=n_resamples, stats_module=stats
    ):
        """Estimate paired Normal-DPN firing-rate effects across subjects/simulations."""
        trial_means = data["mn_rate_trial_mean"]
        normal = np.asarray(trial_means["normal"], dtype=float).ravel()
        dpn = np.asarray(trial_means["DPN"], dtype=float).ravel()

        if normal.size != dpn.size:
            raise ValueError("Normal and DPN must contain the same number of simulations.")
        simulation_ids = data.get("simulation_ids")
        if simulation_ids is not None:
            normal_ids = np.asarray(simulation_ids["normal"], dtype=int).ravel()
            dpn_ids = np.asarray(simulation_ids["DPN"], dtype=int).ravel()
            if not np.array_equal(normal_ids, dpn_ids):
                raise ValueError("Normal and DPN simulation IDs must match in order.")

        valid_pairs = np.isfinite(normal) & np.isfinite(dpn)
        normal = normal[valid_pairs]
        dpn = dpn[valid_pairs]
        if normal.size < 2:
            raise ValueError(
                "At least two complete Normal-DPN simulation pairs are required."
            )

        def mean_statistic(sample, axis=-1):
            """Compute a sample mean along SciPy's resampling axis."""
            return np.mean(sample, axis=axis)

        def mean_difference(normal_sample, dpn_sample, axis=-1):
            """Compute the DPN-minus-Normal mean firing-rate difference."""
            return np.mean(dpn_sample, axis=axis) - np.mean(normal_sample, axis=axis)

        rng = np.random.default_rng(seed)
        bootstrap_options = {
            "n_resamples": n_resamples,
            "confidence_level": 0.95,
            "method": "BCa",
            "vectorized": True,
            "rng": rng,
        }
        normal_bootstrap = stats_module.bootstrap(
            (normal,), mean_statistic, **bootstrap_options
        )
        dpn_bootstrap = stats_module.bootstrap((dpn,), mean_statistic, **bootstrap_options)
        difference_bootstrap = stats_module.bootstrap(
            (normal, dpn),
            mean_difference,
            paired=True,
            **bootstrap_options,
        )

        paired_differences = dpn - normal
        if np.allclose(paired_differences, 0):
            wilcoxon_statistic = 0.0
            p_value = 1.0
        else:
            wilcoxon_result = stats_module.wilcoxon(
                normal,
                dpn,
                alternative="two-sided",
                method="auto",
            )
            wilcoxon_statistic = float(wilcoxon_result.statistic)
            p_value = float(wilcoxon_result.pvalue)

        result = {
            "mode": mode,
            "unit_of_analysis": "simulation/subject",
            "selection_seed": data.get("selection_seed"),
            "bootstrap_seed": seed,
            "n_resamples": int(n_resamples),
            "n_simulations": int(normal.size),
            "normal_mean_pps": float(normal.mean()),
            "normal_sd_pps": float(normal.std(ddof=1)),
            "normal_ci_low": float(normal_bootstrap.confidence_interval.low),
            "normal_ci_high": float(normal_bootstrap.confidence_interval.high),
            "DPN_mean_pps": float(dpn.mean()),
            "DPN_sd_pps": float(dpn.std(ddof=1)),
            "DPN_ci_low": float(dpn_bootstrap.confidence_interval.low),
            "DPN_ci_high": float(dpn_bootstrap.confidence_interval.high),
            "DPN_minus_normal_pps": float(paired_differences.mean()),
            "difference_ci_low": float(difference_bootstrap.confidence_interval.low),
            "difference_ci_high": float(difference_bootstrap.confidence_interval.high),
            "wilcoxon_statistic": wilcoxon_statistic,
            "p_value": p_value,
        }
        return result


    def bootstrap_isi_cv(
        data, mode, seed=20260728, n_resamples=n_resamples, stats_module=stats
    ):
        """Estimate paired Normal-DPN effects on simulation-level mean ISI-CoV."""
        isi_data = {
            "mn_rate_trial_mean": data["isi_cv_trial_mean"],
            "simulation_ids": data.get("simulation_ids"),
            "selection_seed": data.get("selection_seed"),
        }
        result = bootstrap_mode(
            isi_data,
            mode,
            seed=seed,
            n_resamples=n_resamples,
            stats_module=stats_module,
        )
        return {
            "mode": mode,
            "unit_of_analysis": result["unit_of_analysis"],
            "selection_seed": result["selection_seed"],
            "bootstrap_seed": result["bootstrap_seed"],
            "n_resamples": result["n_resamples"],
            "n_simulations": result["n_simulations"],
            "normal_mean": result["normal_mean_pps"],
            "normal_sd": result["normal_sd_pps"],
            "normal_ci_low": result["normal_ci_low"],
            "normal_ci_high": result["normal_ci_high"],
            "DPN_mean": result["DPN_mean_pps"],
            "DPN_sd": result["DPN_sd_pps"],
            "DPN_ci_low": result["DPN_ci_low"],
            "DPN_ci_high": result["DPN_ci_high"],
            "DPN_minus_normal": result["DPN_minus_normal_pps"],
            "difference_ci_low": result["difference_ci_low"],
            "difference_ci_high": result["difference_ci_high"],
            "wilcoxon_statistic": result["wilcoxon_statistic"],
            "p_value": result["p_value"],
        }
    return (
        calculate_fr_data,
        compute_cv,
        compute_fr,
        plot_mn_fr_combined_data,
        print_statistics,
        select_mns_hdemg,
        select_mns_randomly,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## All-active-MU simulation truth

    For each simulated subject, the mean firing rate across every active motor unit is known exactly and defines the trial-specific simulation truth. This full-population value is the sole reference for the sampled HD-sEMG estimate.
    """)
    return


@app.cell
def _(
    batch_name,
    bootstrap_seeds,
    calculate_fr_data,
    conditions,
    path,
    pd,
    print_statistics,
    stats,
    t_end,
    t_start,
    trials,
):
    # Calculate the trial-specific simulation truth from every active motor unit.
    print("=" * 60)
    print("=== SIMULATION TRUTH (all motor units) ===")
    print("=" * 60)

    force_level = 20
    data_truth = calculate_fr_data(
        trials,
        "all",
        pd,
        force_level,
        conditions,
        path,
        batch_name,
        t_start,
        t_end,
    )
    result_truth = print_statistics(
        data_truth,
        stats,
        mode="Simulation truth (all motor units)",
        seed=bootstrap_seeds["All motor units"],
    )
    return data_truth, result_truth


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Firing rates at 20% MVC

    Each simulation represents one subject. Group means, SDs, confidence intervals, and tests for firing rate and ISI-CoV therefore use one mean per simulation; raw motor-unit values are retained only for explicitly descriptive analyses.
    In the HD-sEMG mode, 10 unique motor units are drawn without replacement from those meeting the firing-rate and ISI-CoV eligibility criteria, using the configured fixed seed. Red horizontal lines show the condition means of the subject-specific simulation truths calculated from all active MUs.
    """)
    return


@app.cell
def _(
    batch_name,
    bootstrap_seeds,
    calculate_fr_data,
    conditions,
    criteria,
    data_truth,
    mn_number,
    path,
    pd,
    plot_mn_fr_combined_data,
    print_statistics,
    selection_seeds,
    stats,
    t_end,
    t_start,
    trials,
):
    data_hdemg = calculate_fr_data(
        trials,
        "hdsemg",
        pd,
        20,
        conditions,
        path,
        batch_name,
        t_start,
        t_end,
        criteria=criteria,
        mn_number=mn_number,
        selection_seed=selection_seeds["hdsemg"],
    )
    print("=" * 60)
    print("=== HD-sEMG MODE (seeded random selection) ===")
    print("=" * 60)
    print(f"Selection criteria: {criteria}")
    print(f"Motor units per simulation: {mn_number}")
    print(f"Selection seed: {selection_seeds['hdsemg']}")
    result_hdemg = print_statistics(
        data_hdemg,
        stats,
        mode="HD-sEMG",
        seed=bootstrap_seeds["HD-sEMG"],
    )
    plot_mn_fr_combined_data(data_hdemg, data_truth, conditions, pd)
    return data_hdemg, result_hdemg


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Force-production statistics

    Each simulation represents one subject and contributes one steady-state mean force and force coefficient of variation (CoV) per group. Normal–DPN estimates use paired simulation IDs, with 95% BCa bootstrap intervals and two-sided Wilcoxon signed-rank p-values.
    """)
    return


@app.cell
def _(
    batch_name,
    conditions,
    n_resamples,
    np,
    path,
    pd,
    stats,
    t_start,
    trials,
):
    def bootstrap_mean_ci(values, seed, n_resamples):
        """Return a BCa 95% confidence interval for a sample mean."""
        values = np.asarray(values, dtype=float)
        values = values[np.isfinite(values)]
        if values.size < 2:
            return (np.nan, np.nan)

        point_estimate = float(values.mean())
        if np.allclose(values, values[0]):
            return (point_estimate, point_estimate)

        result = stats.bootstrap(
            (values,),
            np.mean,
            n_resamples=n_resamples,
            confidence_level=0.95,
            method="BCa",
            vectorized=True,
            rng=np.random.default_rng(seed),
        )
        return (
            float(result.confidence_interval.low),
            float(result.confidence_interval.high),
        )


    def paired_bootstrap_summary(first, second, seed, n_resamples):
        """Summarize paired samples with bootstrap intervals and Wilcoxon p-values."""
        first = np.asarray(first, dtype=float)
        second = np.asarray(second, dtype=float)
        if first.size != second.size:
            raise ValueError("Paired samples must have the same length.")

        valid_pairs = np.isfinite(first) & np.isfinite(second)
        first = first[valid_pairs]
        second = second[valid_pairs]
        if first.size < 2:
            raise ValueError("At least two complete simulation pairs are required.")

        difference = second - first
        first_ci = bootstrap_mean_ci(first, seed, n_resamples)
        second_ci = bootstrap_mean_ci(second, seed + 1, n_resamples)

        if np.allclose(difference, difference[0]):
            difference_ci = (float(difference.mean()), float(difference.mean()))
        else:
            difference_result = stats.bootstrap(
                (first, second),
                lambda first_sample, second_sample, axis=-1: (
                    np.mean(second_sample, axis=axis) - np.mean(first_sample, axis=axis)
                ),
                paired=True,
                n_resamples=n_resamples,
                confidence_level=0.95,
                method="BCa",
                vectorized=True,
                rng=np.random.default_rng(seed + 2),
            )
            difference_ci = (
                float(difference_result.confidence_interval.low),
                float(difference_result.confidence_interval.high),
            )

        if np.allclose(difference, 0):
            wilcoxon_statistic = 0.0
            p_value = 1.0
        else:
            wilcoxon_result = stats.wilcoxon(
                first,
                second,
                alternative="two-sided",
                method="auto",
            )
            wilcoxon_statistic = float(wilcoxon_result.statistic)
            p_value = float(wilcoxon_result.pvalue)

        return {
            "n_resamples": int(n_resamples),
            "n_pairs": int(first.size),
            "first": {
                "mean": float(first.mean()),
                "sd": float(first.std(ddof=1)),
                "ci": first_ci,
            },
            "second": {
                "mean": float(second.mean()),
                "sd": float(second.std(ddof=1)),
                "ci": second_ci,
            },
            "difference": float(difference.mean()),
            "difference_ci": difference_ci,
            "wilcoxon_statistic": wilcoxon_statistic,
            "p_value": p_value,
        }


    def compute_force_statistics(
        trials_param,
        batch_name_param,
        force_level,
        conditions_param,
        path_param,
        t_start_param,
        MVC=300,
    ):
        """Calculate steady-state force statistics while retaining trial IDs."""
        results = {}
        for condition in conditions_param:
            trial_statistics = {}
            for trial in trials_param:
                try:
                    force_df = pd.read_csv(
                        f"{path_param}force_{condition}_{trial}_{batch_name_param}/force_ref{force_level}.csv",
                        delimiter=",",
                    )
                    force_vals = force_df.values
                    # Select steady-state: after t_start (in ms)
                    steady = force_vals[force_vals[:, 0] > t_start_param]
                    force_steady = steady[:, 1]
                    if force_steady.size == 0:
                        raise ValueError("steady-state force data are empty")

                    mean_f = float(force_steady.mean())
                    if not np.isfinite(mean_f) or mean_f <= 0:
                        raise ValueError("mean steady-state force must be positive")
                    cv_f = float(force_steady.std(ddof=1) / mean_f)
                    if not np.isfinite(cv_f):
                        raise ValueError("force CoV is not finite")

                    trial_statistics[int(trial)] = {
                        "mean_force": mean_f,
                        "force_cv": cv_f,
                    }
                except (OSError, ValueError, IndexError) as exc:
                    print(f"Skipping {condition} trial {trial}: {exc}")
                    continue

            trial_ids = np.asarray(sorted(trial_statistics), dtype=int)
            trial_means = np.asarray(
                [trial_statistics[trial]["mean_force"] for trial in trial_ids]
            )
            trial_cvs = np.asarray(
                [trial_statistics[trial]["force_cv"] for trial in trial_ids]
            )

            results[condition] = {
                "trial_statistics": trial_statistics,
                "trial_ids": trial_ids,
                "trial_means": trial_means,
                "trial_cvs": trial_cvs,
                "n_trials": int(trial_ids.size),
                "MVC": MVC,
            }
        return results


    def print_force_stats(
        results,
        conditions_param,
        label="",
        seed=20260728,
        n_resamples_param=n_resamples,
    ):
        """Print paired bootstrap and Wilcoxon summaries for force outcomes."""
        print(f"\n{'=' * 60}")
        print(f"=== FORCE PRODUCTION STATISTICS {label} ===")
        print(f"{'=' * 60}")
        print(f"(Steady-state: t > {t_start} ms)")
        print(f"(Bootstrap resamples: {n_resamples_param:,})")

        first_condition, second_condition = conditions_param
        first_trials = results[first_condition]["trial_statistics"]
        second_trials = results[second_condition]["trial_statistics"]
        common_trial_ids = sorted(set(first_trials) & set(second_trials))
        first_only = sorted(set(first_trials) - set(second_trials))
        second_only = sorted(set(second_trials) - set(first_trials))
        if first_only:
            print(f"Unpaired {first_condition} trial IDs excluded: {first_only}")
        if second_only:
            print(f"Unpaired {second_condition} trial IDs excluded: {second_only}")
        if len(common_trial_ids) < 2:
            print("Paired inference skipped: fewer than two common simulations.")
            return None

        first_force = [first_trials[trial]["mean_force"] for trial in common_trial_ids]
        second_force = [second_trials[trial]["mean_force"] for trial in common_trial_ids]
        first_cv = [first_trials[trial]["force_cv"] for trial in common_trial_ids]
        second_cv = [second_trials[trial]["force_cv"] for trial in common_trial_ids]

        force_summary = paired_bootstrap_summary(
            first_force, second_force, seed, n_resamples_param
        )
        cv_summary = paired_bootstrap_summary(
            first_cv, second_cv, seed + 100, n_resamples_param
        )
        group_keys = {first_condition: "first", second_condition: "second"}

        for condition in conditions_param:
            group_key = group_keys[condition]
            force_group = force_summary[group_key]
            cv_group = cv_summary[group_key]
            available_trials = results[condition]["n_trials"]
            print(
                f"\n--- {condition} (n={force_summary['n_pairs']} paired "
                f"simulations/subjects; {available_trials} available) ---"
            )
            print(
                f"  Mean force: {force_group['mean']:.4f} ± {force_group['sd']:.4f} "
                f"[95% BCa CI: {force_group['ci'][0]:.4f}, "
                f"{force_group['ci'][1]:.4f}]"
            )
            print(
                f"  Force as %MVC: "
                f"{force_group['mean'] / results[condition]['MVC'] * 100:.2f}%"
            )
            print(
                f"  CoV of force: {cv_group['mean']:.4f} ± {cv_group['sd']:.4f} "
                f"[95% BCa CI: {cv_group['ci'][0]:.4f}, "
                f"{cv_group['ci'][1]:.4f}]"
            )

        difference_label = f"{second_condition} - {first_condition}"
        print(f"\n--- Paired comparison ({difference_label}) ---")
        print(
            f"  Mean-force difference: {force_summary['difference']:.4f} "
            f"[95% BCa CI: {force_summary['difference_ci'][0]:.4f}, "
            f"{force_summary['difference_ci'][1]:.4f}]; paired Wilcoxon "
            f"W={force_summary['wilcoxon_statistic']:.1f}, "
            f"p={force_summary['p_value']:.4e}"
        )
        print(
            f"  Force-CoV difference: {cv_summary['difference']:.4f} "
            f"[95% BCa CI: {cv_summary['difference_ci'][0]:.4f}, "
            f"{cv_summary['difference_ci'][1]:.4f}]; paired Wilcoxon "
            f"W={cv_summary['wilcoxon_statistic']:.1f}, "
            f"p={cv_summary['p_value']:.4e}"
        )

        # Between-subject variability (one simulation per subject).
        print("\n--- Between-simulation/subject variability ---")
        for condition in conditions_param:
            group_key = group_keys[condition]
            force_group = force_summary[group_key]
            cv_group = cv_summary[group_key]
            cv_between_trials_force = (
                force_group["sd"] / force_group["mean"] * 100
                if force_group["mean"] > 0
                else np.nan
            )
            cv_between_trials_cv = (
                cv_group["sd"] / cv_group["mean"] * 100 if cv_group["mean"] > 0 else np.nan
            )
            print(
                f"  {condition}: CoV of mean force across simulations/subjects = "
                f"{cv_between_trials_force:.2f}%"
            )
            print(
                f"  {condition}: CoV of force CoV across simulations/subjects = "
                f"{cv_between_trials_cv:.2f}%"
            )

        return {
            "common_trial_ids": common_trial_ids,
            "mean_force": force_summary,
            "force_cv": cv_summary,
        }


    # === 20% MVC (main batch) ===
    force_level_20 = 20
    try:
        results_20 = compute_force_statistics(
            trials, batch_name, force_level_20, conditions, path, t_start, MVC=300
        )
        print_force_stats(
            results_20,
            conditions,
            label="(20% MVC, batch: variability)",
            seed=20260720,
        )
    except Exception as e:
        print(f"20% MVC force data error: {e}")

    # === 10% MVC ===
    _mvc10_trials = np.arange(50)
    _force_level_10 = 10
    try:
        _results_10 = compute_force_statistics(
            _mvc10_trials, "mvc10", _force_level_10, conditions, path, t_start, MVC=300
        )
        print_force_stats(
            _results_10,
            conditions,
            label="(10% MVC, batch: mvc10)",
            seed=20260710,
        )
    except Exception as e:
        print(f"10% MVC force data not yet available: {e}")

    # === 50% MVC ===
    _mvc50_trials = np.arange(50)
    _force_level_50 = 50
    try:
        _results_50 = compute_force_statistics(
            _mvc50_trials, "mvc50", _force_level_50, conditions, path, t_start, MVC=300
        )
        print_force_stats(
            _results_50,
            conditions,
            label="(50% MVC, batch: mvc50)",
            seed=20260750,
        )
    except Exception as e:
        print(f"50% MVC force data not yet available: {e}")
    return (paired_bootstrap_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Firing-rate and ISI-variability relationship

    This scatterplot is an explicitly descriptive motor-unit-level view; it is not used for group-level inference.
    """)
    return


@app.cell
def _(
    MaxNLocator,
    batch_name,
    compute_cv,
    compute_fr,
    conditions,
    fs_label,
    fs_legend,
    fs_ticklabels,
    np,
    path,
    pd,
    plt,
    select_mns_randomly,
    selection_seeds,
    t_end,
    t_start,
):
    def fr_cv(trials, pd=pd, selection_seed=selection_seeds["fr_cv"]):
        """Plot firing rate against ISI variability for randomly selected units."""
        import os

        force_level = 20
        selection_rng = np.random.default_rng(selection_seed)

        mn_rate_mean_mean = {condition: np.empty((0, 1)) for condition in conditions}
        mn_rate_mean_CV = {condition: np.empty((0, 1)) for condition in conditions}
        colormap = {conditions[0]: "Blues", conditions[1]: "Oranges"}
        neurons_index = {condition: np.empty((0, 1)) for condition in conditions}

        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )

                data = data.values

                selected_neurons = select_mns_randomly(
                    data,
                    t_start=t_start,
                    t_end=t_end,
                    size=100,
                    rng=selection_rng,
                )
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)
                ISI_CV = ISI_CV[mns_rate_mean >= 0.01].reshape(-1, 1)
                selected_neurons = selected_neurons[mns_rate_mean >= 0.01].reshape(-1, 1)

                mns_rate_mean = mns_rate_mean[mns_rate_mean >= 0.01].reshape(-1, 1)
                mn_rate_mean_mean[condition] = np.vstack(
                    (mn_rate_mean_mean[condition], mns_rate_mean)
                )
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))
                neurons_index[condition] = np.vstack(
                    (neurons_index[condition], selected_neurons.reshape(-1, 1))
                )

        neurons_index[conditions[0]][neurons_index[conditions[0]] > 120] = 250
        neurons_index[conditions[1]][neurons_index[conditions[1]] > 120] = 250

        neurons_index[conditions[0]][
            (neurons_index[conditions[0]] <= 120) & (neurons_index[conditions[0]] > 60)
        ] = 100
        neurons_index[conditions[1]][
            (neurons_index[conditions[1]] <= 120) & (neurons_index[conditions[1]] > 60)
        ] = 100

        neurons_index[conditions[0]][(neurons_index[conditions[0]] < 60)] = 10
        neurons_index[conditions[1]][(neurons_index[conditions[1]] < 60)] = 10

        fig, ax = plt.subplots(figsize=(12, 8))
        # Main scatter plot.
        ax.scatter(
            mn_rate_mean_CV[conditions[0]],
            mn_rate_mean_mean[conditions[0]],
            c=neurons_index[conditions[0]],
            cmap=colormap[conditions[0]],
            vmin=1,
            vmax=250,
        )
        ax.scatter(
            mn_rate_mean_CV[conditions[1]],
            mn_rate_mean_mean[conditions[1]],
            c=neurons_index[conditions[1]],
            cmap=colormap[conditions[1]],
            vmin=1,
            vmax=250,
        )
        ax.set_xlim(0, 1.4)
        ax.set_ylim(0, 25)
        ax.set_xlabel("ISI-CoV", fontsize=fs_label)
        ax.set_ylabel("Mean firing rate (pps)", fontsize=fs_label)
        ax.tick_params(axis="both", labelsize=fs_ticklabels)
        # ax.grid(True, linestyle="--", alpha=0.7)
        # Legend with fixed colors (no patches)
        legend_labels = ["Normal", "DPN"]
        legend_colors = ["blue", "orange"]
        legend_handles = []
        for legend_color, label in zip(legend_colors, legend_labels):
            legend_handles.append(ax.scatter([], [], color=legend_color, label=label))
        ax.legend(
            handles=legend_handles,
            loc="upper left",
            bbox_to_anchor=(0.05, 0.95),
            fontsize=fs_legend,
        )
        # Detail inset.
        axins2 = fig.add_axes([0.58, 0.5, 0.3, 0.35])
        axins2.scatter(
            mn_rate_mean_CV[conditions[0]],
            mn_rate_mean_mean[conditions[0]],
            c=neurons_index[conditions[0]],
            cmap=colormap[conditions[0]],
            vmin=1,
            vmax=250,
        )
        axins2.scatter(
            mn_rate_mean_CV[conditions[1]],
            mn_rate_mean_mean[conditions[1]],
            c=neurons_index[conditions[1]],
            cmap=colormap[conditions[1]],
            vmin=1,
            vmax=250,
        )
        axins2.set_xlim(0.02, 0.12)
        axins2.set_ylim(12, 22)
        axins2.xaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.yaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.tick_params(axis="both", which="major", labelsize=fs_ticklabels - 2)
        # axins2.grid(True, linestyle="--", alpha=0.7)
        fig.savefig("diabetes/figures/fr_cv_scatter_full_v2.png", bbox_inches="tight")
        plt.show()
        # Export the plotted data.
        os.makedirs("diabetes", exist_ok=True)
        for cond in conditions:
            df = pd.DataFrame(
                {
                    "firing_rate": mn_rate_mean_mean[cond].flatten(),
                    "ISI_CV": mn_rate_mean_CV[cond].flatten(),
                    "neuron_index": neurons_index[cond].flatten(),
                }
            )
            df.to_csv(f"diabetes/csv_results/fr_cv_{cond}_v2.csv", index=False)
    return (fr_cv,)


@app.cell
def _(fr_cv, pd, trials):
    fr_cv(trials, pd=pd)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motor-unit selection visualizations
    """)
    return


@app.cell
def _(
    batch_name,
    conditions,
    criteria,
    fontweight,
    fs_label,
    fs_legend,
    fs_ticklabels,
    fs_title,
    mn_number,
    np,
    path,
    pd,
    plt,
    select_mns_hdemg,
    selection_seeds,
):
    def what_mn_selected(trial, criteria=criteria, mn_number=mn_number):
        """Visualize the fixed-seed randomized HD-sEMG selection for one trial."""
        import os

        force_level = 20
        t_start = 4000
        t_end = 10000

        selection_rng = np.random.default_rng(selection_seeds["hdsemg"])
        selected_trial_data = {}
        for current_trial in range(trial + 1):
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{current_trial}_{batch_name}/"
                    f"cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                ).values
                selected_neurons = select_mns_hdemg(
                    data,
                    t_start=t_start,
                    t_end=t_end,
                    criteria=criteria,
                    mn_number=mn_number,
                    rng=selection_rng,
                )
                if current_trial == trial:
                    selected_trial_data[condition] = (data, selected_neurons)

        # Create one raster panel per condition.
        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

        colors = {condition: "red" for condition in conditions}

        for i, condition in enumerate(conditions):
            data, selected_neurons = selected_trial_data[condition]

            ax = axes[i]

            # Plot all motor units in light gray.
            ax.plot(
                data[:, 1],
                data[:, 0],
                linestyle="",
                marker=".",
                color=[0.7, 0.7, 0.7],
                markersize=4,
                alpha=0.8,
            )

            # Highlight selected motor units.
            selected_indices = np.nonzero(np.in1d(data[:, 0], selected_neurons))[0]
            ax.plot(
                data[selected_indices, 1],
                data[selected_indices, 0],
                linestyle="",
                marker=".",
                color=colors[condition],
                markersize=6,
                alpha=1,
            )

            # Mark the beginning of the steady-state analysis interval.
            ax.axvline(
                x=4000,
                color="blue",
                linestyle="--",
                linewidth=2,
                alpha=0.8,
                label="Start of analysis (4000 ms)",
            )

            # Format the condition panel.
            ax.set_title(
                f"{condition.replace('_', ' ').title() if condition != 'DPN' else 'DPN'}",
                fontsize=fs_title,
                fontweight=fontweight,
            )
            ax.set_ylabel("Motor-unit ID", fontsize=fs_label)
            ax.tick_params(axis="both", labelsize=fs_ticklabels)
            # ax.grid(True, alpha=0.3)

            # Show the legend only once.
            if i == 0:
                ax.legend(loc="upper right", fontsize=fs_legend)

            # Display the complete simulation interval.
            ax.set_xlim(0, data[:, 1].max())

        # Share a single x-axis label.
        axes[-1].set_xlabel("Time (ms)", fontsize=fs_label)

        # Adjust and save the figure.
        fig.tight_layout()
        fig.subplots_adjust(top=0.93)

        os.makedirs("diabetes/figures", exist_ok=True)
        figure_path = f"diabetes/figures/what_mn_selected_combined_trial_{trial}_v2.png"
        fig.savefig(
            figure_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.show()
        plt.close(fig)

        print(f"Motor-unit selection figure saved to: {figure_path}")


    def index_mn_selected(criteria=criteria, mn_number=mn_number):
        """Export descriptive motor-unit ID ranges for the fixed-seed selection."""
        import os

        force_level = 20
        t_start = 4000
        t_end = 10000

        selection_rng = np.random.default_rng(selection_seeds["hdsemg"])
        min_index = {condition: np.inf for condition in conditions}
        max_index = {condition: -np.inf for condition in conditions}
        selection_records = []
        for trial in range(50):
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                ).values
                selected_neurons = select_mns_hdemg(
                    data,
                    t_start=t_start,
                    t_end=t_end,
                    criteria=criteria,
                    mn_number=mn_number,
                    rng=selection_rng,
                )
                min_index[condition] = min(min_index[condition], int(selected_neurons.min()))
                max_index[condition] = max(max_index[condition], int(selected_neurons.max()))
                sorted_ids = np.sort(selected_neurons.astype(int))
                selection_records.append(
                    {
                        "simulation_id": int(trial),
                        "condition": condition,
                        "selected_motor_unit_ids": ";".join(
                            str(unit_id) for unit_id in sorted_ids
                        ),
                        "minimum_id": int(sorted_ids.min()),
                        "maximum_id": int(sorted_ids.max()),
                        "id_span": int(sorted_ids.max() - sorted_ids.min()),
                    }
                )

        selection_frame = pd.DataFrame(selection_records)
        os.makedirs("diabetes/csv_results", exist_ok=True)
        selection_frame.to_csv(
            "diabetes/csv_results/hdsemg_selected_motor_units_v2.csv",
            index=False,
        )
        for condition in conditions:
            condition_spans = selection_frame.loc[
                selection_frame["condition"] == condition, "id_span"
            ].to_numpy(dtype=float)
            print(
                f"Condition {condition}: min index={int(min_index[condition])}, "
                f"max index={int(max_index[condition])}; mean ID span="
                f"{condition_spans.mean():.1f} ± {condition_spans.std(ddof=1):.1f}"
            )
        paired_spans = selection_frame.pivot(
            index="simulation_id", columns="condition", values="id_span"
        )
        print(
            "Paired subjects with larger DPN ID span: "
            f"{int((paired_spans['DPN'] > paired_spans['normal']).sum())}/"
            f"{paired_spans.shape[0]}"
        )
        print(
            "Selected-MU ID summary saved to: "
            "diabetes/csv_results/hdsemg_selected_motor_units_v2.csv"
        )
    return index_mn_selected, what_mn_selected


@app.cell
def _(what_mn_selected):
    what_mn_selected(30)
    return


@app.cell
def _(index_mn_selected):
    index_mn_selected()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ISI-variability distributions

    These histograms describe individual motor units pooled across simulations; they are not used for subject-level estimates or tests.
    """)
    return


@app.cell
def _(
    MaxNLocator,
    batch_name,
    compute_cv,
    conditions,
    fontweight,
    fs_label,
    fs_legend,
    fs_ticklabels,
    fs_title,
    np,
    path,
    pd,
    plt,
    t_end,
    t_start,
):
    def isi_cov_histograms(trials, pd=pd, batch_name=batch_name):
        """Plot ISI-variability distributions for all motor units."""
        import os

        os.makedirs("diabetes/figures", exist_ok=True)

        # Use the same condition colors as the firing-rate plots.
        colors = {
            conditions[0]: (0.0039, 0.451, 0.698),
            conditions[1]: (0.0078, 0.6196, 0.451),
        }

        # Collect ISI CoV values for all motor units, not only selected units.
        force_level = 20
        all_cov_data = {condition: [] for condition in conditions}

        for trial in trials:
            for condition in conditions:
                # Load motor-unit discharge times.
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )
                data = data.values

                # Compute ISI CoV for every motor unit without selection.
                all_neurons = np.unique(data[:, 0])
                ISI_CV, _ = compute_cv(all_neurons, data, t_start, t_end)

                # Retain valid CoV estimates.
                valid_mask = ISI_CV > 0
                valid_cov = ISI_CV[valid_mask]

                # Accumulate observations for this condition.
                all_cov_data[condition].extend(valid_cov)

        # Create one histogram per condition.
        fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12, 5))

        for i, condition in enumerate(conditions):
            ax = axes[i]

            # ISI CoV observations for this condition.
            cov_data = np.array(all_cov_data[condition])

            # Plot the distribution.
            n_bins = np.linspace(0, 1.0, 21)
            ax.hist(
                cov_data,
                bins=n_bins,
                alpha=0.7,
                color=colors[conditions[0]],
                edgecolor="black",
                linewidth=0.5,
            )
            ax.set_xlim(0, 1.0)

            # Shade the region that satisfies the selection threshold.
            ax.axvspan(0, 0.3, alpha=0.3, color=colors[conditions[1]], zorder=0)

            # Count motor units below the threshold.
            count_low_cov = np.sum(cov_data < 0.3)
            total_neurons = len(cov_data)

            # Annotate the count below the threshold.
            ax.text(
                0.45,
                0.9,
                f"CoV < 0.3: {count_low_cov}/{total_neurons}",
                transform=ax.transAxes,
                fontsize=fs_legend,
            )

            # Format the panel.
            ax.set_xlabel("ISI-CoV", fontsize=fs_label)
            if i == 0:
                ax.set_ylabel("Number of motor units", fontsize=fs_label)
            ax.set_title(
                f"{condition.replace('_', ' ').title() if condition != 'DPN' else 'DPN'}",
                fontsize=fs_title,
                fontweight=fontweight,
            )
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.tick_params(axis="both", labelsize=fs_ticklabels)
            # ax.grid(True, alpha=0.3)

            # Mark the selection threshold.
            ax.axvline(x=0.3, color="red", linestyle="--", alpha=0.8, linewidth=2)

        # Adjust and save the figure.
        fig.tight_layout()

        filename = f"diabetes/figures/isi_cov_histograms_all_units_{batch_name}_v2.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        print(f"ISI CoV histograms for all motor units saved to: {filename}")
    return (isi_cov_histograms,)


@app.cell
def _(isi_cov_histograms, trials):
    isi_cov_histograms(trials)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Robustness across contraction intensities

    The 20% MVC condition was designated as the primary reference analysis. The
    same simulation-level analysis was repeated at 10% and 50% MVC using 50
    paired simulated subjects per force level to assess whether the direction
    and magnitude of the findings were robust across contraction intensities.

    For firing rate and ISI-CoV, the analysis estimates the paired DPN-minus-Normal
    effect at each MVC, quantifies the difference between the randomized HD-sEMG
    estimate and the all-active-MU simulation truth, and tests force-level
    dependence using a within-subject Friedman test followed by all three paired
    MVC contrasts with Holm adjustment. Trial identifiers must match within each
    condition pair and across contraction intensities.
    """)
    return


@app.cell
def _(np):
    def paired_subject_effects(data, value_key, conditions_param):
        """Return aligned condition values and the subject-level DPN-Normal effect."""
        first_condition, second_condition = conditions_param
        values = data[value_key]
        simulation_ids = data["simulation_ids"]

        first = np.asarray(values[first_condition], dtype=float).ravel()
        second = np.asarray(values[second_condition], dtype=float).ravel()
        first_ids = np.asarray(simulation_ids[first_condition], dtype=int).ravel()
        second_ids = np.asarray(simulation_ids[second_condition], dtype=int).ravel()

        if first.size != first_ids.size or second.size != second_ids.size:
            raise ValueError("Each condition value must have one simulation ID.")
        if first.size != second.size:
            raise ValueError("Conditions must contain the same number of simulations.")
        if not np.array_equal(first_ids, second_ids):
            raise ValueError("Condition simulation IDs must match in order.")

        valid_pairs = np.isfinite(first) & np.isfinite(second)
        if valid_pairs.sum() < 2:
            raise ValueError("At least two complete subject pairs are required.")

        first = first[valid_pairs]
        second = second[valid_pairs]
        return {
            "simulation_ids": first_ids[valid_pairs],
            "first": first,
            "second": second,
            "effect": second - first,
        }


    def holm_adjust_pvalues(p_values):
        """Return Holm family-wise-error adjusted p-values in original order."""
        p_values = np.asarray(p_values, dtype=float)
        if p_values.ndim != 1 or p_values.size == 0:
            raise ValueError("p_values must be a non-empty one-dimensional sequence.")
        if np.any(~np.isfinite(p_values)) or np.any((p_values < 0) | (p_values > 1)):
            raise ValueError("p_values must be finite and between zero and one.")

        order = np.argsort(p_values)
        adjusted = np.empty_like(p_values)
        running_maximum = 0.0
        n_tests = int(p_values.size)
        for rank, original_index in enumerate(order):
            candidate = (n_tests - rank) * p_values[original_index]
            running_maximum = max(running_maximum, float(candidate))
            adjusted[original_index] = min(running_maximum, 1.0)
        return adjusted


    def summarize_force_level_dependence(
        effects_by_force,
        paired_summary,
        stats_module,
        holm_adjuster,
        seed,
        n_resamples,
        reference_force=20,
    ):
        """Test whether paired condition effects differ across MVC levels."""
        force_levels = sorted(int(force) for force in effects_by_force)
        if len(force_levels) < 3:
            raise ValueError("At least three MVC levels are required.")
        if reference_force not in force_levels:
            raise ValueError("The reference MVC must be present.")

        reference_ids = np.asarray(
            effects_by_force[reference_force]["simulation_ids"], dtype=int
        )
        for force_level in force_levels:
            force_ids = np.asarray(
                effects_by_force[force_level]["simulation_ids"], dtype=int
            )
            if not np.array_equal(reference_ids, force_ids):
                raise ValueError("Simulation IDs must match across MVC levels.")

        effect_arrays = [
            np.asarray(effects_by_force[force]["effect"], dtype=float)
            for force in force_levels
        ]
        if all(np.allclose(effect_arrays[0], values) for values in effect_arrays[1:]):
            friedman_statistic = 0.0
            friedman_p_value = 1.0
        else:
            friedman_result = stats_module.friedmanchisquare(*effect_arrays)
            friedman_statistic = float(friedman_result.statistic)
            friedman_p_value = float(friedman_result.pvalue)

        nonreference_forces = [force for force in force_levels if force != reference_force]
        comparison_pairs = [(reference_force, force) for force in nonreference_forces]
        for index, first_force in enumerate(nonreference_forces):
            for second_force in nonreference_forces[index + 1 :]:
                comparison_pairs.append((first_force, second_force))

        contrasts = []
        for comparison_index, (first_force, second_force) in enumerate(comparison_pairs):
            summary = paired_summary(
                effects_by_force[first_force]["effect"],
                effects_by_force[second_force]["effect"],
                seed + comparison_index * 10,
                n_resamples,
            )
            contrasts.append(
                {
                    "first_force_mvc": int(first_force),
                    "second_force_mvc": int(second_force),
                    "contrast_label": f"{second_force}_minus_{first_force}",
                    "n_pairs": int(summary["n_pairs"]),
                    "effect_contrast": float(summary["difference"]),
                    "contrast_ci_low": float(summary["difference_ci"][0]),
                    "contrast_ci_high": float(summary["difference_ci"][1]),
                    "wilcoxon_statistic": float(summary["wilcoxon_statistic"]),
                    "raw_p_value": float(summary["p_value"]),
                }
            )

        adjusted = holm_adjuster([contrast["raw_p_value"] for contrast in contrasts])
        for contrast, adjusted_p_value in zip(contrasts, adjusted):
            contrast["holm_adjusted_p_value"] = float(adjusted_p_value)

        return {
            "n_subjects": int(reference_ids.size),
            "force_levels_mvc": force_levels,
            "friedman_statistic": friedman_statistic,
            "friedman_p_value": friedman_p_value,
            "contrasts": contrasts,
        }
    return (
        holm_adjust_pvalues,
        paired_subject_effects,
        summarize_force_level_dependence,
    )


@app.cell
def _(
    bootstrap_seeds,
    calculate_fr_data,
    conditions,
    criteria,
    mn_number,
    np,
    path,
    pd,
    print_statistics,
    selection_seeds,
    stats,
    t_end,
    t_start,
):
    # === Analysis for 10% MVC simulations ===
    mvc10_trials = np.arange(50)
    mvc10_batch = "mvc10"
    mvc10_force_level = 10  # int(0.1 * 100)

    print("=" * 60)
    print("=== FIRING RATES AT 10% MVC (batch: mvc10) ===")
    print("=" * 60)

    data_mvc10_hdemg = calculate_fr_data(
        mvc10_trials,
        "hdsemg",
        pd,
        mvc10_force_level,
        conditions,
        path,
        mvc10_batch,
        t_start,
        t_end,
        criteria=criteria,
        mn_number=mn_number,
        selection_seed=selection_seeds["mvc10_hdsemg"],
    )
    print("\n--- Randomized HD-sEMG selection ---")
    print("Selection criteria:", criteria)
    print(f"Selection seed: {selection_seeds['mvc10_hdsemg']}")
    result_mvc10_hdemg = print_statistics(
        data_mvc10_hdemg,
        stats,
        mode="10% MVC HD-sEMG",
        seed=bootstrap_seeds["10% MVC HD-sEMG"],
    )

    data_mvc10_truth = calculate_fr_data(
        mvc10_trials,
        "all",
        pd,
        mvc10_force_level,
        conditions,
        path,
        mvc10_batch,
        t_start,
        t_end,
    )
    print("\n--- Simulation truth (all active MUs) ---")
    result_mvc10_truth = print_statistics(
        data_mvc10_truth,
        stats,
        mode="10% MVC all motor units",
        seed=bootstrap_seeds["10% MVC all motor units"],
    )

    # === Analysis for 50% MVC simulations ===
    mvc50_trials = np.arange(50)
    mvc50_batch = "mvc50"
    mvc50_force_level = 50  # int(0.5 * 100)

    print("\n" + "=" * 60)
    print("=== FIRING RATES AT 50% MVC (batch: mvc50) ===")
    print("=" * 60)

    data_mvc50_hdemg = calculate_fr_data(
        mvc50_trials,
        "hdsemg",
        pd,
        mvc50_force_level,
        conditions,
        path,
        mvc50_batch,
        t_start,
        t_end,
        criteria=criteria,
        mn_number=mn_number,
        selection_seed=selection_seeds["mvc50_hdsemg"],
    )
    print("\n--- Randomized HD-sEMG selection ---")
    print("Selection criteria:", criteria)
    print(f"Selection seed: {selection_seeds['mvc50_hdsemg']}")
    result_mvc50_hdemg = print_statistics(
        data_mvc50_hdemg,
        stats,
        mode="50% MVC HD-sEMG",
        seed=bootstrap_seeds["50% MVC HD-sEMG"],
    )

    data_mvc50_truth = calculate_fr_data(
        mvc50_trials,
        "all",
        pd,
        mvc50_force_level,
        conditions,
        path,
        mvc50_batch,
        t_start,
        t_end,
    )
    print("\n--- Simulation truth (all active MUs) ---")
    result_mvc50_truth = print_statistics(
        data_mvc50_truth,
        stats,
        mode="50% MVC all motor units",
        seed=bootstrap_seeds["50% MVC all motor units"],
    )

    _additional_force_rows = []
    for _force_level, _estimate, _result in (
        (10, "randomized_hdsemg", result_mvc10_hdemg),
        (10, "simulation_truth_all_active_motor_units", result_mvc10_truth),
        (50, "randomized_hdsemg", result_mvc50_hdemg),
        (50, "simulation_truth_all_active_motor_units", result_mvc50_truth),
    ):
        _row = {"force_level_mvc": _force_level, "estimate": _estimate}
        _row.update(
            {
                f"firing_rate_{_key}": _value
                for _key, _value in _result.items()
                if _key != "isi_cv"
            }
        )
        _row.update({f"isi_cv_{_key}": _value for _key, _value in _result["isi_cv"].items()})
        _additional_force_rows.append(_row)

    pd.DataFrame(_additional_force_rows).to_csv(
        "diabetes/csv_results/additional_force_firing_rate_summary_v2.csv",
        index=False,
    )
    return (
        data_mvc10_hdemg,
        data_mvc10_truth,
        data_mvc50_hdemg,
        data_mvc50_truth,
        result_mvc10_hdemg,
        result_mvc10_truth,
        result_mvc50_hdemg,
        result_mvc50_truth,
    )


@app.cell
def _(
    bootstrap_seeds,
    conditions,
    data_hdemg,
    data_mvc10_hdemg,
    data_mvc10_truth,
    data_mvc50_hdemg,
    data_mvc50_truth,
    data_truth,
    fontweight,
    fs_label,
    fs_legend,
    fs_ticklabels,
    fs_title,
    holm_adjust_pvalues,
    n_resamples,
    np,
    os,
    paired_bootstrap_summary,
    paired_subject_effects,
    pd,
    plt,
    result_hdemg,
    result_mvc10_hdemg,
    result_mvc10_truth,
    result_mvc50_hdemg,
    result_mvc50_truth,
    result_truth,
    stats,
    summarize_force_level_dependence,
):
    os.makedirs("diabetes/figures", exist_ok=True)
    os.makedirs("diabetes/csv_results", exist_ok=True)

    _data_by_estimate = {
        "randomized_hdsemg": {
            10: data_mvc10_hdemg,
            20: data_hdemg,
            50: data_mvc50_hdemg,
        },
        "simulation_truth_all_active_motor_units": {
            10: data_mvc10_truth,
            20: data_truth,
            50: data_mvc50_truth,
        },
    }
    _result_by_estimate = {
        "randomized_hdsemg": {
            10: result_mvc10_hdemg,
            20: result_hdemg,
            50: result_mvc50_hdemg,
        },
        "simulation_truth_all_active_motor_units": {
            10: result_mvc10_truth,
            20: result_truth,
            50: result_mvc50_truth,
        },
    }
    _outcomes = (
        ("firing_rate", "mn_rate_trial_mean", "pps"),
        ("isi_cv", "isi_cv_trial_mean", "unitless"),
    )
    _seed_base = int(bootstrap_seeds["Force-level robustness"])


    def _standardized_result(result, outcome):
        if outcome == "firing_rate":
            return {
                "n_pairs": result["n_simulations"],
                "normal_mean": result["normal_mean_pps"],
                "normal_sd": result["normal_sd_pps"],
                "normal_ci_low": result["normal_ci_low"],
                "normal_ci_high": result["normal_ci_high"],
                "dpn_mean": result["DPN_mean_pps"],
                "dpn_sd": result["DPN_sd_pps"],
                "dpn_ci_low": result["DPN_ci_low"],
                "dpn_ci_high": result["DPN_ci_high"],
                "condition_effect": result["DPN_minus_normal_pps"],
                "effect_ci_low": result["difference_ci_low"],
                "effect_ci_high": result["difference_ci_high"],
                "wilcoxon_statistic": result["wilcoxon_statistic"],
                "raw_p_value": result["p_value"],
                "selection_seed": result["selection_seed"],
            }

        isi_result = result["isi_cv"]
        return {
            "n_pairs": isi_result["n_simulations"],
            "normal_mean": isi_result["normal_mean"],
            "normal_sd": isi_result["normal_sd"],
            "normal_ci_low": isi_result["normal_ci_low"],
            "normal_ci_high": isi_result["normal_ci_high"],
            "dpn_mean": isi_result["DPN_mean"],
            "dpn_sd": isi_result["DPN_sd"],
            "dpn_ci_low": isi_result["DPN_ci_low"],
            "dpn_ci_high": isi_result["DPN_ci_high"],
            "condition_effect": isi_result["DPN_minus_normal"],
            "effect_ci_low": isi_result["difference_ci_low"],
            "effect_ci_high": isi_result["difference_ci_high"],
            "wilcoxon_statistic": isi_result["wilcoxon_statistic"],
            "raw_p_value": isi_result["p_value"],
            "selection_seed": isi_result["selection_seed"],
        }


    _summary_rows = []
    _subject_rows = []
    for _outcome, _value_key, _unit in _outcomes:
        for _estimate, _force_results in _result_by_estimate.items():
            _estimate_rows = []
            for _force_level in (10, 20, 50):
                _standardized = _standardized_result(_force_results[_force_level], _outcome)
                _row = {
                    "outcome": _outcome,
                    "outcome_unit": _unit,
                    "estimate": _estimate,
                    "force_level_mvc": _force_level,
                    "primary_reference": _force_level == 20,
                    "analysis_role": (
                        "primary_reference"
                        if _force_level == 20
                        else "force_level_robustness"
                    ),
                }
                _row.update(_standardized)
                _estimate_rows.append(_row)

                _paired = paired_subject_effects(
                    _data_by_estimate[_estimate][_force_level],
                    _value_key,
                    conditions,
                )
                for _index, _simulation_id in enumerate(_paired["simulation_ids"]):
                    _subject_rows.append(
                        {
                            "outcome": _outcome,
                            "outcome_unit": _unit,
                            "estimate": _estimate,
                            "force_level_mvc": _force_level,
                            "simulation_id": int(_simulation_id),
                            "normal_value": float(_paired["first"][_index]),
                            "dpn_value": float(_paired["second"][_index]),
                            "dpn_minus_normal": float(_paired["effect"][_index]),
                        }
                    )

            _adjusted = holm_adjust_pvalues([row["raw_p_value"] for row in _estimate_rows])
            for _row, _adjusted_p_value in zip(_estimate_rows, _adjusted):
                _row["holm_adjusted_p_value_across_mvc"] = float(_adjusted_p_value)
            _summary_rows.extend(_estimate_rows)

    _summary_frame = pd.DataFrame(_summary_rows)
    _subject_frame = pd.DataFrame(_subject_rows)
    _summary_frame.to_csv(
        "diabetes/csv_results/force_level_robustness_summary_v2.csv",
        index=False,
    )
    _subject_frame.to_csv(
        "diabetes/csv_results/force_level_subject_effects_v2.csv",
        index=False,
    )

    # Compare the subject-level condition effect estimated from 10 selected MUs
    # with the known effect over every active MU at each contraction intensity.
    _bias_rows = []
    for _outcome_index, (_outcome, _value_key, _unit) in enumerate(_outcomes):
        _outcome_bias_rows = []
        for _force_level in (10, 20, 50):
            _hdsemg_effects = paired_subject_effects(
                _data_by_estimate["randomized_hdsemg"][_force_level],
                _value_key,
                conditions,
            )
            _truth_effects = paired_subject_effects(
                _data_by_estimate["simulation_truth_all_active_motor_units"][_force_level],
                _value_key,
                conditions,
            )
            if not np.array_equal(
                _hdsemg_effects["simulation_ids"],
                _truth_effects["simulation_ids"],
            ):
                raise ValueError(
                    "HD-sEMG and simulation-truth IDs must match for bias analysis."
                )

            _bias_summary = paired_bootstrap_summary(
                _truth_effects["effect"],
                _hdsemg_effects["effect"],
                _seed_base + 1000 * _outcome_index + _force_level,
                n_resamples,
            )
            _outcome_bias_rows.append(
                {
                    "outcome": _outcome,
                    "outcome_unit": _unit,
                    "force_level_mvc": _force_level,
                    "n_pairs": int(_bias_summary["n_pairs"]),
                    "truth_condition_effect": float(_truth_effects["effect"].mean()),
                    "hdsemg_condition_effect": float(_hdsemg_effects["effect"].mean()),
                    "hdsemg_minus_truth_effect_bias": float(_bias_summary["difference"]),
                    "bias_ci_low": float(_bias_summary["difference_ci"][0]),
                    "bias_ci_high": float(_bias_summary["difference_ci"][1]),
                    "wilcoxon_statistic": float(_bias_summary["wilcoxon_statistic"]),
                    "raw_p_value": float(_bias_summary["p_value"]),
                }
            )

        _adjusted = holm_adjust_pvalues([row["raw_p_value"] for row in _outcome_bias_rows])
        for _row, _adjusted_p_value in zip(_outcome_bias_rows, _adjusted):
            _row["holm_adjusted_p_value_across_mvc"] = float(_adjusted_p_value)
        _bias_rows.extend(_outcome_bias_rows)

    _bias_frame = pd.DataFrame(_bias_rows)
    _bias_frame.to_csv(
        "diabetes/csv_results/force_level_estimator_bias_v2.csv",
        index=False,
    )

    # A force-by-condition interaction is represented by a change in each
    # subject's DPN-minus-Normal effect across MVC levels.
    _dependence_rows = []
    for _outcome_index, (_outcome, _value_key, _unit) in enumerate(_outcomes):
        for _estimate_index, (_estimate, _force_data) in enumerate(
            _data_by_estimate.items()
        ):
            _effects_by_force = {
                _force_level: paired_subject_effects(
                    _force_data[_force_level], _value_key, conditions
                )
                for _force_level in (10, 20, 50)
            }
            _dependence = summarize_force_level_dependence(
                _effects_by_force,
                paired_bootstrap_summary,
                stats,
                holm_adjust_pvalues,
                seed=(_seed_base + 5000 + 1000 * _outcome_index + 100 * _estimate_index),
                n_resamples=n_resamples,
                reference_force=20,
            )
            for _contrast in _dependence["contrasts"]:
                _dependence_rows.append(
                    {
                        "outcome": _outcome,
                        "outcome_unit": _unit,
                        "estimate": _estimate,
                        "n_subjects": _dependence["n_subjects"],
                        "force_levels_mvc": "10,20,50",
                        "omnibus_test": "friedman",
                        "friedman_statistic": _dependence["friedman_statistic"],
                        "friedman_p_value": _dependence["friedman_p_value"],
                        **_contrast,
                    }
                )

    _dependence_frame = pd.DataFrame(_dependence_rows)
    _dependence_frame.to_csv(
        "diabetes/csv_results/force_level_dependence_contrasts_v2.csv",
        index=False,
    )

    print("=" * 78)
    print("=== FORCE-LEVEL ROBUSTNESS OF DPN - NORMAL EFFECTS ===")
    print("=" * 78)
    for _outcome, _, _unit in _outcomes:
        print(f"\n{_outcome} ({_unit})")
        for _row in _summary_frame[_summary_frame["outcome"] == _outcome].to_dict("records"):
            print(
                f"  {_row['force_level_mvc']:>2}% MVC, {_row['estimate']}: "
                f"{_row['condition_effect']:+.4f} "
                f"[{_row['effect_ci_low']:+.4f}, {_row['effect_ci_high']:+.4f}], "
                f"p={_row['raw_p_value']:.4g}, "
                f"Holm p={_row['holm_adjusted_p_value_across_mvc']:.4g}"
            )

        for _estimate in _data_by_estimate:
            _rows = _dependence_frame[
                (_dependence_frame["outcome"] == _outcome)
                & (_dependence_frame["estimate"] == _estimate)
            ]
            _first = _rows.iloc[0]
            print(
                f"  MVC dependence, {_estimate}: Friedman "
                f"Q={_first['friedman_statistic']:.3f}, "
                f"p={_first['friedman_p_value']:.4g}"
            )
            for _, _contrast in _rows.iterrows():
                print(
                    f"    {_contrast['contrast_label']}: "
                    f"{_contrast['effect_contrast']:+.4f} "
                    f"[{_contrast['contrast_ci_low']:+.4f}, "
                    f"{_contrast['contrast_ci_high']:+.4f}], "
                    f"Holm p={_contrast['holm_adjusted_p_value']:.4g}"
                )


    def finalize_force_robustness_figure(
        figure,
        handles,
        labels,
        legend_fontsize,
        title_fontsize,
        title_fontweight,
    ):
        """Place the global legend below a non-overlapping figure title."""
        title = figure.suptitle(
            "Robustness of paired condition effects across contraction intensities",
            fontsize=title_fontsize,
            fontweight=title_fontweight,
            y=0.99,
        )
        legend = figure.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.91),
            ncol=2,
            fontsize=legend_fontsize,
            frameon=False,
        )
        figure.tight_layout(rect=(0, 0, 1, 0.80))
        return title, legend


    _figure, _axes = plt.subplots(1, 2, figsize=(14, 6))
    _estimate_styles = {
        "randomized_hdsemg": {
            "label": "Randomized HD-sEMG estimate (10 MUs)",
            "color": "red",
            "marker": "o",
            "offset": -0.7,
        },
        "simulation_truth_all_active_motor_units": {
            "label": "Simulation truth (all active MUs)",
            "color": "green",
            "marker": "s",
            "offset": 0.7,
        },
    }
    _axis_labels = {
        "firing_rate": "DPN - Normal firing rate (pps)",
        "isi_cv": "DPN - Normal mean ISI-CoV",
    }
    _panel_titles = {
        "firing_rate": "Firing rate",
        "isi_cv": "ISI-CoV",
    }
    for _axis, (_outcome, _, _) in zip(_axes, _outcomes):
        _axis.axhline(0, color="black", linewidth=1, zorder=0)
        for _estimate, _style in _estimate_styles.items():
            _plot_data = _summary_frame[
                (_summary_frame["outcome"] == _outcome)
                & (_summary_frame["estimate"] == _estimate)
            ].sort_values("force_level_mvc")
            _x = _plot_data["force_level_mvc"].to_numpy(dtype=float)
            _effect = _plot_data["condition_effect"].to_numpy(dtype=float)
            _lower = _plot_data["effect_ci_low"].to_numpy(dtype=float)
            _upper = _plot_data["effect_ci_high"].to_numpy(dtype=float)
            _axis.errorbar(
                _x + _style["offset"],
                _effect,
                yerr=np.vstack((_effect - _lower, _upper - _effect)),
                color=_style["color"],
                marker=_style["marker"],
                markersize=9,
                linewidth=2,
                capsize=5,
                label=_style["label"],
            )
        _axis.axvline(20, color="grey", linestyle=":", linewidth=1.5)
        _axis.set_xticks([10, 20, 50])
        _axis.set_xlabel("Contraction intensity (% MVC)", fontsize=fs_label)
        _axis.set_ylabel(_axis_labels[_outcome], fontsize=fs_label)
        _axis.set_title(_panel_titles[_outcome], fontsize=fs_title, fontweight=fontweight)
        _axis.tick_params(axis="both", labelsize=fs_ticklabels)

    _handles, _labels = _axes[0].get_legend_handles_labels()
    finalize_force_robustness_figure(
        _figure,
        _handles,
        _labels,
        legend_fontsize=fs_legend,
        title_fontsize=fs_title,
        title_fontweight=fontweight,
    )
    _figure_path = "diabetes/figures/force_level_robustness_v2.png"
    _figure.savefig(_figure_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(_figure)

    print(f"\nForce-level robustness figure saved to: {_figure_path}")
    print("Statistical summaries saved to diabetes/csv_results/force_level_*_v2.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Selection-threshold sensitivity analysis

    At 20% MVC, the ISI-CoV eligibility threshold was varied while holding the
    remaining selection criteria constant to assess the sensitivity of
    HD-sEMG-like estimates to this analytical choice.

    The HD-sEMG analysis first applies a firing-rate window
    (`fmin < FR < fmax`) and an ISI-CoV ceiling, then randomly samples 10 eligible
    motor units without replacement. Per-MU firing rates and ISI-CoV values are
    computed once per simulated subject and reused across all analyses below.

    Selection stability is evaluated over 1,000 prespecified seeds at 20%, 10%,
    and 50% MVC. The threshold analysis uses that same ordered seed set at every
    ISI-CoV threshold (common random numbers), so differences along the curve are
    less affected by unrelated draw noise. Its shaded band is the central 95%
    across-selection-seed range, not a confidence interval. The known mean over
    all active motor units is shown separately as the simulation truth.
    """)
    return


@app.cell
def _(compute_cv, compute_fr, conditions, np, path, pd, stats, t_end, t_start):
    def build_mu_stats(trials, batch_name, force_level=20):
        """Cache per-motor-unit firing rate and ISI-CoV for each subject and condition.

        Returns ``{(condition, trial): (unit_ids, firing_rate, isi_cov)}`` using
        the same estimators as the main analysis.
        """
        cache = {}
        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/"
                    f"cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                ).values
                unit_ids = np.unique(data[:, 0])
                steady = data[(data[:, 1] >= t_start) & (data[:, 1] <= t_end)]
                isi_cov, _ = compute_cv(unit_ids, steady, t_start, t_end)
                firing_rate = compute_fr(unit_ids, data, t_start, t_end)
                cache[(condition, int(trial))] = (
                    unit_ids.astype(int),
                    firing_rate,
                    isi_cov,
                )
        return cache


    def _selection_mean_rate(unit_stats, fmin, fmax, isicv, mn_number, rng):
        """Sample eligible MUs and return their mean rate and the pool size."""
        _, firing_rate, isi_cov = unit_stats
        eligible = np.where(
            (firing_rate >= 0.01)
            & (firing_rate > fmin)
            & (firing_rate < fmax)
            & (isi_cov <= isicv)
        )[0]
        pool_size = int(eligible.size)
        if pool_size < mn_number:
            raise ValueError(
                f"Cannot select {mn_number} HD-sEMG motor units from "
                f"{pool_size} eligible units at fmin={fmin}, fmax={fmax}, "
                f"ISI-CoV={isicv}."
            )
        selected = rng.choice(eligible, size=mn_number, replace=False)
        return float(firing_rate[selected].mean()), pool_size


    def selection_paired_difference(
        cache, trials, fmin, fmax, isicv, mn_number, selection_seed
    ):
        """Return one seeded randomized HD-sEMG paired comparison."""
        selection_rng = np.random.default_rng(selection_seed)
        condition_means = {condition: [] for condition in conditions}
        pool_sizes = []
        for trial in trials:
            for condition in conditions:
                mean_rate, pool_size = _selection_mean_rate(
                    cache[(condition, int(trial))],
                    fmin,
                    fmax,
                    isicv,
                    mn_number,
                    selection_rng,
                )
                condition_means[condition].append(mean_rate)
                pool_sizes.append(pool_size)

        normal = np.asarray(condition_means[conditions[0]], dtype=float)
        dpn = np.asarray(condition_means[conditions[1]], dtype=float)
        paired = np.isfinite(normal) & np.isfinite(dpn)
        wilcoxon_result = stats.wilcoxon(dpn[paired], normal[paired])
        return {
            "selection_strategy": "seeded_random_10",
            "selection_seed": int(selection_seed),
            "sample_size": int(mn_number),
            "fmin": float(fmin),
            "fmax": float(fmax),
            "isicv": float(isicv),
            "normal_mean": float(normal[paired].mean()),
            "dpn_mean": float(dpn[paired].mean()),
            "difference": float((dpn - normal)[paired].mean()),
            "wilcoxon_statistic": float(wilcoxon_result.statistic),
            "p_value": float(wilcoxon_result.pvalue),
            "n_pairs": int(paired.sum()),
            "min_eligible_pool": int(min(pool_sizes)) if pool_sizes else 0,
            "median_eligible_pool": float(np.median(pool_sizes)) if pool_sizes else 0,
            "max_eligible_pool": int(max(pool_sizes)) if pool_sizes else 0,
        }


    def selection_seed_stability(
        cache, trials, fmin, fmax, isicv, mn_number, selection_seeds
    ):
        """Evaluate the paired estimate over an explicit ordered seed set."""
        return pd.DataFrame(
            [
                selection_paired_difference(
                    cache,
                    trials,
                    fmin,
                    fmax,
                    isicv,
                    mn_number,
                    selection_seed,
                )
                for selection_seed in selection_seeds
            ]
        )


    def simulation_truth_paired_difference(cache, trials):
        """Return the paired comparison over every active MU in each simulation."""
        condition_means = {condition: [] for condition in conditions}
        active_counts = []
        for trial in trials:
            for condition in conditions:
                _, firing_rate, _ = cache[(condition, int(trial))]
                active_rates = firing_rate[firing_rate >= 0.01]
                condition_means[condition].append(float(active_rates.mean()))
                active_counts.append(int(active_rates.size))

        normal = np.asarray(condition_means[conditions[0]], dtype=float)
        dpn = np.asarray(condition_means[conditions[1]], dtype=float)
        wilcoxon_result = stats.wilcoxon(dpn, normal)
        return {
            "selection_strategy": "simulation_truth_all_active_motor_units",
            "normal_mean": float(normal.mean()),
            "dpn_mean": float(dpn.mean()),
            "difference": float((dpn - normal).mean()),
            "wilcoxon_statistic": float(wilcoxon_result.statistic),
            "p_value": float(wilcoxon_result.pvalue),
            "n_pairs": int(normal.size),
            "min_active_motor_units": int(min(active_counts)),
            "median_active_motor_units": float(np.median(active_counts)),
            "max_active_motor_units": int(max(active_counts)),
        }


    def selection_stability_summary(distribution):
        """Summarize across-seed variation without treating it as sampling error."""
        differences = distribution["difference"].to_numpy(dtype=float)
        return {
            "n_selection_seeds": int(distribution.shape[0]),
            "mean_difference_across_seeds": float(differences.mean()),
            "sd_difference_across_seeds": float(differences.std(ddof=1)),
            "median_difference_across_seeds": float(np.median(differences)),
            "selection_range_2_5_percentile": float(np.quantile(differences, 0.025)),
            "selection_range_97_5_percentile": float(np.quantile(differences, 0.975)),
            "fraction_nonnegative": float(np.mean(differences >= 0)),
            "fraction_nominal_p_below_0_05": float(
                np.mean(distribution["p_value"].to_numpy(dtype=float) < 0.05)
            ),
            "eligible_pool_minimum": int(distribution["min_eligible_pool"].min()),
            "eligible_pool_median": float(distribution["median_eligible_pool"].median()),
            "eligible_pool_maximum": int(distribution["max_eligible_pool"].max()),
        }
    return (
        build_mu_stats,
        selection_paired_difference,
        selection_seed_stability,
        selection_stability_summary,
        simulation_truth_paired_difference,
    )


@app.cell
def _(
    batch_name,
    build_mu_stats,
    criteria,
    fontweight,
    fs_label,
    fs_legend,
    fs_ticklabels,
    fs_title,
    mn_number,
    n_selection_seeds,
    np,
    os,
    pd,
    plt,
    selection_paired_difference,
    selection_seed_stability,
    selection_seeds,
    selection_stability_summary,
    simulation_truth_paired_difference,
    trials,
):
    os.makedirs("diabetes/figures", exist_ok=True)
    os.makedirs("diabetes/csv_results", exist_ok=True)


    def add_threshold_truth_reference(ax, truth_difference):
        """Add Figure 3's emphasized simulation-truth reference."""
        return ax.axhline(
            truth_difference,
            color="green",
            linestyle="--",
            linewidth=3,
            label=f"Simulation truth ({truth_difference:+.2f} pps)",
        )


    _stability_seeds = np.arange(
        selection_seeds["seed_stability_start"],
        selection_seeds["seed_stability_start"] + n_selection_seeds,
    )
    _force_specs = (
        (20, trials, batch_name, selection_seeds["hdsemg"]),
        (10, np.arange(50), "mvc10", selection_seeds["mvc10_hdsemg"]),
        (50, np.arange(50), "mvc50", selection_seeds["mvc50_hdsemg"]),
    )
    _force_output_paths = {
        20: "diabetes/csv_results/selection_seed_stability_20mvc_v2.csv",
        10: "diabetes/csv_results/selection_seed_stability_10mvc_v2.csv",
        50: "diabetes/csv_results/selection_seed_stability_50mvc_v2.csv",
    }
    _force_caches = {}
    _force_summaries = []

    print("=" * 78)
    print("=== RANDOMIZED HD-sEMG SELECTION-STABILITY ANALYSIS ===")
    print("=" * 78)
    for _force_level, _force_trials, _batch, _fixed_seed in _force_specs:
        _cache = build_mu_stats(_force_trials, _batch, force_level=_force_level)
        _force_caches[_force_level] = _cache
        _distribution = selection_seed_stability(
            _cache,
            _force_trials,
            criteria["fmin"],
            criteria["fmax"],
            criteria["isicv"],
            mn_number,
            _stability_seeds,
        )
        _distribution.insert(0, "force_level_mvc", _force_level)
        _distribution.to_csv(_force_output_paths[_force_level], index=False)

        _fixed = selection_paired_difference(
            _cache,
            _force_trials,
            criteria["fmin"],
            criteria["fmax"],
            criteria["isicv"],
            mn_number,
            _fixed_seed,
        )
        _truth = simulation_truth_paired_difference(_cache, _force_trials)
        _summary = selection_stability_summary(_distribution)
        _summary.update(
            {
                "force_level_mvc": _force_level,
                "n_pairs": int(len(_force_trials)),
                "fixed_selection_seed": int(_fixed_seed),
                "fixed_normal_mean": _fixed["normal_mean"],
                "fixed_dpn_mean": _fixed["dpn_mean"],
                "fixed_difference": _fixed["difference"],
                "fixed_wilcoxon_statistic": _fixed["wilcoxon_statistic"],
                "fixed_p_value": _fixed["p_value"],
                "truth_normal_mean": _truth["normal_mean"],
                "truth_dpn_mean": _truth["dpn_mean"],
                "truth_difference": _truth["difference"],
                "truth_wilcoxon_statistic": _truth["wilcoxon_statistic"],
                "truth_p_value": _truth["p_value"],
            }
        )
        _force_summaries.append(_summary)

        print(
            f"{_force_level:>2}% MVC ({len(_force_trials)} pairs): fixed seed "
            f"{_fixed_seed}, difference {_fixed['difference']:+.3f} pps, "
            f"p={_fixed['p_value']:.4g}"
        )
        print(
            "   Across-selection-seed range: "
            f"{_summary['selection_range_2_5_percentile']:+.3f} to "
            f"{_summary['selection_range_97_5_percentile']:+.3f} pps; "
            f"median {_summary['median_difference_across_seeds']:+.3f}"
        )
        print(
            "   Eligible pool (minimum/median/maximum): "
            f"{_summary['eligible_pool_minimum']}/"
            f"{_summary['eligible_pool_median']:.1f}/"
            f"{_summary['eligible_pool_maximum']}"
        )
        print(
            f"   Simulation truth: {_truth['difference']:+.3f} pps, "
            f"p={_truth['p_value']:.4g}"
        )

    pd.DataFrame(_force_summaries).to_csv(
        "diabetes/csv_results/selection_seed_stability_summary_v2.csv",
        index=False,
    )

    _cache = _force_caches[20]
    _truth = simulation_truth_paired_difference(_cache, trials)

    # Grid spanning the ISI-CoV thresholds used experimentally (0.2-0.3) and beyond.
    _isicv_grid = [0.15, 0.20, 0.25, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.45, 0.50]

    _threshold_distributions = []
    _threshold_summaries = []
    for _isicv in _isicv_grid:
        _threshold_distribution = selection_seed_stability(
            _cache,
            trials,
            criteria["fmin"],
            criteria["fmax"],
            _isicv,
            mn_number,
            _stability_seeds,
        )
        _threshold_distributions.append(_threshold_distribution)
        _threshold_summary = selection_stability_summary(_threshold_distribution)
        _threshold_summary.update(
            {
                "isicv": float(_isicv),
                "fmin": float(criteria["fmin"]),
                "fmax": float(criteria["fmax"]),
                "sample_size": int(mn_number),
                "n_pairs": int(len(trials)),
                "truth_difference": _truth["difference"],
            }
        )
        _threshold_summaries.append(_threshold_summary)

    pd.concat(_threshold_distributions, ignore_index=True).to_csv(
        "diabetes/csv_results/selection_threshold_sensitivity_v2.csv", index=False
    )
    _threshold_summary_frame = pd.DataFrame(_threshold_summaries).sort_values("isicv")
    _threshold_summary_frame.to_csv(
        "diabetes/csv_results/selection_threshold_sensitivity_summary_v2.csv",
        index=False,
    )

    print("=" * 78)
    print("=== SELECTION-THRESHOLD SENSITIVITY (20% MVC) ===")
    print("=" * 78)
    print(
        f"Simulation truth (all active MUs): {_truth['difference']:+.2f} pps  "
        f"(Normal {_truth['normal_mean']:.2f}, DPN {_truth['dpn_mean']:.2f})"
    )
    print(
        f"Fixed: fmin={criteria['fmin']} pps, fmax={criteria['fmax']} pps, "
        f"mn_number={mn_number}, {len(trials)} paired subjects"
    )
    print(
        f"Common ordered seed set: {_stability_seeds[0]}-{_stability_seeds[-1]} "
        "at every threshold"
    )
    print(f"\n{'ISI-CoV':>8}{'median difference':>20}{'95% seed range':>27}{'min pool':>10}")
    for _row in _threshold_summaries:
        _flag = "   <- main analysis" if _row["isicv"] == criteria["isicv"] else ""
        print(
            f"{_row['isicv']:>8.2f}"
            f"{_row['median_difference_across_seeds']:>+20.3f}"
            f"{_row['selection_range_2_5_percentile']:>+12.3f} to "
            f"{_row['selection_range_97_5_percentile']:>+7.3f}"
            f"{_row['eligible_pool_minimum']:>10}{_flag}"
        )

    # --- Figure: paired difference against the ISI-CoV eligibility threshold ---
    _fig, _ax = plt.subplots(figsize=(10, 6.5))

    _x = _threshold_summary_frame["isicv"].to_numpy(dtype=float)
    _median = _threshold_summary_frame["median_difference_across_seeds"].to_numpy(
        dtype=float
    )
    _lower = _threshold_summary_frame["selection_range_2_5_percentile"].to_numpy(dtype=float)
    _upper = _threshold_summary_frame["selection_range_97_5_percentile"].to_numpy(
        dtype=float
    )

    _ax.axhline(0, color="black", linewidth=1)
    add_threshold_truth_reference(_ax, _truth["difference"])
    _ax.plot(
        _x,
        _median,
        "o-",
        color="tab:blue",
        markersize=9,
        linewidth=2,
        label=f"Median randomized HD-sEMG estimate ({mn_number} MUs)",
    )
    _ax.fill_between(
        _x,
        _lower,
        _upper,
        color="tab:blue",
        alpha=0.2,
        label="Central 95% across-selection-seed range",
    )
    _ax.axvline(criteria["isicv"], color="grey", linestyle=":", linewidth=2)
    _ax.text(
        criteria["isicv"] - 0.005,
        0.02,
        "main analysis",
        transform=_ax.get_xaxis_transform(),
        rotation=90,
        va="bottom",
        ha="right",
        color="grey",
        fontsize=fs_legend,
    )

    _ax.set_xlabel("ISI-CoV eligibility threshold", fontsize=fs_label)
    _ax.set_ylabel("Paired difference, DPN - Normal (pps)", fontsize=fs_label)
    _ax.set_title(
        "Selection-threshold sensitivity at 20% MVC",
        fontsize=fs_title,
        fontweight=fontweight,
    )
    _ax.tick_params(axis="both", labelsize=fs_ticklabels)
    # Headroom above the simulation-truth line keeps the legend clear of the curves.
    _ax.set_ylim(
        float(_lower.min()) - 0.15,
        max(float(_upper.max()), _truth["difference"]) + 0.65,
    )
    _ax.legend(fontsize=fs_legend, loc="upper left")
    _fig.tight_layout()

    _figure_path = "diabetes/figures/selection_threshold_sensitivity_v2.png"
    _fig.savefig(_figure_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(_fig)

    print(f"\nFigure saved to: {_figure_path}")
    print("Sweep saved to: diabetes/csv_results/selection_threshold_sensitivity_v2.csv")
    return


if __name__ == "__main__":
    app.run()
