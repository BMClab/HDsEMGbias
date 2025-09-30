import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import sys
    sys.path.append('./../')
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    from scipy.signal import welch, detrend, butter, filtfilt, csd
    import sympy as sym
    import scipy
    import scipy.stats as stats
    from scikit_posthocs import posthoc_dunn


    path = 'diabetes/results/'
    batch_name = 'variability1'
    trials = np.arange(50)



    trials_long = np.arange(1, 5)

    conditions = ['normal', 'low_affected', 'severe']

    t_start = 4000
    t_end = 10000
    return (
        batch_name,
        butter,
        conditions,
        csd,
        detrend,
        filtfilt,
        np,
        path,
        pd,
        plt,
        posthoc_dunn,
        scipy,
        stats,
        t_end,
        t_start,
        trials_long,
        welch,
    )


@app.cell
def _(butter, filtfilt, np, plt):
    def select_mns_randomly(data, t_start, t_end, size=4, column_spikes=1):
        steady_data = data[(data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)]
        unique_neurons = np.unique(data[:, 0])
        fr = compute_fr(unique_neurons, steady_data, t_start, t_end, column_spikes=column_spikes)
        # Filtrar dados da fase de estado estacionário

        # Seleção dos neurônios
        selected_neurons = unique_neurons
        # selected_neurons = selected_neurons[np.where((fr < 200))[0]].astype(int)
        selected_neurons = np.random.choice(selected_neurons, size=size)

        return selected_neurons




    def select_mns_regular(data, t_start, t_end, column_spikes=1):
        unique_neurons = np.unique(data[:, 0])

        # Filtrar dados da fase de estado estacionário
        steady_data = data[(data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)]
        ISI_CV, ISI_mean = compute_cv(unique_neurons, steady_data, t_start, t_end, column_spikes=column_spikes)

        fr = compute_fr(unique_neurons, data, t_start, t_end, column_spikes=column_spikes)

        # Seleção dos neurônios

        selection_criteria = np.where((fr > 5) & (fr < 15) & (ISI_CV <=0.3))[0]
        selected_neurons = unique_neurons[selection_criteria].astype(int)
        fr = fr[selection_criteria]
        mn_number =6#int(min(np.random.randint(low=4, high=12, size=1)[0], len(fr)))
        if len(selected_neurons) > mn_number:
             selected_neurons = selected_neurons[np.argsort(fr)][:mn_number]
        # print(ISI_CV[selection_criteria])
        return selected_neurons

    def compute_fr(selected_neurons, data, t_start, t_end, column_spikes=1):
        window_duration = (t_end - t_start) / 1000  # s
        steady_data = data[(data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)]
        firing_rates = np.zeros(len(selected_neurons))
        i = 0
        for neuron in selected_neurons:
            n_spikes = np.sum(steady_data[:, 0] == neuron)
            fr = n_spikes / window_duration
            firing_rates[i] = fr
            i = i + 1
        return firing_rates

    def compute_mn_cv(spike_times, t_start):
        ISI = np.diff(spike_times[spike_times> t_start])
        if len(ISI)>3:
            ISI_SD = ISI.std(ddof=1)
            ISI_mean = ISI.mean()
            ISI_CV = ISI_SD/ISI_mean
        else:
            ISI_mean = 0
            ISI_CV = 1
        return ISI_CV, ISI_mean

    def compute_cv(selected_neurons, data, t_start, t_end, column_spikes=1):
        steady_data = data[(data[:, column_spikes] >= t_start) & (data[:, column_spikes] <= t_end)]
        ISI_CV = np.zeros(len(selected_neurons))
        ISI_mean = np.zeros(len(selected_neurons))
        i = 0
        for neuron in selected_neurons:
            ISI_CV[i], ISI_mean[i] = compute_mn_cv(steady_data[steady_data[:, 0] == neuron, column_spikes], t_start=t_start)
            i = i + 1

        return ISI_CV, ISI_mean


    def plot_mn_fr_combined(mn_rate_mean_mean_regular, mn_rate_mean_CV_regular,
                           mn_rate_mean_mean_randomly, mn_rate_mean_CV_randomly,
                           conditions, pd, stats, p_values_regular, p_values_randomly):
        import os
        os.makedirs('diabetes/figuras', exist_ok=True)

        # Calcular estatísticas para ambos os modos
        mean_fr_regular = np.hstack((np.mean(mn_rate_mean_mean_regular[conditions[0]]),
                                   np.mean(mn_rate_mean_mean_regular[conditions[1]]),
                                   np.mean(mn_rate_mean_mean_regular[conditions[2]])))
        sem_fr_regular = np.hstack((mn_rate_mean_mean_regular[conditions[0]].std()/np.sqrt(len(mn_rate_mean_mean_regular[conditions[0]])),
                                  mn_rate_mean_mean_regular[conditions[1]].std()/np.sqrt(len(mn_rate_mean_mean_regular[conditions[1]])),
                                  mn_rate_mean_mean_regular[conditions[2]].std(ddof=1)/np.sqrt(len(mn_rate_mean_mean_regular[conditions[2]]))))

        mean_fr_randomly = np.hstack((np.mean(mn_rate_mean_mean_randomly[conditions[0]]),
                                    np.mean(mn_rate_mean_mean_randomly[conditions[1]]),
                                    np.mean(mn_rate_mean_mean_randomly[conditions[2]])))
        sem_fr_randomly = np.hstack((mn_rate_mean_mean_randomly[conditions[0]].std()/np.sqrt(len(mn_rate_mean_mean_randomly[conditions[0]])),
                                   mn_rate_mean_mean_randomly[conditions[1]].std()/np.sqrt(len(mn_rate_mean_mean_randomly[conditions[1]])),
                                   mn_rate_mean_mean_randomly[conditions[2]].std(ddof=1)/np.sqrt(len(mn_rate_mean_mean_randomly[conditions[2]]))))

        # Criar figura com dois subplots lado a lado
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Função para adicionar indicações de significância
        def add_significance_bars(ax, means, p_values, y_offset=0.5):
            max_y = max(means) + y_offset

            # Comparação normal vs severe (posições 1 e 3)
            if p_values['normal_vs_severe'] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([1, 3], [y_pos, y_pos], 'k-', linewidth=1)
                ax.plot([1, 1], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                ax.plot([3, 3], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                significance = '***' if p_values['normal_vs_severe'] < 0.001 else '**' if p_values['normal_vs_severe'] < 0.01 else '*'
                ax.text(2, y_pos + 0.1, significance, ha='center', va='bottom', fontweight='bold')
                max_y = y_pos + 0.4

            # Comparação low_affected vs severe (posições 2 e 3)
            if p_values['low_affected_vs_severe'] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([2, 3], [y_pos, y_pos], 'k-', linewidth=1)
                ax.plot([2, 2], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                ax.plot([3, 3], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                significance = '***' if p_values['low_affected_vs_severe'] < 0.001 else '**' if p_values['low_affected_vs_severe'] < 0.01 else '*'
                ax.text(2.5, y_pos + 0.1, significance, ha='center', va='bottom', fontweight='bold')
                max_y = y_pos + 0.4

            # Comparação normal vs low_affected (posições 1 e 2)
            if p_values['normal_vs_low_affected'] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([1, 2], [y_pos, y_pos], 'k-', linewidth=1)
                ax.plot([1, 1], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                ax.plot([2, 2], [y_pos-0.1, y_pos], 'k-', linewidth=1)
                significance = '***' if p_values['normal_vs_low_affected'] < 0.001 else '**' if p_values['normal_vs_low_affected'] < 0.01 else '*'
                ax.text(1.5, y_pos + 0.1, significance, ha='center', va='bottom', fontweight='bold')

        # Plot para modo regular
        ax1.errorbar([1,2,3], mean_fr_regular, fmt='.', yerr=sem_fr_regular, capsize=5, color='black')
        ax1.grid()
        ax1.scatter(1+0.1*np.random.normal(size=len(mn_rate_mean_mean_regular[conditions[0]])), mn_rate_mean_mean_regular[conditions[0]])
        ax1.scatter(2+0.1*np.random.normal(size=len(mn_rate_mean_mean_regular[conditions[1]])), mn_rate_mean_mean_regular[conditions[1]])
        ax1.scatter(3+0.1*np.random.normal(size=len(mn_rate_mean_mean_regular[conditions[2]])), mn_rate_mean_mean_regular[conditions[2]])
        ax1.set_xticks([1,2,3])
        ax1.set_xticklabels([conditions[0], conditions[1], conditions[2]])
        ax1.set_ylabel('MN firing rate (pps)')
        ax1.set_title('Regular Mode')
        add_significance_bars(ax1, mean_fr_regular, p_values_regular)

        # Plot para modo random
        ax2.errorbar([1,2,3], mean_fr_randomly, fmt='.', yerr=sem_fr_randomly, capsize=5, color='black')
        ax2.grid()
        ax2.scatter(1+0.1*np.random.normal(size=len(mn_rate_mean_mean_randomly[conditions[0]])), mn_rate_mean_mean_randomly[conditions[0]])
        ax2.scatter(2+0.1*np.random.normal(size=len(mn_rate_mean_mean_randomly[conditions[1]])), mn_rate_mean_mean_randomly[conditions[1]])
        ax2.scatter(3+0.1*np.random.normal(size=len(mn_rate_mean_mean_randomly[conditions[2]])), mn_rate_mean_mean_randomly[conditions[2]])
        ax2.set_xticks([1,2,3])
        ax2.set_xticklabels([conditions[0], conditions[1], conditions[2]])
        ax2.set_ylabel('MN firing rate (pps)')
        ax2.set_title('Random Mode')
        add_significance_bars(ax2, mean_fr_randomly, p_values_randomly)

        # Adicionar legenda para significância apenas se houver alguma significância
        has_significance = any([
            any(p < 0.05 for p in p_values_regular.values()),
            any(p < 0.05 for p in p_values_randomly.values())
        ])

        if has_significance:
            fig.text(0.5, 0.02, '* p < 0.05, ** p < 0.01, *** p < 0.001', ha='center', fontsize=10)
            fig.subplots_adjust(bottom=0.1)  # Deixar espaço para a legenda
        else:
            fig.tight_layout()

        fig.savefig('diabetes/figuras/mn_firing_rate_comparison_combined.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

        # Salvar dados em CSV para ambos os modos
        for mode, mn_rate_mean_mean, mn_rate_mean_CV in [('regular', mn_rate_mean_mean_regular, mn_rate_mean_CV_regular),
                                                        ('random', mn_rate_mean_mean_randomly, mn_rate_mean_CV_randomly)]:
            for cond in conditions:
                df = pd.DataFrame({
                    'firing_rate': mn_rate_mean_mean[cond].flatten(),
                    'ISI_CV': mn_rate_mean_CV[cond].flatten()
                })
                df.to_csv(f'diabetes/mn_firing_rate_{cond}_{mode}.csv', index=False)

            mean_fr = mean_fr_regular if mode == 'regular' else mean_fr_randomly
            sem_fr = sem_fr_regular if mode == 'regular' else sem_fr_randomly
            df_mean = pd.DataFrame({
                'condition': conditions,
                'mean_firing_rate': mean_fr,
                'sem_firing_rate': sem_fr
            })
            df_mean.to_csv(f'diabetes/mn_firing_rate_summary_{mode}.csv', index=False)

    def firing_rate(spiketrains, delta_t=0.00005, filtro_ordem=4, freq_corte=0.001, tempo_max=1000):
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
        idx = np.searchsorted(t, spiketrains/1000)
        idx = idx[idx<len(fr)]
        fr[idx] = 1/delta_t
        # Filtro Butterworth
        fs = 1/delta_t
        b, a = butter(filtro_ordem, freq_corte/(fs/2))

        # Aplicação do filtro
        fr = filtfilt(b, a, fr)
        fr[fr<0] = 0
        return fr, t




    return (
        compute_cv,
        compute_fr,
        firing_rate,
        select_mns_randomly,
        select_mns_regular,
    )


@app.cell
def _(
    batch_name,
    compute_cv,
    compute_fr,
    conditions,
    csd,
    detrend,
    firing_rate,
    np,
    p_cv_val,
    path,
    plot_mn_cv_single_mode,
    plt,
    posthoc_dunn,
    scipy,
    select_mns_randomly,
    select_mns_regular,
    t_end,
    t_start,
    welch,
):
    def fr_analysis_single_mode(
        trials,
        mode="regular",
        pd=None,
        batch_name="",
        save_plot=False,
        save_cv_plot=False,
        show_stats=True,
        title="",
        stats=None,
    ):
        """
        Função que computa a análise de firing rate para um modo específico.

        Args:
            trials: lista de trials para análise
            mode: 'regular' ou 'random'
            pd: pandas module
            batch_name: nome do batch
            save_plot: se True, salva gráfico de firing rate para este modo
            save_cv_plot: se True, exibe e salva gráfico de CoV dos ISI para este modo
            show_stats: se True, imprime estatísticas e p-values

        Returns:
            tuple: (mn_rate_mean_mean, mn_rate_mean_CV, force_stats)
        """
        force_level = 20

        # Inicializar dicionários para armazenar dados
        mn_rate_mean_mean = dict()
        mn_rate_mean_CV = dict()
        for condition in conditions:
            mn_rate_mean_mean[condition] = np.array([]).reshape(-1, 1)
            mn_rate_mean_CV[condition] = np.array([]).reshape(-1, 1)

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

                if condition == "severe":
                    force = force[force[:, 0] > t_start, 1]
                    force_mean = force_mean + force
                    CV_mean = CV_mean + force.std() / force.mean()
                    n = n + 1

                # Seleção de neurônios baseada no modo
                if mode == "regular":
                    selected_neurons = select_mns_regular(
                        data, t_start=t_start, t_end=t_end
                    )
                elif mode == "random":
                    selected_neurons = select_mns_randomly(
                        data, t_start=t_start, t_end=t_end, size=6
                    )
                else:
                    raise ValueError("Mode deve ser 'regular' ou 'random'")

                # Computar firing rate e CV
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)

                # Filtrar dados válidos
                valid_mask = mns_rate_mean >= 0.01
                ISI_CV = ISI_CV[valid_mask].reshape(-1, 1)
                mns_rate_mean = mns_rate_mean[valid_mask].reshape(-1, 1)

                # Armazenar dados
                mn_rate_mean_mean[condition] = np.vstack(
                    (mn_rate_mean_mean[condition], mns_rate_mean)
                )
                mn_rate_mean_CV[condition] = np.vstack(
                    (mn_rate_mean_CV[condition], ISI_CV)
                )

        # Calcular estatísticas da força
        force_stats = {
            "force_mean": force_mean / n if n > 0 else 0,
            "CV_mean": CV_mean / n if n > 0 else 0,
        }

        # Imprimir estatísticas se solicitado
        if show_stats:
            print(
                "Mean force: ",
                force_stats["force_mean"].mean()
                if hasattr(force_stats["force_mean"], "mean")
                else force_stats["force_mean"],
                "CV force:",
                force_stats["CV_mean"],
            )
            p_values_fr, p_values_cv = calculate_pvalues_and_print(
                mn_rate_mean_mean, mn_rate_mean_CV, mode, conditions, stats
            )

        # Salvar gráfico individual se solicitado
        if save_plot:
            plot_mn_fr_single_mode(
                mn_rate_mean_mean,
                mn_rate_mean_CV,
                mode,
                conditions,
                pd,
                stats,
                title=title,
            )

        # Salvar gráfico do CoV dos ISI se solicitado
        if save_cv_plot:
            plot_mn_cv_single_mode(
                mn_rate_mean_mean,
                mn_rate_mean_CV,
                mode,
                conditions,
                pd,
                stats,
                title=title,
            )

        return mn_rate_mean_mean, mn_rate_mean_CV, force_stats


    def calculate_pvalues_and_print(
        firing_rate_data, cv_data, mode_name, conditions, stats
    ):
        """
        Função auxiliar para calcular p-values e imprimir estatísticas.
        """
        p_values = {}
        print(f"=== MODO {mode_name.upper()} ===")

        # Imprimir estatísticas de Firing Rate
        print("FIRING RATE:")
        print(
            f"  Normal: {firing_rate_data['normal'].mean():.2f} ± {firing_rate_data['normal'].std():.2f} pps"
        )
        print(
            f"  Low_affected: {firing_rate_data['low_affected'].mean():.2f} ± {firing_rate_data['low_affected'].std():.2f} pps"
        )
        print(
            f"  Severe: {firing_rate_data['severe'].mean():.2f} ± {firing_rate_data['severe'].std():.2f} pps"
        )

        # Imprimir estatísticas de CoV dos ISI
        print("CoV dos ISI:")
        print(
            f"  Normal: {cv_data['normal'].mean():.3f} ± {cv_data['normal'].std():.3f}"
        )
        print(
            f"  Low_affected: {cv_data['low_affected'].mean():.3f} ± {cv_data['low_affected'].std():.3f}"
        )
        print(
            f"  Severe: {cv_data['severe'].mean():.3f} ± {cv_data['severe'].std():.3f}"
        )

        # Calcular p-values para Firing Rate
        print("P-VALUES (Firing Rate):")
        # _, p_val = stats.ttest_ind(a=firing_rate_data[conditions[0]], b=firing_rate_data[conditions[2]])
        p_val = posthoc_dunn(
            [firing_rate_data[conditions[0]], firing_rate_data[conditions[2]]]
        )
        p_values["normal_vs_severe"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )
        print(f"  Normal vs Severe: {p_values['normal_vs_severe']:.6f}")

        # _, p_val = stats.ttest_ind(a=firing_rate_data[conditions[1]], b=firing_rate_data[conditions[2]])
        p_val = posthoc_dunn(
            [firing_rate_data[conditions[1]], firing_rate_data[conditions[2]]]
        )
        p_values["low_affected_vs_severe"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )
        print(
            f"  Low_affected vs Severe: {p_values['low_affected_vs_severe']:.6f}"
        )

        # _, p_val = stats.ttest_ind(a=firing_rate_data[conditions[0]], b=firing_rate_data[conditions[1]])
        p_val = posthoc_dunn(
            [firing_rate_data[conditions[0]], firing_rate_data[conditions[1]]]
        )
        p_values["normal_vs_low_affected"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )
        print(
            f"  Normal vs Low_affected: {p_values['normal_vs_low_affected']:.6f}"
        )

        # Calcular p-values para CoV dos ISI
        print("P-VALUES (CoV dos ISI):")
        p_values_cv = {}

        # _, p_cv_val = stats.ttest_ind(a=cv_data[conditions[0]], b=cv_data[conditions[2]])
        p_val = posthoc_dunn([cv_data[conditions[0]], cv_data[conditions[2]]])
        p_values_cv["normal_vs_severe"] = (
            p_cv_val.item() if hasattr(p_cv_val, "item") else p_cv_val
        )
        print(f"  Normal vs Severe: {p_values_cv['normal_vs_severe']:.6f}")

        # _, p_cv_val = stats.ttest_ind(a=cv_data[conditions[1]], b=cv_data[conditions[2]])
        p_val = posthoc_dunn([cv_data[conditions[1]], cv_data[conditions[2]]])
        p_values_cv["low_affected_vs_severe"] = (
            p_cv_val.item() if hasattr(p_cv_val, "item") else p_cv_val
        )
        print(
            f"  Low_affected vs Severe: {p_values_cv['low_affected_vs_severe']:.6f}"
        )

        # _, p_cv_val = stats.ttest_ind(a=cv_data[conditions[0]], b=cv_data[conditions[1]])
        p_val = posthoc_dunn([cv_data[conditions[0]], cv_data[conditions[1]]])
        p_values_cv["normal_vs_low_affected"] = (
            p_cv_val.item() if hasattr(p_cv_val, "item") else p_cv_val
        )
        print(
            f"  Normal vs Low_affected: {p_values_cv['normal_vs_low_affected']:.6f}"
        )

        print("-" * 50)

        return p_values, p_values_cv


    def plot_mn_fr_single_mode(
        mn_rate_mean_mean, mn_rate_mean_CV, mode, conditions, pd, stats, title=""
    ):
        """
        Função para criar gráfico individual para um modo específico.
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Calcular estatísticas
        mean_fr = np.hstack(
            (
                np.mean(mn_rate_mean_mean[conditions[0]]),
                np.mean(mn_rate_mean_mean[conditions[1]]),
                np.mean(mn_rate_mean_mean[conditions[2]]),
            )
        )
        sem_fr = np.hstack(
            (
                mn_rate_mean_mean[conditions[0]].std()
                / np.sqrt(len(mn_rate_mean_mean[conditions[0]])),
                mn_rate_mean_mean[conditions[1]].std()
                / np.sqrt(len(mn_rate_mean_mean[conditions[1]])),
                mn_rate_mean_mean[conditions[2]].std(ddof=1)
                / np.sqrt(len(mn_rate_mean_mean[conditions[2]])),
            )
        )

        # Calcular p-values
        p_values = {}
        # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[2]])
        p_val = posthoc_dunn(
            [mn_rate_mean_mean[conditions[0]], mn_rate_mean_mean[conditions[2]]]
        )
        p_values["normal_vs_severe"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )
        # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[1]], b=mn_rate_mean_mean[conditions[2]])
        p_val = posthoc_dunn(
            [mn_rate_mean_mean[conditions[1]], mn_rate_mean_mean[conditions[2]]]
        )
        p_values["low_affected_vs_severe"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )
        # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[1]])
        p_val = posthoc_dunn(
            [mn_rate_mean_mean[conditions[0]], mn_rate_mean_mean[conditions[1]]]
        )
        p_values["normal_vs_low_affected"] = (
            p_val.item() if hasattr(p_val, "item") else p_val
        )

        # Criar figura
        fig, ax = plt.subplots(figsize=(10, 8))

        # Função para adicionar indicações de significância
        def add_significance_bars(ax, means, p_values, y_offset=0.5):
            max_y = max(means) + y_offset

            # Comparação normal vs severe (posições 1 e 3)
            if p_values["normal_vs_severe"] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([1, 3], [y_pos, y_pos], "k-", linewidth=1)
                ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                significance = (
                    "***"
                    if p_values["normal_vs_severe"] < 0.001
                    else "**"
                    if p_values["normal_vs_severe"] < 0.01
                    else "*"
                )
                ax.text(
                    2,
                    y_pos + 0.1,
                    significance,
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )
                max_y = y_pos + 0.4

            # Comparação low_affected vs severe (posições 2 e 3)
            if p_values["low_affected_vs_severe"] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([2, 3], [y_pos, y_pos], "k-", linewidth=1)
                ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                significance = (
                    "***"
                    if p_values["low_affected_vs_severe"] < 0.001
                    else "**"
                    if p_values["low_affected_vs_severe"] < 0.01
                    else "*"
                )
                ax.text(
                    2.5,
                    y_pos + 0.1,
                    significance,
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )
                max_y = y_pos + 0.4

            # Comparação normal vs low_affected (posições 1 e 2)
            if p_values["normal_vs_low_affected"] < 0.05:
                y_pos = max_y + 0.3
                ax.plot([1, 2], [y_pos, y_pos], "k-", linewidth=1)
                ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                significance = (
                    "***"
                    if p_values["normal_vs_low_affected"] < 0.001
                    else "**"
                    if p_values["normal_vs_low_affected"] < 0.01
                    else "*"
                )
                ax.text(
                    1.5,
                    y_pos + 0.1,
                    significance,
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

        # Plot principal
        ax.errorbar(
            [1, 2, 3], mean_fr, fmt=".", yerr=sem_fr, capsize=5, color="black"
        )
        ax.grid()
        ax.scatter(
            1 + 0.1 * np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])),
            mn_rate_mean_mean[conditions[0]],
        )
        ax.scatter(
            2 + 0.1 * np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])),
            mn_rate_mean_mean[conditions[1]],
        )
        ax.scatter(
            3 + 0.1 * np.random.normal(size=len(mn_rate_mean_mean[conditions[2]])),
            mn_rate_mean_mean[conditions[2]],
        )
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels([conditions[0], conditions[1], conditions[2]])
        ax.set_ylabel("MN firing rate (pps)")
        ax.set_title(title)
        add_significance_bars(ax, mean_fr, p_values)

        # Adicionar legenda para significância se houver alguma significância
        has_significance = any(p < 0.05 for p in p_values.values())
        if has_significance:
            fig.text(
                0.5,
                0.02,
                "* p < 0.05, ** p < 0.01, *** p < 0.001",
                ha="center",
                fontsize=10,
            )
            fig.subplots_adjust(bottom=0.1)
        else:
            fig.tight_layout()

        fig.savefig(
            f"diabetes/figuras/mn_firing_rate_{mode}_mode_{title}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()  # Exibir o gráfico
        plt.close(fig)

        # Salvar dados em CSV
        for cond in conditions:
            df = pd.DataFrame(
                {
                    "firing_rate": mn_rate_mean_mean[cond].flatten(),
                    "ISI_CV": mn_rate_mean_CV[cond].flatten(),
                }
            )
            df.to_csv(
                f"diabetes/mn_firing_rate_{cond}_{mode}_mode.csv", index=False
            )

        df_mean = pd.DataFrame(
            {
                "condition": conditions,
                "mean_firing_rate": mean_fr,
                "sem_firing_rate": sem_fr,
            }
        )
        df_mean.to_csv(
            f"diabetes/mn_firing_rate_summary_{mode}_mode_{title}.csv", index=False
        )


    def coherence_mu_combined(trials, pd=None):
        import os

        force_level = 20
        divisions = 40
        nperseg = int(176000 / 0.05) // divisions

        # Dados para ambos os modos
        results = {}
        for mode in ["regular", "randomly"]:
            Prate = dict()
            Pfr = dict()
            Prate_fr = dict()
            n = dict()
            for condition in conditions:
                Prate[condition] = 0
                Pfr[condition] = 0
                Prate_fr[condition] = 0
                n[condition] = 0

            for trial in trials:
                for condition in conditions:
                    data = pd.read_csv(
                        f"{path}spikedata_{condition}_{trial}_{batch_name}_long/cell_spike_ref_{force_level}.csv",
                        delimiter=",",
                    )
                    source_data = pd.read_csv(
                        f"{path}spikefeedbacksource_{condition}_{trial}_{batch_name}_long/spike_data_ref_{force_level}.csv",
                        delimiter=",",
                    )
                    data = data.values
                    source_data["spike_time"] = source_data[
                        "spike_time"
                    ].str.replace(" ms", "")
                    source_data["spike_time"] = source_data["spike_time"].astype(
                        "float"
                    )
                    source_data = source_data.values
                    steady_data = data[
                        (data[:, 1] >= t_start) & (data[:, 1] <= 180000)
                    ]
                    steady_source_data = source_data[
                        (source_data[:, 1] >= t_start)
                        & (source_data[:, 1] <= 180000)
                    ]
                    if mode == "randomly":
                        selected_neurons = select_mns_randomly(
                            data, t_start=t_start, t_end=t_end, size=10
                        )
                    if mode == "regular":
                        selected_neurons = select_mns_regular(
                            data, t_start=t_start, t_end=t_end
                        )
                    rate = 0
                    dc_neurons = np.unique(steady_source_data[:, 0])
                    np.random.shuffle(dc_neurons)
                    for dc in dc_neurons:
                        fr_source, _ = firing_rate(
                            steady_source_data[steady_source_data[:, 0] == dc, 1]
                            - t_start,
                            delta_t=0.00005,
                            filtro_ordem=4,
                            freq_corte=500,
                            tempo_max=(180000 - t_start) / 1000,
                        )
                        rate = rate + fr_source
                    rate = rate / len(dc_neurons)
                    for neuron in selected_neurons:
                        fr_new, _ = firing_rate(
                            steady_data[steady_data[:, 0] == neuron, 1] - t_start,
                            delta_t=0.00005,
                            filtro_ordem=4,
                            freq_corte=5,
                            tempo_max=(180000 - t_start) / 1000,
                        )
                        f, Sfr = welch(
                            detrend(fr_new),
                            fs=1 / 0.00005,
                            nperseg=nperseg,
                            detrend=None,
                        )
                        Pfr[condition] = Pfr[condition] + Sfr

                        f, Srate = welch(
                            detrend(rate),
                            fs=1 / 0.00005,
                            nperseg=nperseg,
                            detrend=None,
                        )
                        Prate[condition] = Prate[condition] + Srate
                        f, Sratefr = csd(
                            detrend(rate),
                            detrend(fr_new),
                            fs=1 / 0.00005,
                            nperseg=nperseg,
                            detrend=None,
                        )
                        Prate_fr[condition] = Prate_fr[condition] + Sratefr
                        n[condition] = n[condition] + 1

            Coh = dict()
            CL = dict()
            for condition in conditions:
                Pfr[condition] = Pfr[condition] / n[condition]
                Prate[condition] = Prate[condition] / n[condition]
                Prate_fr[condition] = Prate_fr[condition] / n[condition]
                Coh[condition] = np.abs(Prate_fr[condition]) ** 2 / (
                    Prate[condition] * Pfr[condition] + 1e-6
                )
                # Cálculo do nível de confiança (CL)
                k = divisions * n[condition]  # Número de segmentos
                F_critical = scipy.stats.f.ppf(0.95, 2, 2 * (k - 1))
                CL[condition] = F_critical / (k - 1 + F_critical)

            results[mode] = {"Coh": Coh, "Pfr": Pfr, "f": f, "CL": CL}

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Criar figura única com 2 linhas (regular, random) e 3 colunas (normal, low_affected, severe)
        fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True, sharey=True)
        mode_labels = ["regular", "randomly"]
        for i, mode in enumerate(mode_labels):
            for j, condition in enumerate(["normal", "low_affected", "severe"]):
                ax = axes[i, j]
                ax.plot(
                    results[mode]["f"],
                    results[mode]["Coh"][condition],
                    label=f"Coherence",
                )
                ax.axhline(
                    y=results[mode]["CL"][condition],
                    color="r",
                    linestyle="--",
                    label=f"CL",
                )
                ax.set_xlim(results[mode]["f"][0], 10)
                ax.set_xlabel("Frequency (Hz)")
                if j == 0:
                    ax.set_ylabel("Coherence")
                if i == 0:
                    ax.set_title(condition)
                if i == 1:
                    ax.set_xlabel("Frequency (Hz)")
                ax.grid(True, linestyle="--", alpha=0.7)
                if j == 2 and i == 0:
                    ax.legend()
                if j == 0:
                    ax.annotate(
                        "Regular" if i == 0 else "Random",
                        xy=(-0.25, 0.5),
                        xycoords="axes fraction",
                        rotation=90,
                        va="center",
                        ha="center",
                        fontsize=14,
                        fontweight="bold",
                    )
        # fig.suptitle('Coherence Analysis', fontsize=18, fontweight='bold')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(
            "diabetes/figuras/coherence_mu_combined.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close(fig)

        # Salvar dados em CSV para ambos os modos
        for mode in ["random", "regular"]:
            mode_key = "randomly" if mode == "random" else "regular"
            for cond in conditions:
                df = pd.DataFrame(
                    {
                        "frequency": results[mode_key]["f"],
                        "coherence": results[mode_key]["Coh"][cond],
                    }
                )
                df.to_csv(f"diabetes/coherence_mu_{cond}_{mode}.csv", index=False)


    def fr_analysis_combined_batches(trials, pd=None, stats=None):
        """
        Função que cria uma figura combinada com 3 linhas (batches) e 2 colunas (modos).
        Primeira coluna: modo regular
        Segunda coluna: modo random

        Args:
            trials: lista de trials para análise
            pd: pandas module
            stats: scipy.stats module
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Definir os batches
        batch_names = [
            "variability_no_change",
            "variability_reinnervation_no_change",
            "variability_uptake",
        ]
        batch_titles = ["No Change", "Reinnervation No Change", "Uptake"]
        modes = ["regular", "random"]

        # Criar figura com 3 linhas e 2 colunas
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))

        # Para cada batch (linha)
        for batch_idx, (batch_name, batch_title) in enumerate(
            zip(batch_names, batch_titles)
        ):
            # Para cada modo (coluna)
            for mode_idx, mode in enumerate(modes):
                ax = axes[batch_idx, mode_idx]

                # Executar análise para este batch e modo
                mn_rate_mean_mean, _, _ = fr_analysis_single_mode(
                    trials,
                    mode=mode,
                    pd=pd,
                    batch_name=batch_name,
                    save_plot=False,
                    save_cv_plot=False,
                    show_stats=False,
                    title="",
                    stats=stats,
                )

                # Calcular estatísticas para o plot
                mean_fr = np.hstack(
                    (
                        np.mean(mn_rate_mean_mean[conditions[0]]),
                        np.mean(mn_rate_mean_mean[conditions[1]]),
                        np.mean(mn_rate_mean_mean[conditions[2]]),
                    )
                )
                sem_fr = np.hstack(
                    (
                        mn_rate_mean_mean[conditions[0]].std()
                        / np.sqrt(len(mn_rate_mean_mean[conditions[0]])),
                        mn_rate_mean_mean[conditions[1]].std()
                        / np.sqrt(len(mn_rate_mean_mean[conditions[1]])),
                        mn_rate_mean_mean[conditions[2]].std(ddof=1)
                        / np.sqrt(len(mn_rate_mean_mean[conditions[2]])),
                    )
                )

                # Calcular p-values
                p_values = {}
                # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[2]])

                p_val = posthoc_dunn([mn_rate_mean_mean[conditions[0]].squeeze(), mn_rate_mean_mean[conditions[2]].squeeze()])
                p_values["normal_vs_severe"] = (
                    p_val.item() if hasattr(p_val, "item") else p_val
                )
                # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[1]], b=mn_rate_mean_mean[conditions[2]])
                p_val = posthoc_dunn([mn_rate_mean_mean[conditions[1]].squeeze(), mn_rate_mean_mean[conditions[2]].squeeze()])
                p_values["low_affected_vs_severe"] = (
                    p_val.item() if hasattr(p_val, "item") else p_val
                )
                # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[1]])
                p_val = posthoc_dunn([mn_rate_mean_mean[conditions[0]].squeeze(), mn_rate_mean_mean[conditions[1]].squeeze()])
                p_values["normal_vs_low_affected"] = (
                    p_val.item() if hasattr(p_val, "item") else p_val
                )

                # Função para adicionar indicações de significância
                def add_significance_bars(ax, means, p_values, y_offset=0.5):
                    max_y = max(means) + y_offset

                    # Comparação normal vs severe (posições 1 e 3)
                    print(p_values["normal_vs_severe"])
                    if p_values["normal_vs_severe"].values[0,1] < 0.05:
                        y_pos = max_y + 0.3
                        ax.plot([1, 3], [y_pos, y_pos], "k-", linewidth=1)
                        ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        significance = (
                            "***"
                            if p_values["normal_vs_severe"].values[0,1] < 0.001
                            else "**"
                            if p_values["normal_vs_severe"].values[0,1] < 0.01
                            else "*"
                        )
                        ax.text(
                            2,
                            y_pos + 0.1,
                            significance,
                            ha="center",
                            va="bottom",
                            fontweight="bold",
                        )
                        max_y = y_pos + 0.4

                    # Comparação low_affected vs severe (posições 2 e 3)
                    if p_values["low_affected_vs_severe"].values[0,1] < 0.05:
                        y_pos = max_y + 0.3
                        ax.plot([2, 3], [y_pos, y_pos], "k-", linewidth=1)
                        ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        significance = (
                            "***"
                            if p_values["low_affected_vs_severe"].values[0,1] < 0.001
                            else "**"
                            if p_values["low_affected_vs_severe"].values[0,1] < 0.01
                            else "*"
                        )
                        ax.text(
                            2.5,
                            y_pos + 0.1,
                            significance,
                            ha="center",
                            va="bottom",
                            fontweight="bold",
                        )
                        max_y = y_pos + 0.4

                    # Comparação normal vs low_affected (posições 1 e 2)
                    if p_values["normal_vs_low_affected"].values[0,1] < 0.05:
                        y_pos = max_y + 0.3
                        ax.plot([1, 2], [y_pos, y_pos], "k-", linewidth=1)
                        ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                        significance = (
                            "***"
                            if p_values["normal_vs_low_affected"].values[0,1] < 0.001
                            else "**"
                            if p_values["normal_vs_low_affected"].values[0,1] < 0.01
                            else "*"
                        )
                        ax.text(
                            1.5,
                            y_pos + 0.1,
                            significance,
                            ha="center",
                            va="bottom",
                            fontweight="bold",
                        )

                # Plot principal
                ax.errorbar(
                    [1, 2, 3],
                    mean_fr,
                    fmt=".",
                    yerr=sem_fr,
                    capsize=10,
                    color="black",
                    elinewidth=5,
                )
                ax.grid()
                ax.scatter(
                    1
                    + 0.1
                    * np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])),
                    mn_rate_mean_mean[conditions[0]],
                    color=(0.0039, 0.451, 0.698),
                )
                ax.scatter(
                    2
                    + 0.1
                    * np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])),
                    mn_rate_mean_mean[conditions[1]],
                    color=(0.8709, 0.5608, 0.0196),
                )
                ax.scatter(
                    3
                    + 0.1
                    * np.random.normal(size=len(mn_rate_mean_mean[conditions[2]])),
                    mn_rate_mean_mean[conditions[2]],
                    color=(0.0078, 0.6196, 0.451),
                )
                ax.set_xticks([1, 2, 3])
                ax.set_xticklabels(
                    [conditions[0], conditions[1], conditions[2]], fontsize=13
                )

                # Labels e títulos
                if batch_idx == 2:  # Última linha
                    ax.set_xlabel("Condition", fontsize=15)
                if mode_idx == 0:  # Primeira coluna
                    ax.set_ylabel("MN firing rate (pps)", fontsize=15)

                # Título das colunas (apenas na primeira linha)
                if batch_idx == 0:
                    mode_title = (
                        "Regular Mode" if mode == "regular" else "Random Mode"
                    )
                    ax.set_title(mode_title)

                # Label das linhas (apenas na primeira coluna)
                if mode_idx == 0:
                    ax.text(
                        -0.15,
                        0.5,
                        batch_title,
                        transform=ax.transAxes,
                        rotation=90,
                        va="center",
                        ha="center",
                        fontweight="bold",
                        fontsize=15,
                    )

                add_significance_bars(ax, mean_fr, p_values)

        # Adicionar legenda para significância
        fig.text(
            0.5,
            0.02,
            "* p < 0.05, ** p < 0.01, *** p < 0.001",
            ha="center",
            fontsize=12,
        )

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.08, left=0.1)

        # Salvar figura
        fig.savefig(
            "diabetes/figuras/mn_firing_rate_combined_batches.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close(fig)

        print(
            "Figura combinada salva como: diabetes/figuras/mn_firing_rate_combined_batches.png"
        )


    def fr_analysis_batch_variability(trials, pd=None, stats=None):
        """
        Função que cria uma figura com batch variability comparando modo regular e random.
        Usa apenas dados com final 'variability' - uma linha com 2 colunas (regular vs random).

        Args:
            trials: lista de trials para análise
            pd: pandas module
            stats: scipy.stats module
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Usar apenas batch 'variability' (sem sufixos específicos)
        batch_name = batch_name
        modes = ["regular", "random"]

        # Criar figura com 1 linha e 2 colunas
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        # Para cada modo (coluna)
        for mode_idx, mode in enumerate(modes):
            ax = axes[mode_idx]

            # Executar análise para este modo usando batch 'variability'
            mn_rate_mean_mean, _, _ = fr_analysis_single_mode(
                trials,
                mode=mode,
                pd=pd,
                batch_name=batch_name,
                save_plot=False,
                save_cv_plot=False,
                show_stats=False,
                title="",
                stats=stats,
            )

            # Calcular estatísticas para o plot
            mean_fr = np.hstack(
                (
                    np.mean(mn_rate_mean_mean[conditions[0]]),
                    np.mean(mn_rate_mean_mean[conditions[1]]),
                    np.mean(mn_rate_mean_mean[conditions[2]]),
                )
            )
            sem_fr = np.hstack(
                (
                    mn_rate_mean_mean[conditions[0]].std()
                    / np.sqrt(len(mn_rate_mean_mean[conditions[0]])),
                    mn_rate_mean_mean[conditions[1]].std()
                    / np.sqrt(len(mn_rate_mean_mean[conditions[1]])),
                    mn_rate_mean_mean[conditions[2]].std(ddof=1)
                    / np.sqrt(len(mn_rate_mean_mean[conditions[2]])),
                )
            )

            # Calcular p-values
            p_values = {}
            # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[2]])

            p_val = posthoc_dunn([mn_rate_mean_mean[conditions[0]].squeeze(), mn_rate_mean_mean[conditions[2]].squeeze()])
            p_values["normal_vs_severe"] = (
                p_val.item() if hasattr(p_val, "item") else p_val
            )
            # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[1]], b=mn_rate_mean_mean[conditions[2]])
            p_val = posthoc_dunn([mn_rate_mean_mean[conditions[1]].squeeze(), mn_rate_mean_mean[conditions[2]].squeeze()])
            p_values["low_affected_vs_severe"] = (p_val.item() if hasattr(p_val, "item") else p_val)
            # _, p_val = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[1]])
            p_val = posthoc_dunn([mn_rate_mean_mean[conditions[0]].squeeze(), mn_rate_mean_mean[conditions[1]].squeeze()])
            p_values["normal_vs_low_affected"] = (p_val.item() if hasattr(p_val, "item") else p_val)

            # Função para adicionar indicações de significância
            def add_significance_bars(ax, means, p_values, y_offset=0.5):
                max_y = max(means) + y_offset

                # Comparação normal vs severe (posições 1 e 3)
                if p_values["normal_vs_severe"].values[0,1] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([1, 3], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***"
                        if p_values["normal_vs_severe"].values[0,1] < 0.001
                        else "**"
                        if p_values["normal_vs_severe"].values[0,1] < 0.01
                        else "*"
                    )
                    ax.text(
                        2,
                        y_pos + 0.1,
                        significance,
                        ha="center",
                        va="bottom",
                        fontweight="bold",
                    )
                    max_y = y_pos + 0.4

                # Comparação low_affected vs severe (posições 2 e 3)
                if p_values["low_affected_vs_severe"].values[0,1] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([2, 3], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***"
                        if p_values["low_affected_vs_severe"].values[0,1] < 0.001
                        else "**"
                        if p_values["low_affected_vs_severe"].values[0,1] < 0.01
                        else "*"
                    )
                    ax.text(
                        2.5,
                        y_pos + 0.1,
                        significance,
                        ha="center",
                        va="bottom",
                        fontweight="bold",
                    )
                    max_y = y_pos + 0.4

                # Comparação normal vs low_affected (posições 1 e 2)
                if p_values["normal_vs_low_affected"].values[0,1] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([1, 2], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***"
                        if p_values["normal_vs_low_affected"].values[0,1] < 0.001
                        else "**"
                        if p_values["normal_vs_low_affected"].values[0,1] < 0.01
                        else "*"
                    )
                    ax.text(
                        1.5,
                        y_pos + 0.1,
                        significance,
                        ha="center",
                        va="bottom",
                        fontweight="bold",
                    )

            # Plot principal
            ax.errorbar(
                [1, 2, 3],
                mean_fr,
                fmt=".",
                yerr=sem_fr,
                capsize=10,
                color="black",
                elinewidth=5,
            )
            ax.grid()
            ax.scatter(
                1
                + 0.1
                * np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])),
                mn_rate_mean_mean[conditions[0]],
                color=(0.0039, 0.451, 0.698),
            )
            ax.scatter(
                2
                + 0.1
                * np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])),
                mn_rate_mean_mean[conditions[1]],
                color=(0.8709, 0.5608, 0.0196),
            )
            ax.scatter(
                3
                + 0.1
                * np.random.normal(size=len(mn_rate_mean_mean[conditions[2]])),
                mn_rate_mean_mean[conditions[2]],
                color=(0.0078, 0.6196, 0.451),
            )
            ax.set_xticks([1, 2, 3])
            ax.set_xticklabels(
                [conditions[0], conditions[1], conditions[2]], fontsize=13
            )

            # Labels e títulos
            ax.set_xlabel("Condition", fontsize=15)
            ax.set_ylabel("MN firing rate (pps)", fontsize=15)

            # Título de cada coluna
            mode_title = "Regular Mode" if mode == "regular" else "Random Mode"
            ax.set_title(mode_title)

            add_significance_bars(ax, mean_fr, p_values)

        # Adicionar legenda para significância
        fig.text(
            0.5,
            0.02,
            "* p < 0.05, ** p < 0.01, *** p < 0.001",
            ha="center",
            fontsize=12,
        )

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)

        # Salvar figura
        fig.savefig(
            "diabetes/figuras/mn_firing_rate_batch_variability.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close(fig)

        print(
            "Figura de batch variability salva como: diabetes/figuras/mn_firing_rate_batch_variability.png"
        )


    def isi_cov_histograms(
        trials, mode="regular", pd=None, batch_name=batch_name, stats=None
    ):
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
            conditions[1]: (0.8709, 0.5608, 0.0196),  # low_affected - laranja
            conditions[2]: (0.0078, 0.6196, 0.451),  # severe - verde
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
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Para cada condição
        for i, condition in enumerate(conditions):
            ax = axes[i]

            # Dados de CoV para esta condição
            cov_data = np.array(all_cov_data[condition])

            # Criar histograma
            n_bins = [
                0,
                0.05,
                0.1,
                0.15,
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.75,
                0.8,
                0.85,
                0.9,
                0.95,
            ]
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
                0.65,
                0.9,
                f"CoV < 0.3: {count_low_cov}/{total_neurons}",
                transform=ax.transAxes,
                fontsize=12,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )

            # Labels e formatação
            ax.set_xlabel("Coefficient of Variation (CoV) of ISI", fontsize=12)
            ax.set_ylabel("Number of occurences", fontsize=14)
            ax.set_title(
                f"{condition.replace('_', ' ').title()}",
                fontsize=14,
                fontweight="bold",
            )
            ax.grid(True, alpha=0.3)

            # Adicionar linha vertical em CoV = 0.3 para referência
            ax.axvline(x=0.3, color="red", linestyle="--", alpha=0.8, linewidth=2)

        # Título geral
        mode_title = "Regular Mode" if mode == "regular" else "Random Mode"

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)

        # Salvar figura
        filename = f"diabetes/figuras/isi_cov_histograms_all_units_{mode}_{batch_name}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        print(
            f"Histogramas de CoV dos ISI (todos os motor units) salvos como: {filename}"
        )



    def fr_analysis_combined_modes(trials, pd=None, stats=None, title=""):
        """
        Função que cria uma figura combinada com 2 colunas (regular e random).
        Mostra os plots de firing rate lado a lado para comparação direta.

        Args:
            trials: lista de trials para análise
            pd: pandas module
            stats: scipy.stats module
            title: título adicional para os gráficos
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        # Obter dados para ambos os modos
        data_regular = fr_analysis_single_mode(
            trials, mode="regular", pd=pd, batch_name=batch_name,
            save_plot=False, show_stats=False, stats=stats
        )
        data_random = fr_analysis_single_mode(
            trials, mode="random", pd=pd, batch_name=batch_name,
            save_plot=False, show_stats=False, stats=stats
        )

        mn_rate_regular, mn_cv_regular, force_stats_regular = data_regular
        mn_rate_random, mn_cv_random, force_stats_random = data_random

        # Criar figura com 1 linha e 2 colunas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Cores das condições
        colors = {
            conditions[0]: (0.0039, 0.451, 0.698),  # normal - azul
            conditions[1]: (0.8709, 0.5608, 0.0196),  # low_affected - laranja
            conditions[2]: (0.0078, 0.6196, 0.451),  # severe - verde
        }

        # Função para plotar dados em um subplot
        def plot_firing_rate_data(ax, mn_rate_data, mn_cv_data, mode_name, force_stats):
            # Calcular médias e SEM
            mean_fr = []
            sem_fr = []
            for condition in conditions:
                data = mn_rate_data[condition].flatten()
                mean_fr.append(np.mean(data))
                sem_fr.append(scipy.stats.sem(data))

            # Calcular p-values
            p_values_fr, p_values_cv = calculate_pvalues_and_print(
                mn_rate_data, mn_cv_data, mode_name, conditions, stats
            )

            # Função para adicionar indicações de significância
            def add_significance_bars(ax, means, p_values, y_offset=0.5):
                max_y = max(means) + y_offset

                # Comparação normal vs severe (posições 1 e 3)
                if p_values["normal_vs_severe"] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([1, 3], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***" if p_values["normal_vs_severe"] < 0.001
                        else "**" if p_values["normal_vs_severe"] < 0.01
                        else "*"
                    )
                    ax.text(2, y_pos + 0.1, significance, ha="center", va="bottom", fontweight="bold")
                    max_y = y_pos + 0.4

                # Comparação low_affected vs severe (posições 2 e 3)
                if p_values["low_affected_vs_severe"] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([2, 3], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([3, 3], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***" if p_values["low_affected_vs_severe"] < 0.001
                        else "**" if p_values["low_affected_vs_severe"] < 0.01
                        else "*"
                    )
                    ax.text(2.5, y_pos + 0.1, significance, ha="center", va="bottom", fontweight="bold")
                    max_y = y_pos + 0.4

                # Comparação normal vs low_affected (posições 1 e 2)
                if p_values["normal_vs_low_affected"] < 0.05:
                    y_pos = max_y + 0.3
                    ax.plot([1, 2], [y_pos, y_pos], "k-", linewidth=1)
                    ax.plot([1, 1], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    ax.plot([2, 2], [y_pos - 0.1, y_pos], "k-", linewidth=1)
                    significance = (
                        "***" if p_values["normal_vs_low_affected"] < 0.001
                        else "**" if p_values["normal_vs_low_affected"] < 0.01
                        else "*"
                    )
                    ax.text(1.5, y_pos + 0.1, significance, ha="center", va="bottom", fontweight="bold")

            # Plot principal
            ax.errorbar([1, 2, 3], mean_fr, fmt=".", yerr=sem_fr, capsize=5, color="black")
            ax.grid()

            # Scatter plots para cada condição
            for i, condition in enumerate(conditions):
                ax.scatter(
                    (i+1) + 0.1 * np.random.normal(size=len(mn_rate_data[condition])),
                    mn_rate_data[condition].flatten(),
                    color=colors[condition],
                    alpha=0.6
                )

            ax.set_xticks([1, 2, 3])
            ax.set_xticklabels([cond.replace('_', ' ').title() for cond in conditions])
            ax.set_ylabel("MN firing rate (pps)")
            ax.set_title(f"{mode_name.title()} Mode {title}")
            add_significance_bars(ax, mean_fr, p_values_fr)

            return p_values_fr

        # Plotar dados para modo regular (coluna esquerda)
        p_values_regular = plot_firing_rate_data(ax1, mn_rate_regular, mn_cv_regular, "regular", force_stats_regular)

        # Plotar dados para modo random (coluna direita)
        p_values_random = plot_firing_rate_data(ax2, mn_rate_random, mn_cv_random, "random", force_stats_random)

        # Adicionar legenda para significância se houver alguma significância
        has_significance = (any(p < 0.05 for p in p_values_regular.values()) or
                           any(p < 0.05 for p in p_values_random.values()))
        if has_significance:
            fig.text(0.5, 0.02, "* p < 0.05, ** p < 0.01, *** p < 0.001",
                    ha="center", fontsize=10)
            fig.subplots_adjust(bottom=0.1)
        else:
            fig.tight_layout()

        # Salvar figura
        filename = f"diabetes/figuras/mn_firing_rate_combined_modes_{title}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close(fig)

        print(f"Figura combinada (regular vs random) salva como: {filename}")

        # Salvar dados em CSV para ambos os modos
        for mode, (mn_rate_data, mn_cv_data) in [("regular", (mn_rate_regular, mn_cv_regular)),
                                                  ("random", (mn_rate_random, mn_cv_random))]:
            for cond in conditions:
                df = pd.DataFrame({
                    "firing_rate": mn_rate_data[cond].flatten(),
                    "ISI_CV": mn_cv_data[cond].flatten(),
                })
                df.to_csv(f"diabetes/mn_firing_rate_{cond}_{mode}_mode_combined.csv", index=False)

    return (
        coherence_mu_combined,
        fr_analysis_batch_variability,
        fr_analysis_combined_batches,
        fr_analysis_combined_modes,
        isi_cov_histograms,
    )


@app.cell
def _(batch_name, conditions, np, path, plt, welch):
    def plot_force_and_spectrum(trials_long, pd=None):
        """
        Função que cria um plot com 3 linhas e 2 colunas.
        Coluna esquerda: primeiros 10 segundos da força
        Coluna direita: espectro da força usando método de Welch

        Args:
            trials_long: lista de trials longos para análise
            pd: pandas module
        """
        import os

        os.makedirs("diabetes/figuras", exist_ok=True)

        force_level = 20

        # Criar figura com 3 linhas e 2 colunas
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        # Para cada condição (linha)
        for i, condition in enumerate(conditions):
            # Coletar dados de força dos 5 trials longos
            force_mean = 0
            CV = 0
            for trial in trials_long:

                # Carregar dados de força
                force_file = f"{path}force_{condition}_{trial}_{batch_name}/force_ref{force_level}.csv"

                force = pd.read_csv(force_file, delimiter=",").values[:,1]
                CV =CV + force[int(4000/0.05):].std()/force[int(4000/0.05):].mean()
                force_mean = force_mean +force

            CV = CV/50
            print(f'CV {condition}:{CV}')
            force_mean = force_mean/5       

            # Coluna esquerda: sinal de força dos primeiros 10 segundos
            ax_left = axes[i, 0]
            time_vector = np.linspace(0, 10000, len(force_mean))  # 10 segundos
            ax_left.plot(time_vector, force, linewidth=1.5)
            ax_left.set_xlim(0,10000)
            ax_left.set_ylabel("Force (N)", fontsize=12)
            ax_left.set_title(
                f"{condition.replace('_', ' ').title()}",
                fontsize=14,
                fontweight="bold",
            )
            ax_left.grid(True, alpha=0.3)

            if i == 2:  # Última linha
                ax_left.set_xlabel("Time (ms)", fontsize=12)

            # Coluna direita: espectro da força usando método de Welch
            ax_right = axes[i, 1]

            # Assumindo frequência de amostragem baseada no comprimento dos dados
            # Tipicamente 2000 Hz para dados de força (ajustar conforme necessário)
            fs = 1/0.00005  # Hz (comprimento dos dados / 10 segundos)

            # Calcular espectro usando método de Welch
            frequencies, power_spectrum = welch(force_mean[int(4000/0.05):], fs=fs, nperseg=200000)


            ax_right.plot(frequencies, power_spectrum, linewidth=1.5)
            ax_right.set_ylabel("Power Spectral Density", fontsize=12)
            ax_right.set_xlim(
                0, min(50, frequencies[-1])
            )  # Limitar a 50 Hz ou máximo disponível
            ax_right.grid(True, alpha=0.3)

            if i == 2:  # Última linha
                ax_right.set_xlabel("Frequency (Hz)", fontsize=12)

        # Títulos das colunas
        axes[0, 0].set_title(
            "Force Signal (First 10s)", fontsize=16, fontweight="bold", pad=20
        )
        axes[0, 1].set_title(
            "Force Spectrum (Welch Method)", fontsize=16, fontweight="bold", pad=20
        )

        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(top=0.93)

        # Salvar figura
        fig.savefig(
            "diabetes/figuras/force_and_spectrum_analysis.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
        plt.close(fig)

        print(
            "Figura de força e espectro salva como: diabetes/figuras/force_and_spectrum_analysis.png"
        )


    return (plot_force_and_spectrum,)


@app.cell
def _(np, pd, plot_force_and_spectrum):
    plot_force_and_spectrum(np.arange(50), pd=pd)
    return


@app.cell
def _(
    batch_name,
    compute_cv,
    compute_fr,
    conditions,
    np,
    path,
    plt,
    select_mns_randomly,
    t_end,
    t_start,
):
    def fr_cv(trials, pd=None):
        force_level = 20

        mn_rate_mean_mean = dict()
        mn_rate_mean_mean[conditions[0]] = np.array([]).reshape(-1,1)
        mn_rate_mean_mean[conditions[1]] = np.array([]).reshape(-1,1)
        mn_rate_mean_mean[conditions[2]] = np.array([]).reshape(-1,1)

        mn_rate_mean_CV = dict()
        mn_rate_mean_CV[conditions[0]] = np.array([]).reshape(-1,1)
        mn_rate_mean_CV[conditions[1]] = np.array([]).reshape(-1,1)
        mn_rate_mean_CV[conditions[2]] = np.array([]).reshape(-1,1)

        color = dict()
        color[conditions[0]] = 'Blues'
        color[conditions[1]] = 'Oranges'
        color[conditions[2]] = 'Greens'

        neurons_index = dict()
        neurons_index[conditions[0]] = np.array([]).reshape(-1,1)
        neurons_index[conditions[1]] = np.array([]).reshape(-1,1)
        neurons_index[conditions[2]] = np.array([]).reshape(-1,1)




        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(f'{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv', delimiter=',')

                data = data.values

                selected_neurons = select_mns_randomly(data, t_start=t_start, t_end=t_end, size=100)
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)
                ISI_CV = ISI_CV[mns_rate_mean>=0.01].reshape(-1,1)
                selected_neurons = selected_neurons[mns_rate_mean>=0.01].reshape(-1,1)

                # print(ISI_CV)

                mns_rate_mean = mns_rate_mean[mns_rate_mean>=0.01].reshape(-1,1) 
                mn_rate_mean_mean[condition] = np.vstack((mn_rate_mean_mean[condition], mns_rate_mean))
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))
                neurons_index[condition] = np.vstack((neurons_index[condition], selected_neurons.reshape(-1,1)))

        neurons_index[conditions[0]][neurons_index[conditions[0]]> 120] = 250
        neurons_index[conditions[1]][neurons_index[conditions[1]]> 120] = 250
        neurons_index[conditions[2]][neurons_index[conditions[2]]> 120] = 250

        neurons_index[conditions[0]][(neurons_index[conditions[0]]<= 120) & (neurons_index[conditions[0]]> 60)] = 100
        neurons_index[conditions[1]][(neurons_index[conditions[1]]<= 120) & (neurons_index[conditions[1]]> 60)] = 100
        neurons_index[conditions[2]][(neurons_index[conditions[2]]<= 120) & (neurons_index[conditions[2]]> 60)] = 100        

        neurons_index[conditions[0]][(neurons_index[conditions[0]]< 60)] = 10
        neurons_index[conditions[1]][(neurons_index[conditions[1]]< 60)] = 10
        neurons_index[conditions[2]][(neurons_index[conditions[2]]< 60)] = 10        

        expdata = pd.read_csv('results/ISI_statistics.csv')
        data_muscle = expdata.query('Muscle == "FDI"')

        import matplotlib.patches as mpatches
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
        fig, ax = plt.subplots(figsize=(8,6))
        # Plot principal
        s0 = ax.scatter(mn_rate_mean_CV[conditions[0]], mn_rate_mean_mean[conditions[0]], c=neurons_index[conditions[0]], cmap=color[conditions[0]], vmin=1, vmax=250)
        s1 = ax.scatter(mn_rate_mean_CV[conditions[1]], mn_rate_mean_mean[conditions[1]], c=neurons_index[conditions[1]], cmap=color[conditions[1]], vmin=1, vmax=250)
        s2 = ax.scatter(mn_rate_mean_CV[conditions[2]], mn_rate_mean_mean[conditions[2]], c=neurons_index[conditions[2]], cmap=color[conditions[2]], vmin=1, vmax=250)
        # ax.scatter(data_muscle['ISI CV'], 1/data_muscle['ISI mean'], color='m')
        ax.set_xlabel('CV')
        ax.set_ylabel('Firing rate mean (pps)')
        ax.grid(True, linestyle='--', alpha=0.7)
        # Legenda com cores fixas (sem patches)
        legend_labels = [conditions[0], conditions[1], conditions[2]]
        legend_colors = ['blue', 'orange', 'green']
        legend_handles = []
        for legend_color, label in zip(legend_colors, legend_labels):
            legend_handles.append(ax.scatter([], [], color=legend_color, label=label))
        ax.legend(handles=legend_handles, loc='upper left')
        # Inset 1 (zoom1) - subir
        axins1 = fig.add_axes([0.5, 0.72, 0.35, 0.25])  # [left, bottom, width, height] (subiu de 0.6 para 0.72)
        axins1.scatter(mn_rate_mean_CV[conditions[0]], mn_rate_mean_mean[conditions[0]], c=neurons_index[conditions[0]], cmap=color[conditions[0]], vmin=1, vmax=250)
        axins1.scatter(mn_rate_mean_CV[conditions[1]], mn_rate_mean_mean[conditions[1]], c=neurons_index[conditions[1]], cmap=color[conditions[1]], vmin=1, vmax=250)
        axins1.scatter(mn_rate_mean_CV[conditions[2]], mn_rate_mean_mean[conditions[2]], c=neurons_index[conditions[2]], cmap=color[conditions[2]], vmin=1, vmax=250)
        axins1.set_xlim(0, 0.3)
        axins1.set_ylim(5, 15)
        axins1.set_xlabel('CV', fontsize=8)
        axins1.set_ylabel('FR', fontsize=8)
        axins1.tick_params(axis='both', which='major', labelsize=8)
        axins1.grid(True, linestyle='--', alpha=0.7)
        # Inset 2 (zoom2)
        axins2 = fig.add_axes([0.5, 0.32, 0.35, 0.25])
        axins2.scatter(mn_rate_mean_CV[conditions[0]], mn_rate_mean_mean[conditions[0]], c=neurons_index[conditions[0]], cmap=color[conditions[0]], vmin=1, vmax=250)
        axins2.scatter(mn_rate_mean_CV[conditions[1]], mn_rate_mean_mean[conditions[1]], c=neurons_index[conditions[1]], cmap=color[conditions[1]], vmin=1, vmax=250)
        axins2.scatter(mn_rate_mean_CV[conditions[2]], mn_rate_mean_mean[conditions[2]], c=neurons_index[conditions[2]], cmap=color[conditions[2]], vmin=1, vmax=250)
        axins2.set_xlim(0, 0.2)
        axins2.set_ylim(15, 25)
        axins2.set_xlabel('CV', fontsize=8)
        axins2.set_ylabel('FR', fontsize=8)
        axins2.tick_params(axis='both', which='major', labelsize=8)
        axins2.grid(True, linestyle='--', alpha=0.7)
        fig.savefig('diabetes/fr_cv_scatter_full.png', bbox_inches='tight')
        plt.close(fig)
        # Salvar dados em CSV
        import os
        os.makedirs('diabetes', exist_ok=True)
        for cond in conditions:
            df = pd.DataFrame({
                'firing_rate': mn_rate_mean_mean[cond].flatten(),
                'ISI_CV': mn_rate_mean_CV[cond].flatten(),
                'neuron_index': neurons_index[cond].flatten()
            })
            df.to_csv(f'diabetes/fr_cv_{cond}.csv', index=False)
    return (fr_cv,)


@app.cell
def _(fr_analysis_combined_batches, np, pd, stats):
    # Criar figura combinada com 3 linhas (batches) e 2 colunas (regular/random)
    fr_analysis_combined_batches(np.arange(10), pd=pd, stats=stats)
    return


@app.cell
def _(fr_analysis_batch_variability, np, pd, stats):
    # Criar figura focada apenas nos batches de variabilidade
    fr_analysis_batch_variability(np.arange(50), pd=pd, stats=stats)
    return


@app.cell
def _(fr_analysis_combined_modes, np, pd, stats):
    # Criar figura combinada com regular e random lado a lado
    fr_analysis_combined_modes(np.arange(50), pd=pd, stats=stats, title="variability")
    return


@app.cell
def _(coherence_mu_combined, pd, trials_long):
    coherence_mu_combined(trials=trials_long, pd=pd)
    return


@app.cell
def _(isi_cov_histograms, np, pd, stats):
    # Criar histogramas de CoV dos ISI para modo regular
    isi_cov_histograms(np.arange(10), mode='regular', pd=pd, stats=stats)
    return


@app.cell
def _(isi_cov_histograms, np, pd, stats):
    # Criar histogramas de CoV dos ISI para modo random
    isi_cov_histograms(np.arange(50), mode='random', pd=pd, stats=stats)
    return


@app.cell
def _(fr_cv, np, pd):
    fr_cv(np.arange(50), pd=pd)
    return


@app.cell
def fr_spectra_combined(
    batch_name,
    conditions,
    detrend,
    firing_rate,
    path,
    plt,
    select_mns_randomly,
    select_mns_regular,
    welch,
):
    def fr_spectra_combined(trials, pd=None):
        import os
        force_level = 20
        t_start = 4000
        t_end = 10000
        nperseg = 176000

        # Dados para ambos os modos
        results = {}
        for mode in ['randomly', 'regular']:
            fr_low = dict()
            fr_medium = dict()
            fr_high = dict()
            n_low = dict()
            n_medium = dict()
            n_high = dict()
            Pfr_low = dict()
            Pfr_medium = dict()
            Pfr_high = dict()

            for condition in conditions:
                fr_low[condition] = 0
                fr_medium[condition] = 0
                fr_high[condition] = 0
                n_low[condition] = 0
                n_medium[condition] = 0
                n_high[condition] = 0

            for trial in trials:
                for condition in conditions:
                    data = pd.read_csv(f'{path}spikedata_{condition}_{trial}_{batch_name}_long/cell_spike_ref_{force_level}.csv', delimiter=',')
                    data = data.values
                    steady_data = data[(data[:, 1] >= t_start) & (data[:, 1] <= t_end)]
                    if mode == 'randomly': selected_neurons = select_mns_randomly(data, t_start=t_start, t_end=t_end, size=100)
                    if mode == 'regular': selected_neurons = select_mns_regular(data, t_start=t_start, t_end=t_end)
                    for neuron in selected_neurons:
                        fr_new, _ = firing_rate(steady_data[steady_data[:,0]==neuron,1]-t_start, delta_t=0.00005, filtro_ordem=4, freq_corte=100, tempo_max=(t_end-t_start)/1000)
                        if fr_new.mean() > 0.1:
                            if neuron <= 85:
                                fr_low[condition] = fr_low[condition] + fr_new
                                n_low[condition] = n_low[condition] + 1
                            elif neuron <= 110:
                                fr_medium[condition] = fr_medium[condition] + fr_new
                                n_medium[condition] = n_medium[condition] + 1
                            else:
                                fr_high[condition] = fr_high[condition] + fr_new
                                n_high[condition] = n_high[condition] + 1

            for condition in conditions:
                fr_low[condition] = fr_low[condition]/n_low[condition]
                fr_medium[condition] = fr_medium[condition]/n_medium[condition]
                fr_high[condition] = fr_high[condition]/n_high[condition]
                f, Pfr_low[condition] = welch(detrend(fr_low[condition]), fs=1/0.00005, nperseg=nperseg, nfft = nperseg, detrend=False)
                f, Pfr_high[condition] = welch(detrend(fr_high[condition]), fs=1/0.00005, nperseg=nperseg, nfft = nperseg, detrend=False)

            results[mode] = {
                'fr_low': fr_low, 'fr_medium': fr_medium, 'fr_high': fr_high,
                'Pfr_low': Pfr_low, 'Pfr_high': Pfr_high,
                'f': f
            }

        os.makedirs('diabetes/figuras', exist_ok=True)
        # Para cada tipo (low, high), criar figura com dois subplots lado a lado (um para cada modo)
        tipos = [('low', 'Pfr_low', 'fr_low'), ('high', 'Pfr_high', 'fr_high')]
        for tipo, pfr_key, fr_key in tipos:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))

            # Espectro de firing rate - modo random
            for condition in conditions:
                ax1.plot(results['randomly']['f'], results['randomly'][pfr_key][condition], label=condition)
            ax1.set_title(f'FR Spectrum - {tipo} (Random)')
            ax1.set_xlim(results['randomly']['f'][0], 100)
            ax1.legend()
            ax1.set_xlabel('Frequency (Hz)')
            ax1.set_ylabel('Power')
            ax1.grid(True, linestyle='--', alpha=0.7)

            # Espectro de firing rate - modo regular
            for condition in conditions:
                ax2.plot(results['regular']['f'], results['regular'][pfr_key][condition], label=condition)
            ax2.set_title(f'FR Spectrum - {tipo} (Regular)')
            ax2.set_xlim(results['regular']['f'][0], 100)
            ax2.legend()
            ax2.set_xlabel('Frequency (Hz)')
            ax2.set_ylabel('Power')
            ax2.grid(True, linestyle='--', alpha=0.7)

            # Sinal de firing rate no tempo - modo random
            for condition in conditions:
                ax3.plot(results['randomly'][fr_key][condition], label=condition)
            ax3.set_title(f'FR (mean) - {tipo} (Random)')
            ax3.set_xlabel('Sample')
            ax3.set_ylabel('FR (a.u.)')
            ax3.legend()
            ax3.grid(True, linestyle='--', alpha=0.7)

            # Sinal de firing rate no tempo - modo regular
            for condition in conditions:
                ax4.plot(results['regular'][fr_key][condition], label=condition)
            ax4.set_title(f'FR (mean) - {tipo} (Regular)')
            ax4.set_xlabel('Sample')
            ax4.set_ylabel('FR (a.u.)')
            ax4.legend()
            ax4.grid(True, linestyle='--', alpha=0.7)

            fig.tight_layout()
            fig.savefig(f'diabetes/figuras/fr_spectra_{tipo}_combined.png', dpi=300, bbox_inches='tight')
            plt.close(fig)

        # Salvar dados em CSV para ambos os modos
        for mode in ['random', 'regular']:
            mode_key = 'randomly' if mode == 'random' else 'regular'
            for cond in conditions:
                df = pd.DataFrame({
                    'firing_rate': results[mode_key]['fr_low'][cond],
                    'ISI_CV': results[mode_key]['Pfr_low'][cond],
                })
                df.to_csv(f'diabetes/fr_spectra_{cond}_{mode}.csv', index=False)
    return (fr_spectra_combined,)


@app.cell
def _(fr_spectra_combined, pd, trials_long):
    fr_spectra_combined(trials=trials_long, pd=pd)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
