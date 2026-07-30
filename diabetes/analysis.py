import marimo

__generated_with = "0.17.8"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Computational modeling reveals a potential selection bias in high-density surface electromyography analysis of diabetic neuropathy

    > Renato Naville Watanabe, Marcos Duarte
    > Federal University of ABC, Brazil
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

    modes = ["HD-sEMG", "Random"]

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
        "randomly": 20260101,
        "filtered_random": 20260102,
        "fr_cv": 20260103,
        "mvc10_randomly": 20260104,
        "mvc50_randomly": 20260105,
    }
    n_resamples = 100_000
    bootstrap_seeds = {
        "HD-sEMG": 20260106,
        "Random": 20260107,
        "Filtered-Random": 20260108,
        "All motor units": 20260109,
        "10% MVC HD-sEMG": 20260110,
        "10% MVC all motor units": 20260111,
        "10% MVC Random": 20260112,
        "50% MVC HD-sEMG": 20260113,
        "50% MVC all motor units": 20260114,
        "50% MVC Random": 20260115,
    }
    return (
        batch_name,
        bootstrap_seeds,
        conditions,
        criteria,
        fontweight,
        fs_label,
        fs_legend,
        fs_ticklabels,
        fs_title,
        markersize,
        mn_number,
        modes,
        n_resamples,
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
    criteria,
    filtfilt,
    fs_label,
    fs_ticklabels,
    fs_title,
    markersize,
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


    def select_mns_regular(
        data, t_start, t_end, column_spikes=1, criteria=criteria, mn_number=mn_number
    ):
        """Select eligible motor units with the lowest firing rates."""
        # Restrict ISI calculations to the steady-state interval.
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
        selected_neurons = unique_neurons[selection_criteria].astype(int)
        fr_sel = fr[selection_criteria]
        if len(selected_neurons) > mn_number:
            selected_neurons = selected_neurons[np.argsort(fr_sel)][:mn_number]

        return selected_neurons


    def select_mns_filtered_random(
        data,
        t_start,
        t_end,
        column_spikes=1,
        criteria=criteria,
        mn_number=mn_number,
        rng=None,
    ):
        """Randomly select eligible motor units after HD-sEMG-like filtering."""
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
        # Apply same filtering criteria as HD-sEMG
        selection_criteria = np.where(
            (fr > criteria["fmin"]) & (fr < criteria["fmax"]) & (ISI_CV <= criteria["isicv"])
        )[0]
        selected_neurons = unique_neurons[selection_criteria].astype(int)
        # Randomly pick mn_number from those that pass (instead of lowest FR)
        if len(selected_neurons) > mn_number:
            selected_neurons = rng.choice(selected_neurons, size=mn_number, replace=False)

        return selected_neurons


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
        ax.set_ylabel("Mean MU firing rate per simulation (pps)")
        fig.tight_layout()
        fig.savefig(f"diabetes/mn_firing_rate_comparison_{mode}.png")
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
            df.to_csv(f"diabetes/mn_firing_rate_{cond}_{mode}.csv", index=False)

        df_mean = pd.DataFrame(
            {
                "condition": conditions,
                "n_simulations": [len(simulation_fr[cond]) for cond in conditions],
                "mean_firing_rate": mean_fr,
                "sd_firing_rate": sd_fr,
            }
        )
        df_mean.to_csv(f"diabetes/mn_firing_rate_summary_{mode}.csv", index=False)


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

        random_modes = {"randomly", "filtered_random"}
        if mode in random_modes and selection_seed is None:
            raise ValueError(f"selection_seed is required for mode '{mode}'.")
        selection_rng = (
            np.random.default_rng(selection_seed) if mode in random_modes else None
        )

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
                if mode == "randomly":
                    selected_neurons = select_mns_randomly(
                        data,
                        t_start=t_start_param,
                        t_end=t_end_param,
                        size=mn_number,
                        rng=selection_rng,
                    )
                elif mode == "regular":
                    selected_neurons = select_mns_regular(
                        data,
                        t_start=t_start_param,
                        t_end=t_end_param,
                        criteria=criteria,
                        mn_number=mn_number,
                    )
                elif mode == "filtered_random":
                    selected_neurons = select_mns_filtered_random(
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


    def plot_mn_fr_combined_data(data_regular, data_random, data_truth, conditions, pd):
        """Plot selection-mode estimates against the all-MU simulation truth."""
        import os

        os.makedirs("diabetes/figures", exist_ok=True)
        os.makedirs("diabetes/csv_results", exist_ok=True)

        for condition in conditions:
            truth_ids = data_truth["simulation_ids"][condition]
            for mode_name, mode_data in (
                ("HD-sEMG", data_regular),
                ("Random", data_random),
            ):
                if not np.array_equal(mode_data["simulation_ids"][condition], truth_ids):
                    raise ValueError(
                        f"{mode_name} and simulation-truth IDs differ for {condition}."
                    )

        truth_mean_fr = np.asarray(
            [
                np.mean(data_truth["mn_rate_trial_mean"][condition])
                for condition in conditions
            ]
        )

        # Create one panel for each motor-unit selection mode.
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

        def add_significance_bars(ax, p_values):
            """Add a bar when the paired comparison is statistically significant."""
            # Compare Normal and DPN at positions 1 and 2.
            print(p_values["normal_vs_DPN"])
            if p_values["normal_vs_DPN"] < 0.05:
                y_pos = 20  # max_y + 0.3
                ax.plot([1, 2], [y_pos, y_pos], "k-", linewidth=2)
                ax.plot([1, 1], [y_pos - 0.5, y_pos], "k-", linewidth=2)
                ax.plot([2, 2], [y_pos - 0.5, y_pos], "k-", linewidth=2)
                significance = (
                    "***"
                    if p_values["normal_vs_DPN"] < 0.001
                    else "**"
                    if p_values["normal_vs_DPN"] < 0.01
                    else "*"
                )
                ax.text(
                    1.5,
                    y_pos + 0.1,
                    significance,
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize="xx-large",
                )
            return p_values

        def plot_data(ax, data, title, seed):
            """Plot simulation-level rates with bootstrap intervals."""
            bootstrap_result = bootstrap_mode(data, title, seed, n_resamples)
            isi_cv_result = bootstrap_isi_cv(data, title, seed, n_resamples)
            jitter_rng = np.random.default_rng(seed + 10_000)
            simulation_rates = data["mn_rate_trial_mean"]
            mean_fr = np.asarray(
                [
                    bootstrap_result["normal_mean_pps"],
                    bootstrap_result["DPN_mean_pps"],
                ]
            )
            confidence_intervals = np.asarray(
                [
                    [
                        bootstrap_result["normal_ci_low"],
                        bootstrap_result["normal_ci_high"],
                    ],
                    [
                        bootstrap_result["DPN_ci_low"],
                        bootstrap_result["DPN_ci_high"],
                    ],
                ]
            )
            yerr = np.vstack(
                (
                    mean_fr - confidence_intervals[:, 0],
                    confidence_intervals[:, 1] - mean_fr,
                )
            )

            estimate_handle = ax.errorbar(
                [1, 2],
                mean_fr,
                marker="+",
                linestyle="",
                color="black",
                markersize=markersize,
                markeredgewidth=2,
                yerr=yerr,
                capsize=5,
                zorder=4,
            )
            # ax.grid()
            ax.scatter(
                1 + 0.1 * jitter_rng.normal(size=simulation_rates[conditions[0]].size),
                simulation_rates[conditions[0]].ravel(),
                alpha=0.6,
            )
            ax.scatter(
                2 + 0.1 * jitter_rng.normal(size=simulation_rates[conditions[1]].size),
                simulation_rates[conditions[1]].ravel(),
                alpha=0.6,
            )
            truth_handle = ax.scatter(
                [1, 2],
                truth_mean_fr,
                marker="D",
                s=markersize**2,
                facecolors="none",
                edgecolors="black",
                linewidths=1.8,
                zorder=5,
            )
            ax.set_ylim(0, 22)
            ax.set_xticks([1, 2])
            ax.set_xticklabels(
                [
                    cond.replace("_", " ").title() if cond != "DPN" else "DPN"
                    for cond in conditions
                ],
                fontsize=fs_ticklabels,
            )
            ax.set_yticks([0, 5, 10, 15, 20])
            if title == f"{modes[0]} Mode":
                ax.set_ylabel("Mean MU firing rate per simulation (pps)", fontsize=fs_label)
                ax.set_yticklabels([0, 5, 10, 15, 20], fontsize=fs_ticklabels)
            ax.set_title(title, fontsize=fs_title)

            # Add significance annotations from the paired Wilcoxon test.
            statistic = bootstrap_result["wilcoxon_statistic"]
            p_values = {"normal_vs_DPN": bootstrap_result["p_value"]}
            p_values = add_significance_bars(ax, p_values)

            return (
                statistic,
                p_values,
                bootstrap_result,
                isi_cv_result,
                estimate_handle,
                truth_handle,
            )

        # HD-sEMG selection mode (left).
        (
            statistic_regular,
            p_values_regular,
            bootstrap_regular,
            isi_cv_regular,
            estimate_handle,
            truth_handle,
        ) = plot_data(
            ax1,
            data_regular,
            f"{modes[0]} Mode",
            bootstrap_seeds["HD-sEMG"],
        )

        # Random selection mode (right).
        (
            statistic_random,
            p_values_random,
            bootstrap_random,
            isi_cv_random,
            _estimate_handle_random,
            _truth_handle_random,
        ) = plot_data(
            ax2,
            data_random,
            f"{modes[1]} Mode",
            bootstrap_seeds["Random"],
        )

        fig.legend(
            handles=[estimate_handle, truth_handle],
            labels=[
                "Selection-mode mean (95% BCa CI)",
                "Mean simulation truth (all MUs)",
            ],
            loc="lower center",
            ncol=2,
            frameon=False,
            fontsize=fs_ticklabels,
        )
        fig.tight_layout(rect=(0, 0.12, 1, 1))

        # Save the combined figure.
        fig.savefig(
            "diabetes/figures/mn_firing_rate_comparison_combined.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close(fig)

        # Export one firing-rate and ISI-CoV mean per simulation/subject.
        for mode, data_dict in [("regular", data_regular), ("random", data_random)]:
            for cond in conditions:
                df = pd.DataFrame(
                    {
                        "simulation_id": data_dict["simulation_ids"][cond],
                        "mean_firing_rate": data_dict["mn_rate_trial_mean"][cond],
                        "mean_ISI_CV": data_dict["isi_cv_trial_mean"][cond],
                        "n_motor_units": data_dict["n_motor_units"][cond],
                    }
                )
                df.to_csv(
                    f"diabetes/csv_results/mn_firing_rate_{cond}_{mode}_combined.csv",
                    index=False,
                )

        # Export effect estimates, confidence intervals, and p-values.
        p_values_df = pd.DataFrame(
            {
                "comparison": ["normal_vs_DPN"],
                "unit_of_analysis": ["simulation/subject"],
                "test": ["paired Wilcoxon signed-rank"],
                "random_selection_seed": [data_random["selection_seed"]],
                "bootstrap_seed_regular": [bootstrap_seeds["HD-sEMG"]],
                "bootstrap_seed_random": [bootstrap_seeds["Random"]],
                "n_resamples": [n_resamples],
                "n_simulations_regular": [bootstrap_regular["n_simulations"]],
                "n_simulations_random": [bootstrap_random["n_simulations"]],
                "wilcoxon_statistic_regular": [statistic_regular],
                "wilcoxon_statistic_random": [statistic_random],
                "p_value_regular": [p_values_regular["normal_vs_DPN"]],
                "p_value_random": [p_values_random["normal_vs_DPN"]],
                "mean_difference_regular": [bootstrap_regular["DPN_minus_normal_pps"]],
                "ci_low_regular": [bootstrap_regular["difference_ci_low"]],
                "ci_high_regular": [bootstrap_regular["difference_ci_high"]],
                "mean_difference_random": [bootstrap_random["DPN_minus_normal_pps"]],
                "ci_low_random": [bootstrap_random["difference_ci_low"]],
                "ci_high_random": [bootstrap_random["difference_ci_high"]],
                "significant_random": [p_values_random["normal_vs_DPN"] < 0.05],
                "isi_cv_wilcoxon_statistic_regular": [isi_cv_regular["wilcoxon_statistic"]],
                "isi_cv_wilcoxon_statistic_random": [isi_cv_random["wilcoxon_statistic"]],
                "isi_cv_p_value_regular": [isi_cv_regular["p_value"]],
                "isi_cv_p_value_random": [isi_cv_random["p_value"]],
                "isi_cv_mean_difference_regular": [isi_cv_regular["DPN_minus_normal"]],
                "isi_cv_ci_low_regular": [isi_cv_regular["difference_ci_low"]],
                "isi_cv_ci_high_regular": [isi_cv_regular["difference_ci_high"]],
                "isi_cv_mean_difference_random": [isi_cv_random["DPN_minus_normal"]],
                "isi_cv_ci_low_random": [isi_cv_random["difference_ci_low"]],
                "isi_cv_ci_high_random": [isi_cv_random["difference_ci_high"]],
            }
        )
        p_values_df.to_csv(
            "diabetes/csv_results/mn_firing_rate_p_values_combined.csv", index=False
        )

        print(
            "Combined figure with significance bars saved to: "
            "diabetes/figures/mn_firing_rate_comparison_combined.png"
        )
        print(
            "Statistical results saved to: "
            "diabetes/csv_results/mn_firing_rate_p_values_combined.csv"
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
        bootstrap_mode,
        calculate_fr_data,
        compute_cv,
        compute_fr,
        plot_mn_fr_combined_data,
        print_statistics,
        select_mns_randomly,
        select_mns_regular,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## All-motor-unit simulation-truth reference

    For each simulated subject, the mean firing rate across the complete active-MU population is the trial-specific simulation truth. The condition means across these subject-specific true values are used as references in both selection-mode panels below.
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
    data_all = calculate_fr_data(
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
    print_statistics(
        data_all,
        stats,
        mode="Simulation truth (all motor units)",
        seed=bootstrap_seeds["All motor units"],
    )
    return (data_all,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Firing rates at 20% MVC

    Each simulation represents one subject. Group means, SDs, confidence intervals, and tests for firing rate and ISI-CoV therefore use one mean per simulation; raw motor-unit values are retained only for explicitly descriptive analyses.
    Random-mode selections contain 10 unique motor units per simulation and use the configured fixed selection seed.
    In both panels, hollow diamonds show the condition mean of the trial-specific simulation truth calculated from all active MUs.
    """)
    return


@app.cell
def _(
    batch_name,
    bootstrap_seeds,
    calculate_fr_data,
    conditions,
    criteria,
    mn_number,
    path,
    pd,
    plot_mn_fr_combined_data,
    print_statistics,
    selection_seeds,
    stats,
    t_end,
    t_start,
):
    def fr_analysis(
        trials,
        data_truth,
        mode="regular",
        criteria=criteria,
        mn_number=mn_number,
    ):
        """Run the primary firing-rate analysis for one or both selection modes."""
        force_level = 20
        # Compute and compare both selection modes when requested.
        if mode == "combined":
            # HD-sEMG-like selection.
            data_regular = calculate_fr_data(
                trials,
                "regular",
                pd,
                force_level,
                conditions,
                path,
                batch_name,
                t_start,
                t_end,
            )
            # Unfiltered random selection.
            data_random = calculate_fr_data(
                trials,
                "randomly",
                pd,
                force_level,
                conditions,
                path,
                batch_name,
                t_start,
                t_end,
                selection_seed=selection_seeds["randomly"],
            )
            # Plot both modes and report their statistics.
            plot_mn_fr_combined_data(data_regular, data_random, data_truth, conditions, pd)
            print("Selection criteria:", criteria)
            print(f"Random selection seed: {selection_seeds['randomly']}")
            print("=== HD-sEMG MODE ===")
            print_statistics(
                data_regular,
                stats,
                mode="HD-sEMG",
                seed=bootstrap_seeds["HD-sEMG"],
            )
            print("=== RANDOM MODE ===")
            print_statistics(
                data_random,
                stats,
                mode="Random",
                seed=bootstrap_seeds["Random"],
            )
            return data_regular, data_random
    return (fr_analysis,)


@app.cell
def _(data_all, fr_analysis, trials):
    # Compare HD-sEMG and random selection side by side.
    data_regular, data_random = fr_analysis(
        trials=trials,
        data_truth=data_all,
        mode="combined",
    )
    return data_random, data_regular


@app.cell
def _(
    bootstrap_mode,
    bootstrap_seeds,
    data_random,
    data_regular,
    n_resamples,
    pd,
):
    bootstrap_results = pd.DataFrame(
        [
            bootstrap_mode(
                data_regular,
                "HD-sEMG",
                seed=bootstrap_seeds["HD-sEMG"],
                n_resamples=n_resamples,
            ),
            bootstrap_mode(
                data_random,
                "Random",
                seed=bootstrap_seeds["Random"],
                n_resamples=n_resamples,
            ),
        ]
    )
    bootstrap_results
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## HD-sEMG vs filtered-random motor-unit selection

    This sensitivity analysis applies the same eligibility criteria (`ISI CoV < 0.3` and `fmin < FR < fmax`) before selection:

    - **HD-sEMG**: selects the MUs with the lowest firing rates (as in real HD-sEMG decomposition)
    - **Filtered-Random**: randomly selects MUs from those that pass the same filters
    """)
    return


@app.cell
def _(
    batch_name,
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
    trials,
):
    _force_level = 20

    # --- HD-sEMG mode (regular: lowest FR) ---
    _data_hdemg = calculate_fr_data(
        trials,
        "regular",
        pd,
        _force_level,
        conditions,
        path,
        batch_name,
        t_start,
        t_end,
        criteria=criteria,
        mn_number=mn_number,
    )

    # --- Filtered-Random mode (same criteria, random pick) ---
    _data_filtered_random = calculate_fr_data(
        trials,
        "filtered_random",
        pd,
        _force_level,
        conditions,
        path,
        batch_name,
        t_start,
        t_end,
        criteria=criteria,
        mn_number=mn_number,
        selection_seed=selection_seeds["filtered_random"],
    )

    print("=" * 60)
    print("=== HD-sEMG vs FILTERED-RANDOM COMPARISON ===")
    print("=" * 60)
    print(f"Selection criteria: {criteria}")
    print(f"Max MUs selected: {mn_number}")
    print(f"Filtered-random selection seed: {selection_seeds['filtered_random']}")

    print("\n--- HD-sEMG Mode (lowest FR from filtered pool) ---")
    print_statistics(
        _data_hdemg,
        stats,
        mode="HD-sEMG",
        seed=bootstrap_seeds["HD-sEMG"],
    )
    print("\n--- Filtered-Random Mode (random from filtered pool) ---")
    print_statistics(
        _data_filtered_random,
        stats,
        mode="Filtered-Random",
        seed=bootstrap_seeds["Filtered-Random"],
    )
    # Compare modes within each condition.
    print("\n--- Cross-mode comparison (HD-sEMG vs Filtered-Random) ---")
    for _cond in conditions:
        _hdemg_fr = _data_hdemg["mn_rate_trial_mean"][_cond]
        _frand_fr = _data_filtered_random["mn_rate_trial_mean"][_cond]
        _valid_pairs = np.isfinite(_hdemg_fr) & np.isfinite(_frand_fr)
        _hdemg_fr = _hdemg_fr[_valid_pairs]
        _frand_fr = _frand_fr[_valid_pairs]
        if len(_hdemg_fr) > 1:
            _wilcoxon = stats.wilcoxon(
                _hdemg_fr,
                _frand_fr,
                alternative="two-sided",
                method="auto",
            )
            print(
                f"  {_cond} simulation means (n={len(_hdemg_fr)}): FR "
                f"HD-sEMG={_hdemg_fr.mean():.2f}±{_hdemg_fr.std(ddof=1):.2f} vs "
                f"Filtered-Random={_frand_fr.mean():.2f}±{_frand_fr.std(ddof=1):.2f} "
                f"(paired Wilcoxon W={float(_wilcoxon.statistic):.1f}, "
                f"p={float(_wilcoxon.pvalue):.4e})"
            )
    return


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
    _mvc10_trials = np.arange(10)
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
    _mvc50_trials = np.arange(10)
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
    return


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
        color = {conditions[0]: "Blues", conditions[1]: "Oranges"}
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
            cmap=color[conditions[0]],
            vmin=1,
            vmax=250,
        )
        ax.scatter(
            mn_rate_mean_CV[conditions[1]],
            mn_rate_mean_mean[conditions[1]],
            c=neurons_index[conditions[1]],
            cmap=color[conditions[1]],
            vmin=1,
            vmax=250,
        )
        ax.set_xlim(0, 1.4)
        ax.set_ylim(0, 25)
        ax.set_xlabel("ISI CoV", fontsize=fs_label)
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
            cmap=color[conditions[0]],
            vmin=1,
            vmax=250,
        )
        axins2.scatter(
            mn_rate_mean_CV[conditions[1]],
            mn_rate_mean_mean[conditions[1]],
            c=neurons_index[conditions[1]],
            cmap=color[conditions[1]],
            vmin=1,
            vmax=250,
        )
        axins2.set_xlim(0.02, 0.12)
        axins2.set_ylim(12, 22)
        axins2.xaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.yaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.tick_params(axis="both", which="major", labelsize=fs_ticklabels - 2)
        # axins2.grid(True, linestyle="--", alpha=0.7)
        fig.savefig("diabetes/figures/fr_cv_scatter_full.png", bbox_inches="tight")
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
            df.to_csv(f"diabetes/csv_results/fr_cv_{cond}.csv", index=False)
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
    select_mns_regular,
):
    def what_mn_selected(trial, criteria=criteria, mn_number=mn_number):
        """Visualize which motor units the HD-sEMG-like rule selects."""
        import os

        force_level = 20
        t_start = 4000
        t_end = 10000

        # Create one raster panel per condition.
        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

        colors = {condition: "red" for condition in conditions}

        for i, condition in enumerate(conditions):
            data = pd.read_csv(
                f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                delimiter=",",
            )
            data = data.values
            selected_neurons = select_mns_regular(
                data,
                t_start=t_start,
                t_end=t_end,
                criteria=criteria,
                mn_number=mn_number,
            )

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
            ax.set_ylabel("Motor Unit ID", fontsize=fs_label)
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
        fig.savefig(
            f"diabetes/figures/what_mn_selected_combined_trial_{trial}.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.show()
        plt.close(fig)

        print(
            "Motor-unit selection figure saved to: "
            f"diabetes/figures/what_mn_selected_combined_trial_{trial}.png"
        )


    def index_mn_selected(criteria=criteria, mn_number=mn_number):
        """Report the selected motor-unit index range across simulations."""

        force_level = 20
        t_start = 4000
        t_end = 10000

        for condition in conditions:
            min_index = mn_number
            max_index = 0
            for trial in range(50):
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )
                data = data.values
                selected_neurons = select_mns_regular(
                    data,
                    t_start=t_start,
                    t_end=t_end,
                    criteria=criteria,
                    mn_number=mn_number,
                )
                min_index = min(min_index, min(selected_neurons))
                max_index = max(max_index, max(selected_neurons))

            print(f"Condition {condition}: min index={min_index}, max index={max_index}")
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
    def isi_cov_histograms(trials, mode="regular", pd=pd, batch_name=batch_name):
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
            n_bins = np.arange(0, 0.95, 0.05)
            ax.hist(
                cov_data,
                bins=n_bins,
                alpha=0.7,
                color=colors[condition],
                edgecolor="black",
                linewidth=0.5,
            )
            ax.set_xlim(0, 0.9)

            # Shade the region that satisfies the selection threshold.
            ax.axvspan(0, 0.3, alpha=0.3, color=colors[condition], zorder=0)

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
            ax.set_xlabel("ISI CoV", fontsize=fs_label)
            if i == 0:
                ax.set_ylabel("Number of occurrences", fontsize=fs_label)
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

        filename = f"diabetes/figures/isi_cov_histograms_all_units_{mode}_{batch_name}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        print(f"ISI CoV histograms for all motor units saved to: {filename}")
    return (isi_cov_histograms,)


@app.cell
def _(isi_cov_histograms, trials):
    isi_cov_histograms(trials, mode="regular")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Firing rates at other MVC levels (10% and 50%)

    Each force level is evaluated using HD-sEMG selection, seeded Random selection of ten active motor units, and an all-motor-unit reference.
    """)
    return


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
    mvc10_trials = np.arange(10)
    mvc10_batch = "mvc10"
    mvc10_force_level = 10  # int(0.1 * 100)

    print("=" * 60)
    print("=== FIRING RATES AT 10% MVC (batch: mvc10) ===")
    print("=" * 60)

    try:
        # HD-sEMG mode
        data_mvc10_regular = calculate_fr_data(
            mvc10_trials,
            "regular",
            pd,
            mvc10_force_level,
            conditions,
            path,
            mvc10_batch,
            t_start,
            t_end,
            criteria=criteria,
            mn_number=mn_number,
        )
        print("\n--- HD-sEMG Mode ---")
        print("Selection criteria:", criteria)
        print_statistics(
            data_mvc10_regular,
            stats,
            mode="10% MVC HD-sEMG",
            seed=bootstrap_seeds["10% MVC HD-sEMG"],
        )
        # Seeded random selection of ten active motor units
        data_mvc10_random = calculate_fr_data(
            mvc10_trials,
            "randomly",
            pd,
            mvc10_force_level,
            conditions,
            path,
            mvc10_batch,
            t_start,
            t_end,
            mn_number=mn_number,
            selection_seed=selection_seeds["mvc10_randomly"],
        )
        print("\n--- Random Mode ---")
        print(f"Selection seed: {selection_seeds['mvc10_randomly']}")
        print_statistics(
            data_mvc10_random,
            stats,
            mode="10% MVC Random",
            seed=bootstrap_seeds["10% MVC Random"],
        )
        # All motor units
        data_mvc10_all = calculate_fr_data(
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
        print("\n--- All Motor Units ---")
        print_statistics(
            data_mvc10_all,
            stats,
            mode="10% MVC all motor units",
            seed=bootstrap_seeds["10% MVC all motor units"],
        )
    except Exception as e:
        print(f"10% MVC data not yet available: {e}")

    # === Analysis for 50% MVC simulations ===
    mvc50_trials = np.arange(10)
    mvc50_batch = "mvc50"
    mvc50_force_level = 50  # int(0.5 * 100)

    print("\n" + "=" * 60)
    print("=== FIRING RATES AT 50% MVC (batch: mvc50) ===")
    print("=" * 60)

    try:
        # HD-sEMG mode
        data_mvc50_regular = calculate_fr_data(
            mvc50_trials,
            "regular",
            pd,
            mvc50_force_level,
            conditions,
            path,
            mvc50_batch,
            t_start,
            t_end,
            criteria=criteria,
            mn_number=mn_number,
        )
        print("\n--- HD-sEMG Mode ---")
        print("Selection criteria:", criteria)
        print_statistics(
            data_mvc50_regular,
            stats,
            mode="50% MVC HD-sEMG",
            seed=bootstrap_seeds["50% MVC HD-sEMG"],
        )
        # Seeded random selection of ten active motor units
        data_mvc50_random = calculate_fr_data(
            mvc50_trials,
            "randomly",
            pd,
            mvc50_force_level,
            conditions,
            path,
            mvc50_batch,
            t_start,
            t_end,
            mn_number=mn_number,
            selection_seed=selection_seeds["mvc50_randomly"],
        )
        print("\n--- Random Mode ---")
        print(f"Selection seed: {selection_seeds['mvc50_randomly']}")
        print_statistics(
            data_mvc50_random,
            stats,
            mode="50% MVC Random",
            seed=bootstrap_seeds["50% MVC Random"],
        )
        # All motor units
        data_mvc50_all = calculate_fr_data(
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
        print("\n--- All Motor Units ---")
        print_statistics(
            data_mvc50_all,
            stats,
            mode="50% MVC all motor units",
            seed=bootstrap_seeds["50% MVC all motor units"],
        )
    except Exception as e:
        print(f"50% MVC data not yet available: {e}")
    return


if __name__ == "__main__":
    app.run()
