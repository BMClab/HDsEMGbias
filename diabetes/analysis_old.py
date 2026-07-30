import marimo

__generated_with = "0.17.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import os, sys
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
    from matplotlib.ticker import AutoLocator, MaxNLocator
    import pandas as pd
    from scipy.signal import welch, detrend, butter, filtfilt, csd
    from scipy import stats
    import sympy as sym
    from scikit_posthocs import posthoc_dunn
    return MaxNLocator, butter, filtfilt, mo, np, os, pd, plt, stats, sys


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
    markersize2 = 20
    fontweight = "normal"

    t_start = 4000
    t_end = 10000

    criteria = {"fmin": 5, "fmax": 15, "isicv": 0.3}
    # criteria = {"fmin": 0, "fmax": np.inf, "isicv": 0.3}

    mn_number = 10
    return (
        batch_name,
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
        path,
        t_end,
        t_start,
        trials,
    )


@app.cell
def _(
    butter,
    criteria,
    filtfilt,
    fs_label,
    fs_ticklabels,
    fs_title,
    markersize,
    mn_number,
    modes,
    np,
    os,
    plt,
    stats,
):
    def select_mns_randomly(data, t_start, t_end, size=4, column_spikes=1):
        # Filtrar dados da fase de estado estacionário
        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        unique_neurons = np.unique(data[:, 0])
        fr = compute_fr(
            unique_neurons, steady_data, t_start, t_end, column_spikes=column_spikes
        )
        # Seleção dos neurônios
        selected_neurons = unique_neurons
        # selected_neurons = selected_neurons[np.where((fr < 200))[0]].astype(int)
        selected_neurons = np.random.choice(selected_neurons, size=size)

        return selected_neurons


    def select_all_mns(data, t_start, t_end, column_spikes=1):
        """Select all motor units (no filtering criteria)."""
        unique_neurons = np.unique(data[:, 0])
        return unique_neurons.astype(int)


    def select_mns_regular(
        data, t_start, t_end, column_spikes=1, criteria=criteria, mn_number=mn_number
    ):
        # Filtrar dados da fase de estado estacionário
        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        unique_neurons = np.unique(data[:, 0])
        ISI_CV, ISI_mean = compute_cv(
            unique_neurons, steady_data, t_start, t_end, column_spikes=column_spikes
        )
        fr = compute_fr(unique_neurons, data, t_start, t_end, column_spikes=column_spikes)
        # Seleção dos neurônios
        selection_criteria = np.where(
            (fr > criteria["fmin"]) & (fr < criteria["fmax"]) & (ISI_CV <= criteria["isicv"])
        )[0]
        selected_neurons = unique_neurons[selection_criteria].astype(int)
        fr_sel = fr[selection_criteria]
        if len(selected_neurons) > mn_number:
            selected_neurons = selected_neurons[np.argsort(fr_sel)][:mn_number]

        return selected_neurons


    def select_mns_filtered_random(
        data, t_start, t_end, column_spikes=1, criteria=criteria, mn_number=mn_number
    ):
        """Select MUs randomly from those that pass the HD-sEMG-like criteria.
        Same filtering as select_mns_regular (ISI CV, fmin, fmax), but
        randomly picks mn_number MUs instead of selecting by lowest FR."""
        steady_data = data[
            (data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)
        ]
        unique_neurons = np.unique(data[:, 0])
        ISI_CV, ISI_mean = compute_cv(
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
            selected_neurons = np.random.choice(
                selected_neurons, size=mn_number, replace=False
            )

        return selected_neurons


    def compute_fr(selected_neurons, data, t_start, t_end, column_spikes=1):
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


    def plot_mn_fr(mn_rate_mean_mean, mn_rate_mean_CV, conditions, pd, mode):
        os.makedirs("diabetes", exist_ok=True)
        mean_fr = np.hstack(
            (
                np.mean(mn_rate_mean_mean[conditions[0]]),
                np.mean(mn_rate_mean_mean[conditions[1]]),
            )
        )
        sem_fr = np.hstack(
            (
                mn_rate_mean_mean[conditions[0]].std()
                / np.sqrt(len(mn_rate_mean_mean[conditions[0]])),
                mn_rate_mean_mean[conditions[1]].std(ddof=1)
                / np.sqrt(len(mn_rate_mean_mean[conditions[1]])),
            )
        )

        fig, ax = plt.subplots()
        ax.errorbar([1, 2], mean_fr, fmt=".", yerr=sem_fr, capsize=5, color="black")
        ax.grid()
        ax.scatter(
            1 + 0.1 * np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])),
            mn_rate_mean_mean[conditions[0]],
        )
        ax.scatter(
            2 + 0.1 * np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])),
            mn_rate_mean_mean[conditions[1]],
        )
        ax.set_xticks([1, 2])
        ax.set_xticklabels([conditions[0], conditions[1]])
        ax.set_ylabel("MN firing rate (pps)")
        fig.tight_layout()
        fig.savefig(f"diabetes/mn_firing_rate_comparison_{mode}.png")
        plt.close(fig)
        # Salvar dados em CSV
        for cond in conditions:
            df = pd.DataFrame(
                {
                    "firing_rate": mn_rate_mean_mean[cond].flatten(),
                    "ISI_CV": mn_rate_mean_CV[cond].flatten(),
                }
            )
            df.to_csv(f"diabetes/mn_firing_rate_{cond}_{mode}.csv", index=False)

        df_mean = pd.DataFrame(
            {
                "condition": conditions,
                "mean_firing_rate": mean_fr,
                "sem_firing_rate": sem_fr,
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
    ):
        """
        Função auxiliar para calcular dados de firing rate para um modo específico.
        """

        mn_rate_mean_mean = dict()
        mn_rate_mean_CV = dict()
        for condition in conditions_param:
            mn_rate_mean_mean[condition] = np.array([]).reshape(-1, 1)
            mn_rate_mean_CV[condition] = np.array([]).reshape(-1, 1)

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
                    CV_mean = CV_mean + force.std() / force.mean()
                    n = n + 1

                # Selecionar neurônios baseado no modo
                if mode == "randomly":
                    selected_neurons = select_mns_randomly(
                        data, t_start=t_start_param, t_end=t_end_param, size=4
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
                mn_rate_mean_mean[condition] = np.vstack(
                    (mn_rate_mean_mean[condition], mns_rate_mean)
                )
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))

        return {
            "mn_rate_mean_mean": mn_rate_mean_mean,
            "mn_rate_mean_CV": mn_rate_mean_CV,
            "force_mean": force_mean / n if n > 0 else 0,
            "CV_mean": CV_mean / n if n > 0 else 0,
        }


    def plot_mn_fr_combined_data(data_regular, data_random, conditions, pd):
        """
        Função que cria plots lado a lado usando dados pré-calculados com barras de significância.
        """
        import os

        os.makedirs("diabetes", exist_ok=True)

        # Criar figura com 1 linha e 2 colunas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

        def calculate_p_values(mn_data, conditions):
            """Função auxiliar para calcular p-values"""
            p_values = {}
            # Normal vs DPN
            # res = stats.ttest_ind(a=mn_data[conditions[0]], b=mn_data[conditions[-1]])
            statistic, pvalue = stats.mannwhitneyu(
                mn_data[conditions[0]], mn_data[conditions[-1]]
            )
            p_values["normal_vs_DPN"] = pvalue
            # print("Statistics and p-value Mann-Whitney U:", statistic, p_values["normal_vs_DPN"])

            return statistic, p_values

        def add_significance_bars(ax, means, p_values, y_offset=0.5):
            """Função auxiliar para adicionar barras de significância"""
            max_y = max(means) + y_offset

            # Comparação normal vs DPN (posições 1 e 3)
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
                max_y = y_pos + 0.4

            return p_values

        def plot_data(ax, mn_data, title):
            """Função auxiliar para plotar dados"""
            mean_fr = np.hstack(
                (np.mean(mn_data[conditions[0]]), np.mean(mn_data[conditions[1]]))
            )
            sem_fr = np.hstack(
                (
                    mn_data[conditions[0]].std() / np.sqrt(len(mn_data[conditions[0]])),
                    mn_data[conditions[1]].std(ddof=1)
                    / np.sqrt(len(mn_data[conditions[1]])),
                )
            )

            ax.plot(
                [1, 2],
                mean_fr,
                marker="P",
                linestyle="",
                color="black",
                markersize=markersize,
            )
            ax.grid()
            ax.scatter(
                1 + 0.1 * np.random.normal(size=len(mn_data[conditions[0]])),
                mn_data[conditions[0]],
                alpha=0.6,
            )
            ax.scatter(
                2 + 0.1 * np.random.normal(size=len(mn_data[conditions[1]])),
                mn_data[conditions[1]],
                alpha=0.6,
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
                ax.set_ylabel("MN firing rate (pps)", fontsize=fs_label)
                ax.set_yticklabels([0, 5, 10, 15, 20], fontsize=fs_ticklabels)
            ax.set_title(title, fontsize=fs_title)

            # Calcular p-values e adicionar barras de significância
            statistic, p_values = calculate_p_values(mn_data, conditions)
            p_values = add_significance_bars(ax, mean_fr, p_values)

            return mean_fr, sem_fr, statistic, p_values

        # Plot para modo regular (esquerda)
        mean_fr_regular, sem_fr_regular, statistic_regular, p_values_regular = plot_data(
            ax1, data_regular["mn_rate_mean_mean"], f"{modes[0]} Mode"
        )

        # Plot para modo random (direita)
        mean_fr_random, sem_fr_random, statistic_random, p_values_random = plot_data(
            ax2, data_random["mn_rate_mean_mean"], f"{modes[1]} Mode"
        )

        # Adicionar legenda para significância se houver alguma significância
        has_significance = any(p < 0.05 for p in p_values_regular.values()) or any(
            p < 0.05 for p in p_values_random.values()
        )
        # if has_significance:
        #     fig.text(0.5, 0.02, "* p < 0.05, ** p < 0.01, *** p < 0.001",
        #             ha="center", fontsize=10)
        #     fig.subplots_adjust(bottom=0.1)
        # else:
        fig.tight_layout()

        # Salvar figura
        fig.savefig(
            "diabetes/figures/mn_firing_rate_comparison_combined.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close(fig)

        # Salvar dados em CSV para ambos os modos
        for mode, data_dict in [("regular", data_regular), ("random", data_random)]:
            for cond in conditions[::2]:
                df = pd.DataFrame(
                    {
                        "firing_rate": data_dict["mn_rate_mean_mean"][cond].flatten(),
                        "ISI_CV": data_dict["mn_rate_mean_CV"][cond].flatten(),
                    }
                )
                df.to_csv(
                    f"diabetes/csv_results/mn_firing_rate_{cond}_{mode}_combined.csv",
                    index=False,
                )

        # Salvar resumo dos p-values
        p_values_df = pd.DataFrame(
            {
                "comparison": ["normal_vs_DPN"],
                "statistics_regular": [statistic_regular],
                "statistics_random": [statistic_random],
                "p_value_regular": [p_values_regular["normal_vs_DPN"]],
                "p_value_random": [p_values_random["normal_vs_DPN"]],
                "significant_random": [p < 0.05 for p in p_values_random.values()],
            }
        )
        p_values_df.to_csv(
            "diabetes/csv_results/mn_firing_rate_p_values_combined.csv", index=False
        )

        print(
            "Figura combinada com barras de significância salva como: diabetes/mn_firing_rate_comparison_combined.png"
        )
        print("P-values salvos em: diabetes/mn_firing_rate_p_values_combined.csv")


    def print_statistics(mn_rate_mean_mean, conditions_param, stats_module, mn_rate_mean_CV):
        """
        Função auxiliar para imprimir estatísticas.
        """
        print(
            f"FR normal: {mn_rate_mean_mean['normal'].mean():.2f}$\pm$  {mn_rate_mean_mean['normal'].std(ddof=1):.2f}, FR DPN: {mn_rate_mean_mean['DPN'].mean():.2f} $\pm$ {mn_rate_mean_mean['DPN'].std():.2f}"
        )

        print(
            f"ISI CV normal: {mn_rate_mean_CV['normal'].mean():.2f}$\pm$  {mn_rate_mean_CV['normal'].std(ddof=1):.2f}, ISI CV DPN: {mn_rate_mean_CV['DPN'].mean():.2f} $\pm$ {mn_rate_mean_CV['DPN'].std():.2f}"
        )
        # statistic_ind, p_value_ind = stats_module.ttest_ind(a=mn_rate_mean_mean[conditions_param[0]], b=mn_rate_mean_mean[conditions_param[1]])
        # print("p-value normal-DPN:", p_value_ind)
        statistic, p_value_ind = stats.mannwhitneyu(
            mn_rate_mean_mean[conditions_param[0]], mn_rate_mean_mean[conditions_param[1]]
        )
        print("Statistics and p-value Mann-Whitney U:", statistic, p_value_ind)


    def firing_rate(
        spiketrains, delta_t=0.00005, filtro_ordem=4, freq_corte=0.001, tempo_max=1000
    ):
        """
        Função que gera o impulso de Dirac para os tempos de disparo de um neurônio.

        Parâmetros:
            spiketrains: Lista com os trens de disparo de neurônios.
            neuronio: Índice do neurônio a ser processado.
            delta_t: Intervalo de tempo.
            filtro_ordem : Ordem do filtro Butterworth.
            freq_corte: Frequência de corte normalizada para o filtro Butterworth.
            tempo_max: Tempo máximo para o eixo x (em milissegundos).
        """

        # Criação do vetor de tempo
        t = np.arange(0, tempo_max, delta_t)
        fr = np.zeros_like(t)

        # Adiciona o impulso de Dirac em cada tempo de disparo do neurônio
        idx = np.searchsorted(t, spiketrains / 1000)
        idx = idx[idx < len(fr)]
        fr[idx] = 1 / delta_t
        # Filtro Butterworth
        fs = 1 / delta_t
        b, a = butter(filtro_ordem, freq_corte / (fs / 2))

        # Aplicação do filtro
        fr = filtfilt(b, a, fr)
        fr[fr < 0] = 0
        return fr, t
    return (
        calculate_fr_data,
        compute_cv,
        compute_fr,
        plot_mn_fr,
        plot_mn_fr_combined_data,
        print_statistics,
        select_all_mns,
        select_mns_randomly,
        select_mns_regular,
    )


@app.cell
def _(
    batch_name,
    calculate_fr_data,
    compute_cv,
    compute_fr,
    conditions,
    criteria,
    mn_number,
    np,
    path,
    pd,
    plot_mn_fr,
    plot_mn_fr_combined_data,
    print_statistics,
    select_all_mns,
    select_mns_randomly,
    select_mns_regular,
    stats,
    t_end,
    t_start,
):
    def fr_analysis(trials, mode="regular", criteria=criteria, mn_number=mn_number):
        force_level = 20

        # Se mode for 'combined', calcular dados para ambos os modos
        if mode == "combined":
            # Calcular dados para modo regular
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
            # Calcular dados para modo random
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
            )
            # Criar plots combinados
            plot_mn_fr_combined_data(data_regular, data_random, conditions, pd)
            # Imprimir estatísticas para ambos os modos
            print("Selection criteria:", criteria)
            print("=== MODO HD-sEMG ===")
            print_statistics(
                data_regular["mn_rate_mean_mean"],
                conditions,
                stats,
                data_regular["mn_rate_mean_CV"],
            )
            print("=== MODO RANDOM ===")
            print_statistics(
                data_random["mn_rate_mean_mean"],
                conditions,
                stats,
                data_regular["mn_rate_mean_CV"],
            )
            return

        # Modo individual (regular ou randomly)
        mn_rate_mean_mean = dict()
        mn_rate_mean_mean[conditions[0]] = np.array([]).reshape(-1, 1)
        mn_rate_mean_mean[conditions[1]] = np.array([]).reshape(-1, 1)
        mn_rate_mean_CV = dict()
        mn_rate_mean_CV[conditions[0]] = np.array([]).reshape(-1, 1)
        mn_rate_mean_CV[conditions[1]] = np.array([]).reshape(-1, 1)
        force_mean = 0
        CV_mean = 0
        n = 0
        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )
                force = pd.read_csv(
                    f"{path}force_{condition}_{trial}_{batch_name}/force_ref{force_level}.csv",
                    delimiter=",",
                ).values
                data = data.values
                if condition == "DPN":
                    force = force[force[:, 0] > t_start, 1]
                    force_mean = force_mean + force
                    CV_mean = CV_mean + force.std() / force.mean()
                    n = n + 1
                if mode == "randomly":
                    selected_neurons = select_mns_randomly(
                        data, t_start=t_start, t_end=t_end, size=4
                    )
                if mode == "regular":
                    selected_neurons = select_mns_regular(
                        data,
                        t_start=t_start,
                        t_end=t_end,
                        criteria=criteria,
                        mn_number=mn_number,
                    )
                if mode == "all":
                    selected_neurons = select_all_mns(data, t_start=t_start, t_end=t_end)
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)
                ISI_CV = ISI_CV[mns_rate_mean >= 0.01].reshape(-1, 1)
                mns_rate_mean = mns_rate_mean[mns_rate_mean >= 0.01].reshape(-1, 1)
                mn_rate_mean_mean[condition] = np.vstack(
                    (mn_rate_mean_mean[condition], mns_rate_mean)
                )
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))
        force_mean = force_mean / n
        unique_neurons = np.unique(data[:, 0])
        ISI_CV_all, _ = compute_cv(unique_neurons, data, t_start, t_end)
        print("Mean force: ", force_mean.mean(), "CV force:", CV_mean)
        data = np.hstack((data, np.zeros((len(data), 1))))
        for i in unique_neurons:
            data[data[:, 0] == int(i), 2] = ISI_CV_all[unique_neurons == int(i)]

        plot_mn_fr(mn_rate_mean_mean, mn_rate_mean_CV, conditions, pd, mode)

        print(
            f"FR normal: {mn_rate_mean_mean['normal'].mean():.2f}({mn_rate_mean_mean['normal'].std():.2f}), FR DPN: {mn_rate_mean_mean['DPN'].mean():.2f}({mn_rate_mean_mean['DPN'].std():.2f})"
        )
        t_statistic_ind, p_value_ind = stats.ttest_ind(
            a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[1]]
        )
        print("p-value t-test:", p_value_ind)

        statistic, p_value_ind = stats.mannwhitneyu(
            mn_rate_mean_mean[conditions[0]], mn_rate_mean_mean[conditions[1]]
        )
        print("Statistics and p-value Mann-Whitney U:", statistic, p_value_ind)
    return (fr_analysis,)


@app.cell
def _(fr_analysis, trials):
    # Criar figura combinada com regular e random lado a lado
    # fr_analysis(trials=trials, mode="combined")
    fr_analysis(trials=trials, mode="combined")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## HD-sEMG vs Filtered-Random MU Selection Comparison

    Compares two selection strategies that apply the same filtering criteria (ISI CV < 0.3, fmin < FR < fmax):
    - **HD-sEMG**: selects the MUs with the lowest firing rates (as in real HD-sEMG decomposition)
    - **Filtered-Random**: randomly selects MUs from those that pass the same filters
    """)
    return


@app.cell
def _(
    batch_name,
    calculate_fr_data,
    conditions,
    criteria,
    mn_number,
    path,
    pd,
    print_statistics,
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
    )

    print("=" * 60)
    print("=== HD-sEMG vs FILTERED-RANDOM COMPARISON ===")
    print("=" * 60)
    print(f"Selection criteria: {criteria}")
    print(f"Max MUs selected: {mn_number}")

    print("\n--- HD-sEMG Mode (lowest FR from filtered pool) ---")
    print_statistics(
        _data_hdemg["mn_rate_mean_mean"], conditions, stats, _data_hdemg["mn_rate_mean_CV"]
    )
    print(
        f"Number of MUs — normal: {len(_data_hdemg['mn_rate_mean_mean']['normal'])}, "
        f"DPN: {len(_data_hdemg['mn_rate_mean_mean']['DPN'])}"
    )

    print("\n--- Filtered-Random Mode (random from filtered pool) ---")
    print_statistics(
        _data_filtered_random["mn_rate_mean_mean"],
        conditions,
        stats,
        _data_filtered_random["mn_rate_mean_CV"],
    )
    print(
        f"Number of MUs — normal: {len(_data_filtered_random['mn_rate_mean_mean']['normal'])}, "
        f"DPN: {len(_data_filtered_random['mn_rate_mean_mean']['DPN'])}"
    )

    # --- Cross-mode comparison (within each condition) ---
    print("\n--- Cross-mode comparison (HD-sEMG vs Filtered-Random) ---")
    for _cond in conditions:
        _hdemg_fr = _data_hdemg["mn_rate_mean_mean"][_cond].ravel()
        _frand_fr = _data_filtered_random["mn_rate_mean_mean"][_cond].ravel()
        if len(_hdemg_fr) > 0 and len(_frand_fr) > 0:
            _stat, _p = stats.mannwhitneyu(_hdemg_fr, _frand_fr)
            print(
                f"  {_cond}: FR HD-sEMG={_hdemg_fr.mean():.2f}±{_hdemg_fr.std():.2f} vs "
                f"Filtered-Random={_frand_fr.mean():.2f}±{_frand_fr.std():.2f} "
                f"(Mann-Whitney U={float(_stat):.1f}, p={float(_p):.4e})"
            )
    return


@app.cell
def _(
    batch_name,
    calculate_fr_data,
    conditions,
    np,
    path,
    pd,
    print_statistics,
    stats,
    t_end,
    t_start,
    trials,
):
    # === Analysis for ALL motor units (numbers only, no plots) ===
    print("=" * 60)
    print("=== ALL MOTOR UNITS (no selection criteria) ===")
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
        data_all["mn_rate_mean_mean"], conditions, stats, data_all["mn_rate_mean_CV"]
    )
    print(
        f"\nNumber of MUs — normal: {len(data_all['mn_rate_mean_mean']['normal'])}, "
        f"DPN: {len(data_all['mn_rate_mean_mean']['DPN'])}"
    )
    print(
        f"Mean force (DPN): {data_all['force_mean'].mean():.4f}"
        if isinstance(data_all["force_mean"], np.ndarray)
        else ""
    )
    print(
        f"CV force (DPN): {data_all['CV_mean']:.4f}"
        if isinstance(data_all["CV_mean"], float)
        else ""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Force Production Statistics
    """)
    return


@app.cell
def _(batch_name, conditions, np, path, pd, stats, t_start, trials):
    def compute_force_statistics(
        trials_param,
        batch_name_param,
        force_level,
        conditions_param,
        path_param,
        t_start_param,
        MVC=300,
    ):
        """
        Compute force statistics for each trial and condition.
        Returns per-trial mean force, CV, and aggregated statistics.
        """
        results = {}
        for condition in conditions_param:
            trial_means = []
            trial_cvs = []
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

                    mean_f = force_steady.mean()
                    cv_f = force_steady.std() / mean_f if mean_f > 0 else np.nan
                    trial_means.append(mean_f)
                    trial_cvs.append(cv_f)
                except Exception:
                    continue

            trial_means = np.array(trial_means)
            trial_cvs = np.array(trial_cvs)

            # 95% CI using t-distribution
            n = len(trial_means)
            if n > 1:
                from scipy.stats import t as t_dist

                ci_factor = t_dist.ppf(0.975, n - 1)

                mean_of_means = trial_means.mean()
                sd_of_means = trial_means.std(ddof=1)
                se_means = sd_of_means / np.sqrt(n)
                ci_means = (
                    mean_of_means - ci_factor * se_means,
                    mean_of_means + ci_factor * se_means,
                )

                mean_of_cvs = trial_cvs.mean()
                sd_of_cvs = trial_cvs.std(ddof=1)
                se_cvs = sd_of_cvs / np.sqrt(n)
                ci_cvs = (mean_of_cvs - ci_factor * se_cvs, mean_of_cvs + ci_factor * se_cvs)
            else:
                mean_of_means = trial_means.mean() if n > 0 else np.nan
                sd_of_means = 0
                ci_means = (np.nan, np.nan)
                mean_of_cvs = trial_cvs.mean() if n > 0 else np.nan
                sd_of_cvs = 0
                ci_cvs = (np.nan, np.nan)

            results[condition] = {
                "trial_means": trial_means,
                "trial_cvs": trial_cvs,
                "mean_force": mean_of_means,
                "sd_force": sd_of_means,
                "ci_force": ci_means,
                "mean_cv": mean_of_cvs,
                "sd_cv": sd_of_cvs,
                "ci_cv": ci_cvs,
                "n_trials": n,
                "mean_force_pct_mvc": mean_of_means / MVC * 100,
            }
        return results


    def print_force_stats(results, conditions_param, label=""):
        """Print force statistics in the format requested by reviewer."""
        print(f"\n{'=' * 60}")
        print(f"=== FORCE PRODUCTION STATISTICS {label} ===")
        print(f"{'=' * 60}")
        print(f"(Steady-state: t > {t_start} ms)")

        for condition in conditions_param:
            r = results[condition]
            print(f"\n--- {condition} (n={r['n_trials']} trials) ---")
            print(
                f"  Mean force: {r['mean_force']:.4f} ({r['sd_force']:.4f}) "
                f"[95% CI: {r['ci_force'][0]:.4f}, {r['ci_force'][1]:.4f}]"
            )
            print(f"  Force as %MVC: {r['mean_force_pct_mvc']:.2f}%")
            print(
                f"  CV of force: {r['mean_cv']:.4f} ({r['sd_cv']:.4f}) "
                f"[95% CI: {r['ci_cv'][0]:.4f}, {r['ci_cv'][1]:.4f}]"
            )

        # Between-conditions comparison
        if all(len(results[c]["trial_means"]) > 0 for c in conditions_param):
            stat_force, p_force = stats.mannwhitneyu(
                results[conditions_param[0]]["trial_means"],
                results[conditions_param[1]]["trial_means"],
            )
            stat_cv, p_cv = stats.mannwhitneyu(
                results[conditions_param[0]]["trial_cvs"],
                results[conditions_param[1]]["trial_cvs"],
            )
            print(
                f"\n--- Between-conditions comparison ({conditions_param[0]} vs {conditions_param[1]}) ---"
            )
            print(f"  Mean force: Mann-Whitney U={stat_force:.1f}, p={p_force:.4e}")
            print(f"  CV of force: Mann-Whitney U={stat_cv:.1f}, p={p_cv:.4e}")

        # Between-trials variability (within each condition)
        print(f"\n--- Between-trials variability ---")
        for condition in conditions_param:
            r = results[condition]
            if r["n_trials"] > 1:
                cv_between_trials_force = (
                    r["sd_force"] / r["mean_force"] * 100 if r["mean_force"] > 0 else np.nan
                )
                cv_between_trials_cv = (
                    r["sd_cv"] / r["mean_cv"] * 100 if r["mean_cv"] > 0 else np.nan
                )
                print(
                    f"  {condition}: CV of mean force across trials = {cv_between_trials_force:.2f}%"
                )
                print(
                    f"  {condition}: CV of force-CV across trials = {cv_between_trials_cv:.2f}%"
                )


    # === 20% MVC (main batch) ===
    force_level_20 = 20
    try:
        results_20 = compute_force_statistics(
            trials, batch_name, force_level_20, conditions, path, t_start, MVC=300
        )
        print_force_stats(results_20, conditions, label="(20% MVC, batch: variability)")
    except Exception as e:
        print(f"20% MVC force data error: {e}")

    # === 10% MVC ===
    _mvc10_trials = np.arange(10)
    _force_level_10 = 10
    try:
        _results_10 = compute_force_statistics(
            _mvc10_trials, "mvc10", _force_level_10, conditions, path, t_start, MVC=300
        )
        print_force_stats(_results_10, conditions, label="(10% MVC, batch: mvc10)")
    except Exception as e:
        print(f"10% MVC force data not yet available: {e}")

    # === 50% MVC ===
    _mvc50_trials = np.arange(10)
    _force_level_50 = 50
    try:
        _results_50 = compute_force_statistics(
            _mvc50_trials, "mvc50", _force_level_50, conditions, path, t_start, MVC=300
        )
        print_force_stats(_results_50, conditions, label="(50% MVC, batch: mvc50)")
    except Exception as e:
        print(f"50% MVC force data not yet available: {e}")
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
    t_end,
    t_start,
):
    def fr_cv(trials, pd=pd):
        import os

        force_level = 20

        mn_rate_mean_mean = dict()
        mn_rate_mean_mean[conditions[0]] = np.array([]).reshape(-1, 1)
        mn_rate_mean_mean[conditions[1]] = np.array([]).reshape(-1, 1)

        mn_rate_mean_CV = dict()
        mn_rate_mean_CV[conditions[0]] = np.array([]).reshape(-1, 1)
        mn_rate_mean_CV[conditions[1]] = np.array([]).reshape(-1, 1)

        color = dict()
        color[conditions[0]] = "Blues"
        color[conditions[1]] = "Oranges"

        neurons_index = dict()
        neurons_index[conditions[0]] = np.array([]).reshape(-1, 1)
        neurons_index[conditions[1]] = np.array([]).reshape(-1, 1)

        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )

                data = data.values

                selected_neurons = select_mns_randomly(
                    data, t_start=t_start, t_end=t_end, size=100
                )
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)
                ISI_CV = ISI_CV[mns_rate_mean >= 0.01].reshape(-1, 1)
                selected_neurons = selected_neurons[mns_rate_mean >= 0.01].reshape(-1, 1)

                # print(ISI_CV)

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

        # expdata = pd.read_csv("./diabetes/results/atistics.csv")
        # data_muscle = expdata.query('Muscle == "FDI"')

        fig, ax = plt.subplots(figsize=(12, 8))
        # Plot principal
        s0 = ax.scatter(
            mn_rate_mean_CV[conditions[0]],
            mn_rate_mean_mean[conditions[0]],
            c=neurons_index[conditions[0]],
            cmap=color[conditions[0]],
            vmin=1,
            vmax=250,
        )
        s2 = ax.scatter(
            mn_rate_mean_CV[conditions[1]],
            mn_rate_mean_mean[conditions[1]],
            c=neurons_index[conditions[1]],
            cmap=color[conditions[1]],
            vmin=1,
            vmax=250,
        )
        # ax.scatter(data_muscle['ISI CV'], 1/data_muscle['ISI mean'], color='m')
        ax.set_xlim(0, 1.4)
        ax.set_ylim(0, 25)
        ax.set_xlabel("ISI CoV", fontsize=fs_label)
        ax.set_ylabel("Mean firing rate (pps)", fontsize=fs_label)
        ax.tick_params(axis="both", labelsize=fs_ticklabels)
        ax.grid(True, linestyle="--", alpha=0.7)
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
        # Inset 1 (zoom1)

        # axins1 = fig.add_axes([0.53, 0.3, 0.35, 0.25])  # [left, bottom, width, height]
        # axins1.scatter(
        #     mn_rate_mean_CV[conditions[0]],
        #     mn_rate_mean_mean[conditions[0]],
        #     c=neurons_index[conditions[0]],
        #     cmap=color[conditions[0]],
        #     vmin=1,
        #     vmax=250,
        # )
        # axins1.scatter(
        #     mn_rate_mean_CV[conditions[2]],
        #     mn_rate_mean_mean[conditions[2]],
        #     c=neurons_index[conditions[2]],
        #     cmap=color[conditions[2]],
        #     vmin=1,
        #     vmax=250,
        # )
        # axins1.set_xlim(0, 0.3)
        # axins1.set_ylim(5, 15)
        # #axins1.set_xlabel("CV", fontsize=fs_label-2)
        # #axins1.set_ylabel("FR", fontsize=fs_label-2)
        # axins1.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # axins1.tick_params(axis="both", which="major", labelsize=fs_ticklabels-2)
        # axins1.grid(True, linestyle="--", alpha=0.7)
        # Inset 2 (zoom2)
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
        # axins2.set_xlabel("CV", fontsize=fs_label-2)
        # axins2.set_ylabel("FR", fontsize=fs_label-2)
        axins2.xaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.yaxis.set_major_locator(MaxNLocator(nbins=5))
        axins2.tick_params(axis="both", which="major", labelsize=fs_ticklabels - 2)
        axins2.grid(True, linestyle="--", alpha=0.7)
        fig.savefig("diabetes/figures/fr_cv_scatter_full.png", bbox_inches="tight")
        plt.show()
        # plt.close(fig)
        # Save data in CSV
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
        import os

        force_level = 20
        t_start = 4000
        t_end = 10000

        # Criar figura com 3 subplots verticais
        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

        # Cores para destacar os neurônios selecionados
        colors = {
            conditions[0]: "red",  # normal - azul
            conditions[1]: "red",  # DPN - green
        }

        for i, condition in enumerate(conditions):
            data = pd.read_csv(
                f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                delimiter=",",
            )
            data = data.values
            selected_neurons = select_mns_regular(
                data, t_start=t_start, t_end=t_end, criteria=criteria, mn_number=mn_number
            )

            ax = axes[i]

            # Plot todos os neurônios em cinza claro
            ax.plot(
                data[:, 1],
                data[:, 0],
                linestyle="",
                marker=".",
                color=[0.7, 0.7, 0.7],
                markersize=4,
                alpha=0.8,
            )

            # Plot neurônios selecionados em cor destacada
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

            # Adicionar linha vertical tracejada vermelha em 4000 ms
            ax.axvline(
                x=4000,
                color="blue",
                linestyle="--",
                linewidth=2,
                alpha=0.8,
                label="Start of analysis (4000 ms)",
            )

            # Configurar o subplot
            ax.set_title(
                f"{condition.replace('_', ' ').title() if condition != 'DPN' else 'DPN'}",
                fontsize=fs_title,
                fontweight=fontweight,
            )
            ax.set_ylabel("Motor Unit ID", fontsize=fs_label)
            ax.tick_params(axis="both", labelsize=fs_ticklabels)
            ax.grid(True, alpha=0.3)

            # Adicionar legenda apenas no primeiro subplot
            if i == 0:
                ax.legend(loc="upper right", fontsize=fs_legend)

            # Configurar limites do eixo x para mostrar toda a simulação
            ax.set_xlim(0, data[:, 1].max())

        # Configurar xlabel apenas no último subplot
        axes[-1].set_xlabel("Time (ms)", fontsize=fs_label)

        # Título geral da figura

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(top=0.93)  # Espaço para o título geral

        # Salvar figura
        os.makedirs("diabetes/figures", exist_ok=True)
        fig.savefig(
            f"diabetes/figures/what_mn_selected_combined_trial_{trial}.png",
            dpi=300,
            bbox_inches="tight",
        )

        # Mostrar figura
        plt.show()
        plt.close(fig)

        print(
            f"Figura combinada salva como: diabetes/figures/what_mn_selected_combined_trial_{trial}.png"
        )


    def index_mn_selected(criteria=criteria, mn_number=mn_number):
        import os

        force_level = 20
        t_start = 4000
        t_end = 10000

        # Criar figura com 3 subplots verticais

        for i, condition in enumerate(conditions):
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
                if min(selected_neurons) < min_index:
                    min_index = min(selected_neurons)
                if max(selected_neurons) > max_index:
                    max_index = max(selected_neurons)

            print(f"Condition {condition}: min index={min_index}, max index - {max_index}")
    return index_mn_selected, what_mn_selected


@app.cell
def _(what_mn_selected):
    what_mn_selected(30)
    return


@app.cell
def _(index_mn_selected):
    index_mn_selected()
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
    modes,
    np,
    path,
    pd,
    plt,
    t_end,
    t_start,
):
    def isi_cov_histograms(trials, mode="regular", pd=pd, batch_name=batch_name, stats=None):
        """
        Função que cria histogramas do CoV dos ISI de TODOS os motor units nas três condições.
        Três histogramas lado a lado com as mesmas cores dos gráficos de firing rate.
        Destaca a área com CoV < 0.3 com transparência da cor do histograma.

        Args:
            trials: lista de trials para análise
            mode: 'regular' ou 'random'
            pd: pandas module
            batch_name: nome do batch (default: 'variability')
            stats: scipy.stats module (não usado, mantido para compatibilidade)
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Cores das condições (mesmas dos gráficos de firing rate)
        colors = {
            conditions[0]: (0.0039, 0.451, 0.698),  # normal - azul
            conditions[1]: (0.0078, 0.6196, 0.451),  # DPN - green
        }

        # Coletar dados de CoV de TODOS os motor units (não apenas selecionados)
        force_level = 20
        all_cov_data = {condition: [] for condition in conditions}

        for trial in trials:
            for condition in conditions:
                # Carregar dados de spike
                data = pd.read_csv(
                    f"{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv",
                    delimiter=",",
                )
                data = data.values

                # Computar CV para TODOS os neurônios (não usar seleção)
                all_neurons = np.unique(data[:, 0])  # Todos os IDs de neurônios
                ISI_CV, _ = compute_cv(all_neurons, data, t_start, t_end)

                # Filtrar dados válidos
                valid_mask = ISI_CV > 0
                valid_cov = ISI_CV[valid_mask]

                # Adicionar aos dados da condição
                all_cov_data[condition].extend(valid_cov)

        # Criar figura com 3 subplots lado a lado
        fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12, 5))

        # Para cada condição
        for i, condition in enumerate(conditions):
            ax = axes[i]

            # Dados de CoV para esta condição
            cov_data = np.array(all_cov_data[condition])

            # Criar histograma
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

            # Adicionar área sombreada para CoV < 0.3 com transparência da mesma cor
            ax.axvspan(0, 0.3, alpha=0.3, color=colors[condition], zorder=0)

            # Contar neurônios com CoV < 0.3
            count_low_cov = np.sum(cov_data < 0.3)
            total_neurons = len(cov_data)

            # Adicionar texto com contagem
            ax.text(
                0.45,
                0.9,
                f"CoV < 0.3: {count_low_cov}/{total_neurons}",
                transform=ax.transAxes,
                fontsize=fs_legend,
                # bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )

            # Labels e formatação
            ax.set_xlabel("ISI CoV", fontsize=fs_label)
            if i == 0:
                ax.set_ylabel("Number of occurences", fontsize=fs_label)
            ax.set_title(
                f"{condition.replace('_', ' ').title() if condition != 'DPN' else 'DPN'}",
                fontsize=fs_title,
                fontweight=fontweight,
            )
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.tick_params(axis="both", labelsize=fs_ticklabels)
            ax.grid(True, alpha=0.3)

            # Adicionar linha vertical em CoV = 0.3 para referência
            ax.axvline(x=0.3, color="red", linestyle="--", alpha=0.8, linewidth=2)

        # Título geral
        mode_title = f"{modes[0]} Mode" if mode == "regular" else f"{modes[1]} Mode"

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)

        # Salvar figura
        filename = f"diabetes/figures/isi_cov_histograms_all_units_{mode}_{batch_name}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        print(f"Histogramas de CoV dos ISI (todos os motor units) salvos como: {filename}")
    return (isi_cov_histograms,)


@app.cell
def _(isi_cov_histograms, trials):
    isi_cov_histograms(trials, mode="regular")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Firing Rate Analysis at Different MVC Levels (10% and 50%)
    """)
    return


@app.cell
def _(
    calculate_fr_data,
    conditions,
    criteria,
    mn_number,
    np,
    path,
    pd,
    print_statistics,
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
            data_mvc10_regular["mn_rate_mean_mean"],
            conditions,
            stats,
            data_mvc10_regular["mn_rate_mean_CV"],
        )
        print(
            f"Number of MUs — normal: {len(data_mvc10_regular['mn_rate_mean_mean']['normal'])}, "
            f"DPN: {len(data_mvc10_regular['mn_rate_mean_mean']['DPN'])}"
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
            data_mvc10_all["mn_rate_mean_mean"],
            conditions,
            stats,
            data_mvc10_all["mn_rate_mean_CV"],
        )
        print(
            f"Number of MUs — normal: {len(data_mvc10_all['mn_rate_mean_mean']['normal'])}, "
            f"DPN: {len(data_mvc10_all['mn_rate_mean_mean']['DPN'])}"
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
            data_mvc50_regular["mn_rate_mean_mean"],
            conditions,
            stats,
            data_mvc50_regular["mn_rate_mean_CV"],
        )
        print(
            f"Number of MUs — normal: {len(data_mvc50_regular['mn_rate_mean_mean']['normal'])}, "
            f"DPN: {len(data_mvc50_regular['mn_rate_mean_mean']['DPN'])}"
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
            data_mvc50_all["mn_rate_mean_mean"],
            conditions,
            stats,
            data_mvc50_all["mn_rate_mean_CV"],
        )
        print(
            f"Number of MUs — normal: {len(data_mvc50_all['mn_rate_mean_mean']['normal'])}, "
            f"DPN: {len(data_mvc50_all['mn_rate_mean_mean']['DPN'])}"
        )
    except Exception as e:
        print(f"50% MVC data not yet available: {e}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
