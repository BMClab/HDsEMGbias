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
    from scipy import stats
    import sympy as sym
    from scikit_posthocs import posthoc_dunn

    path = 'diabetes/results/'
    batch_name = 'variability'
    trials = np.arange(50)

    conditions = ['normal', 'low_affected', 'severe']

    t_start = 4000
    t_end = 10000
    return (
        batch_name,
        butter,
        conditions,
        filtfilt,
        np,
        path,
        pd,
        plt,
        posthoc_dunn,
        stats,
        t_end,
        t_start,
        trials,
    )


@app.cell
def _(butter, filtfilt, np, plt, stats):
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


    def plot_mn_fr(mn_rate_mean_mean, mn_rate_mean_CV, conditions, pd, mode):
        import os
        os.makedirs('diabetes', exist_ok=True)
        mean_fr = np.hstack((np.mean(mn_rate_mean_mean[conditions[0]]),
                             np.mean(mn_rate_mean_mean[conditions[1]]),
                                     np.mean(mn_rate_mean_mean[conditions[2]])))
        sem_fr = np.hstack((mn_rate_mean_mean[conditions[0]].std()/np.sqrt(len(mn_rate_mean_mean[conditions[0]])),
                               mn_rate_mean_mean[conditions[1]].std()/np.sqrt(len(mn_rate_mean_mean[conditions[1]])),
                               mn_rate_mean_mean[conditions[2]].std(ddof=1)/np.sqrt(len(mn_rate_mean_mean[conditions[2]]))))
        fig, ax = plt.subplots()
        ax.errorbar([1,2,3], mean_fr, fmt='.', yerr=sem_fr, capsize=5, color='black')
        ax.grid()
        ax.scatter(1+0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])), mn_rate_mean_mean[conditions[0]])
        ax.scatter(2+0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])), mn_rate_mean_mean[conditions[1]])
        ax.scatter(3+0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[2]])), mn_rate_mean_mean[conditions[2]])
        ax.set_xticks([1,2,3])
        ax.set_xticklabels([conditions[0], conditions[1], conditions[2]])
        ax.set_ylabel('MN firing rate (pps)')
        fig.tight_layout()
        fig.savefig(f'diabetes/mn_firing_rate_comparison_{mode}.png')
        plt.close(fig)
        # Salvar dados em CSV
        for cond in conditions:
            df = pd.DataFrame({
                'firing_rate': mn_rate_mean_mean[cond].flatten(),
                'ISI_CV': mn_rate_mean_CV[cond].flatten()
            })
            df.to_csv(f'diabetes/mn_firing_rate_{cond}_{mode}.csv', index=False)
        df_mean = pd.DataFrame({
            'condition': conditions,
            'mean_firing_rate': mean_fr,
            'sem_firing_rate': sem_fr
        })
        df_mean.to_csv(f'diabetes/mn_firing_rate_summary_{mode}.csv', index=False)



    def calculate_fr_data(trials, mode, pd, force_level, conditions_param, path_param, batch_name_param, t_start_param, t_end_param):
        """
        Função auxiliar para calcular dados de firing rate para um modo específico.
        """
        mn_rate_mean_mean = dict()
        mn_rate_mean_CV = dict()
        for condition in conditions_param:
            mn_rate_mean_mean[condition] = np.array([]).reshape(-1,1)
            mn_rate_mean_CV[condition] = np.array([]).reshape(-1,1)

        force_mean = 0
        CV_mean = 0
        n = 0

        for trial in trials:
            for condition in conditions_param:
                data = pd.read_csv(f'{path_param}spikedata_{condition}_{trial}_{batch_name_param}/cell_spike_ref_{force_level}.csv', delimiter=',')
                force = pd.read_csv(f'{path_param}force_{condition}_{trial}_{batch_name_param}/force_ref{force_level}.csv', delimiter=',').values
                data = data.values

                if condition == 'severe':
                    force = force[force[:,0]>t_start_param,1]
                    force_mean = force_mean + force
                    CV_mean = CV_mean + force.std()/force.mean()
                    n = n + 1

                # Selecionar neurônios baseado no modo
                if mode == 'randomly':
                    selected_neurons = select_mns_randomly(data, t_start=t_start_param, t_end=t_end_param, size=4)
                elif mode == 'regular':
                    selected_neurons = select_mns_regular(data, t_start=t_start_param, t_end=t_end_param)
                else:
                    raise ValueError(f"Modo '{mode}' não reconhecido. Use 'regular' ou 'randomly'.")

                mns_rate_mean = compute_fr(selected_neurons, data, t_start_param, t_end_param)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start_param, t_end_param)
                ISI_CV = ISI_CV[mns_rate_mean>=0.01].reshape(-1,1)
                mns_rate_mean = mns_rate_mean[mns_rate_mean>=0.01].reshape(-1,1)
                mn_rate_mean_mean[condition] = np.vstack((mn_rate_mean_mean[condition], mns_rate_mean))
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))

        return {
            'mn_rate_mean_mean': mn_rate_mean_mean,
            'mn_rate_mean_CV': mn_rate_mean_CV,
            'force_mean': force_mean/n if n > 0 else 0,
            'CV_mean': CV_mean/n if n > 0 else 0
        }

    def plot_mn_fr_combined_data(data_regular, data_random, conditions, pd):
        """
        Função que cria plots lado a lado usando dados pré-calculados com barras de significância.
        """
        import os
        os.makedirs('diabetes', exist_ok=True)

        # Criar figura com 1 linha e 2 colunas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Função auxiliar para calcular p-values
        def calculate_p_values(mn_data, conditions):
            p_values = {}
            # Normal vs Severe
            _, p_val = stats.ttest_ind(a=mn_data[conditions[0]], b=mn_data[conditions[2]])
            p_values["normal_vs_severe"] = p_val
            # Low_affected vs Severe
            _, p_val = stats.ttest_ind(a=mn_data[conditions[1]], b=mn_data[conditions[2]])
            p_values["low_affected_vs_severe"] = p_val
            # Normal vs Low_affected
            _, p_val = stats.ttest_ind(a=mn_data[conditions[0]], b=mn_data[conditions[1]])
            p_values["normal_vs_low_affected"] = p_val
            return p_values

        # Função auxiliar para adicionar barras de significância
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

            # Comparing low_affected vs severe (posições 2 e 3)
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

            return p_values

        # Função auxiliar para plotar dados
        def plot_data(ax, mn_data, title):
            mean_fr = np.hstack((np.mean(mn_data[conditions[0]]),
                                 np.mean(mn_data[conditions[1]]),
                                 np.mean(mn_data[conditions[2]])))
            sem_fr = np.hstack((mn_data[conditions[0]].std()/np.sqrt(len(mn_data[conditions[0]])),
                                   mn_data[conditions[1]].std()/np.sqrt(len(mn_data[conditions[1]])),
                                   mn_data[conditions[2]].std(ddof=1)/np.sqrt(len(mn_data[conditions[2]]))))

            ax.plot([1,2,3], mean_fr, marker='o', linestyle='', color='red')
            ax.grid()
            ax.scatter(1+0.1*np.random.normal(size=len(mn_data[conditions[0]])), mn_data[conditions[0]], alpha=0.6)
            ax.scatter(2+0.1*np.random.normal(size=len(mn_data[conditions[1]])), mn_data[conditions[1]], alpha=0.6)
            ax.scatter(3+0.1*np.random.normal(size=len(mn_data[conditions[2]])), mn_data[conditions[2]], alpha=0.6)
            ax.set_xticks([1,2,3])
            ax.set_xticklabels([cond.replace('_', ' ').title() for cond in conditions])
            ax.set_ylabel('MN firing rate (pps)')
            ax.set_title(title)

            # Calcular p-values e adicionar barras de significância
            p_values = calculate_p_values(mn_data, conditions)
            p_values = add_significance_bars(ax, mean_fr, p_values)

            return mean_fr, sem_fr, p_values

        # Plot para modo regular (esquerda)
        mean_fr_regular, sem_fr_regular, p_values_regular = plot_data(ax1, data_regular['mn_rate_mean_mean'], 'HD-EMG Mode')

        # Plot para modo random (direita)
        mean_fr_random, sem_fr_random, p_values_random = plot_data(ax2, data_random['mn_rate_mean_mean'], 'Random Mode')

        # Adicionar legenda para significância se houver alguma significância
        has_significance = (any(p < 0.05 for p in p_values_regular.values()) or
                           any(p < 0.05 for p in p_values_random.values()))
        # if has_significance:
        #     fig.text(0.5, 0.02, "* p < 0.05, ** p < 0.01, *** p < 0.001",
        #             ha="center", fontsize=10)
        #     fig.subplots_adjust(bottom=0.1)
        # else:
        fig.tight_layout()

        # Salvar figura
        fig.savefig('diabetes/figures/mn_firing_rate_comparison_combined.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)

        # Salvar dados em CSV para ambos os modos
        for mode, data_dict in [('regular', data_regular), ('random', data_random)]:
            for cond in conditions:
                df = pd.DataFrame({
                    'firing_rate': data_dict['mn_rate_mean_mean'][cond].flatten(),
                    'ISI_CV': data_dict['mn_rate_mean_CV'][cond].flatten()
                })
                df.to_csv(f'diabetes/csv_results/mn_firing_rate_{cond}_{mode}_combined.csv', index=False)

        # Salvar resumo dos p-values
        p_values_df = pd.DataFrame({
            'comparison': ['normal_vs_severe', 'low_affected_vs_severe', 'normal_vs_low_affected'],
            'p_value_regular': [p_values_regular['normal_vs_severe'],
                               p_values_regular['low_affected_vs_severe'],
                               p_values_regular['normal_vs_low_affected']],
            'p_value_random': [p_values_random['normal_vs_severe'],
                              p_values_random['low_affected_vs_severe'],
                              p_values_random['normal_vs_low_affected']],
            'significant_regular': [p < 0.05 for p in p_values_regular.values()],
            'significant_random': [p < 0.05 for p in p_values_random.values()]
        })
        p_values_df.to_csv('diabetes/csv_results/mn_firing_rate_p_values_combined.csv', index=False)

        print("Figura combinada com barras de significância salva como: diabetes/mn_firing_rate_comparison_combined.png")
        print("P-values salvos em: diabetes/mn_firing_rate_p_values_combined.csv")

    def print_statistics(mn_rate_mean_mean, conditions_param, stats_module):
        """
        Função auxiliar para imprimir estatísticas.
        """
        print(f'FR normal: {mn_rate_mean_mean["normal"].mean():.2f}, FR low_affected: {mn_rate_mean_mean["low_affected"].mean():.2f}, FR severe: {mn_rate_mean_mean["severe"].mean():.2f}')
        t_statistic_ind, p_value_ind = stats_module.ttest_ind(a=mn_rate_mean_mean[conditions_param[0]], b=mn_rate_mean_mean[conditions_param[2]])
        print("p-value normal-severe:", p_value_ind)
        t_statistic_ind, p_value_ind = stats_module.ttest_ind(a=mn_rate_mean_mean[conditions_param[1]], b=mn_rate_mean_mean[conditions_param[2]])
        print("p-value low_affected-severe:", p_value_ind)
        t_statistic_ind, p_value_ind = stats_module.ttest_ind(a=mn_rate_mean_mean[conditions_param[0]], b=mn_rate_mean_mean[conditions_param[1]])
        print("p-value normal-low_affected:", p_value_ind)

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
        calculate_fr_data,
        compute_cv,
        compute_fr,
        plot_mn_fr,
        plot_mn_fr_combined_data,
        print_statistics,
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
    np,
    path,
    pd,
    plot_mn_fr,
    plot_mn_fr_combined_data,
    print_statistics,
    select_mns_randomly,
    select_mns_regular,
    stats,
    t_end,
    t_start,
):

    def fr_analysis(trials, mode='regular'):
        force_level = 20

        # Se mode for 'combined', calcular dados para ambos os modos
        if mode == 'combined':
            # Calcular dados para modo regular
            data_regular = calculate_fr_data(trials, 'regular', pd, force_level, conditions, path, batch_name, t_start, t_end)
            # Calcular dados para modo random
            data_random = calculate_fr_data(trials, 'randomly', pd, force_level, conditions, path, batch_name, t_start, t_end)
            # Criar plots combinados
            plot_mn_fr_combined_data(data_regular, data_random, conditions, pd)
            # Imprimir estatísticas para ambos os modos
            print("=== MODO REGULAR ===")
            print_statistics(data_regular['mn_rate_mean_mean'], conditions, stats)
            print("=== MODO RANDOM ===")
            print_statistics(data_random['mn_rate_mean_mean'], conditions, stats)
            return

        # Modo individual (regular ou randomly)
        mn_rate_mean_mean = dict()
        mn_rate_mean_mean[conditions[0]] = np.array([]).reshape(-1,1)
        mn_rate_mean_mean[conditions[1]] = np.array([]).reshape(-1,1)
        mn_rate_mean_mean[conditions[2]] = np.array([]).reshape(-1,1)
        mn_rate_mean_CV = dict()
        mn_rate_mean_CV[conditions[0]] = np.array([]).reshape(-1,1)
        mn_rate_mean_CV[conditions[1]] = np.array([]).reshape(-1,1)
        mn_rate_mean_CV[conditions[2]] = np.array([]).reshape(-1,1)
        force_mean = 0
        CV_mean = 0
        n = 0
        for trial in trials:
            for condition in conditions:
                data = pd.read_csv(f'{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv', delimiter=',')
                force = pd.read_csv(f'{path}force_{condition}_{trial}_{batch_name}/force_ref{force_level}.csv', delimiter=',').values
                data = data.values
                if condition == 'severe':
                    force = force[force[:,0]>t_start,1]
                    force_mean = force_mean + force
                    CV_mean = CV_mean +force.std()/force.mean()
                    n = n + 1
                if mode=='randomly': selected_neurons = select_mns_randomly(data, t_start=t_start, t_end=t_end, size=4)
                if mode=='regular': selected_neurons = select_mns_regular(data, t_start=t_start, t_end=t_end)
                mns_rate_mean = compute_fr(selected_neurons, data, t_start, t_end)
                ISI_CV, _ = compute_cv(selected_neurons, data, t_start, t_end)
                ISI_CV = ISI_CV[mns_rate_mean>=0.01].reshape(-1,1)
                mns_rate_mean = mns_rate_mean[mns_rate_mean>=0.01].reshape(-1,1)
                mn_rate_mean_mean[condition] = np.vstack((mn_rate_mean_mean[condition], mns_rate_mean))
                mn_rate_mean_CV[condition] = np.vstack((mn_rate_mean_CV[condition], ISI_CV))
        force_mean = force_mean/n
        unique_neurons = np.unique(data[:, 0])
        ISI_CV_all, _ = compute_cv(unique_neurons, data, t_start, t_end)
        print('Mean force: ', force_mean.mean(), 'CV force:', CV_mean)
        data = np.hstack((data, np.zeros((len(data),1))))
        for i in unique_neurons:
            data[data[:,0]==int(i),2] = ISI_CV_all[unique_neurons==int(i)]

        plot_mn_fr(mn_rate_mean_mean, mn_rate_mean_CV, conditions, pd, mode)

        print(f'FR normal: {mn_rate_mean_mean["normal"].mean()}, FR low_affected: {mn_rate_mean_mean["low_affected"].mean()}, FR severe:                        {mn_rate_mean_mean["severe"].mean()}')
        t_statistic_ind, p_value_ind = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[2]])
        print("p-value closed-open:", p_value_ind)
        t_statistic_ind, p_value_ind = stats.ttest_ind(a=mn_rate_mean_mean[conditions[1]], b=mn_rate_mean_mean[conditions[2]])
        print("p-value closed_weak-open:", p_value_ind)
        t_statistic_ind, p_value_ind = stats.ttest_ind(a=mn_rate_mean_mean[conditions[0]], b=mn_rate_mean_mean[conditions[1]])
        print("p-value closed-closed_weak:", p_value_ind)
    return (fr_analysis,)


@app.cell
def _(fr_analysis, trials):
    # Criar figura combinada com regular e random lado a lado
    fr_analysis(trials=trials, mode='combined')
    return


@app.cell
def _(
    batch_name,
    compute_cv,
    compute_fr,
    conditions,
    np,
    path,
    pd,
    plt,
    select_mns_randomly,
    t_end,
    t_start,
):
    def fr_cv(trials, pd=pd):
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
        # Inset 1 (zoom1)

        axins1 = fig.add_axes([0.5, 0.32, 0.35, 0.25])  # [left, bottom, width, height]
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
        axins2 = fig.add_axes([0.5, 0.65, 0.35, 0.25])
        axins2.scatter(mn_rate_mean_CV[conditions[0]], mn_rate_mean_mean[conditions[0]], c=neurons_index[conditions[0]], cmap=color[conditions[0]], vmin=1, vmax=250)
        axins2.scatter(mn_rate_mean_CV[conditions[1]], mn_rate_mean_mean[conditions[1]], c=neurons_index[conditions[1]], cmap=color[conditions[1]], vmin=1, vmax=250)
        axins2.scatter(mn_rate_mean_CV[conditions[2]], mn_rate_mean_mean[conditions[2]], c=neurons_index[conditions[2]], cmap=color[conditions[2]], vmin=1, vmax=250)
        axins2.set_xlim(0, 0.2)
        axins2.set_ylim(15, 25)
        axins2.set_xlabel('CV', fontsize=8)
        axins2.set_ylabel('FR', fontsize=8)
        axins2.tick_params(axis='both', which='major', labelsize=8)
        axins2.grid(True, linestyle='--', alpha=0.7)
        fig.savefig('diabetes/figures/fr_cv_scatter_full.png', bbox_inches='tight')
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
            df.to_csv(f'diabetes/csv_results/fr_cv_{cond}.csv', index=False)
    return (fr_cv,)


@app.cell
def _(fr_cv, pd, trials):
    fr_cv(trials, pd=pd)
    return


@app.cell
def _(batch_name, conditions, np, path, pd, plt, select_mns_regular):
    def what_mn_selected(trial):
        import os
        force_level = 20
        t_start = 4000
        t_end = 10000

        # Criar figura com 3 subplots verticais
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # Cores para destacar os neurônios selecionados
        colors = {
            conditions[0]: 'red',      # normal - azul
            conditions[1]: 'red',    # low_affected - laranja
            conditions[2]: 'red',     # severe - verde
        }

        for i, condition in enumerate(conditions):
            data = pd.read_csv(f'{path}spikedata_{condition}_{trial}_{batch_name}/cell_spike_ref_{force_level}.csv', delimiter=',')
            data = data.values
            selected_neurons = select_mns_regular(data, t_start=t_start, t_end=t_end)

            ax = axes[i]

            # Plot todos os neurônios em cinza claro
            ax.plot(data[:,1], data[:,0], linestyle='', marker='.', color=[0.7,0.7,0.7], markersize=4, alpha=0.8)

            # Plot neurônios selecionados em cor destacada
            selected_indices = np.nonzero(np.in1d(data[:,0], selected_neurons))[0]
            ax.plot(data[selected_indices,1], data[selected_indices,0],
                   linestyle='', marker='.', color=colors[condition], markersize=6, alpha=1)

            # Adicionar linha vertical tracejada vermelha em 4000 ms
            ax.axvline(x=4000, color='blue', linestyle='--', linewidth=2, alpha=0.8,
                      label='Início das análises (4000 ms)')

            # Configurar o subplot
            ax.set_title(f'{condition.replace("_", " ").title()}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Motor Unit ID', fontsize=12)
            ax.grid(True, alpha=0.3)

            # Adicionar legenda apenas no primeiro subplot
            if i == 0:
                ax.legend(loc='upper right', fontsize=10)

            # Configurar limites do eixo x para mostrar toda a simulação
            ax.set_xlim(0, data[:,1].max())

        # Configurar xlabel apenas no último subplot
        axes[-1].set_xlabel('Time (ms)', fontsize=12)

        # Título geral da figura
    
        # Ajustar layout
        fig.tight_layout()
        fig.subplots_adjust(top=0.93)  # Espaço para o título geral

        # Salvar figura
        os.makedirs('diabetes/figures', exist_ok=True)
        fig.savefig(f'diabetes/figures/what_mn_selected_combined_trial_{trial}.png',
                   dpi=300, bbox_inches='tight')

        # Mostrar figura
        plt.show()
        plt.close(fig)

        print(f"Figura combinada salva como: diabetes/figures/what_mn_selected_combined_trial_{trial}.png")
    return (what_mn_selected,)


@app.cell
def _(what_mn_selected):
    what_mn_selected(30)
    return


@app.cell
def _(batch_name, compute_cv, conditions, np, path, pd, plt, t_end, t_start):
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
            filename = f"diabetes/figures/isi_cov_histograms_all_units_{mode}_{batch_name}.png"
            fig.savefig(filename, dpi=300, bbox_inches="tight")
            plt.show()
            plt.close(fig)

            print(
                f"Histogramas de CoV dos ISI (todos os motor units) salvos como: {filename}"
            )

    return (isi_cov_histograms,)


@app.cell
def _(isi_cov_histograms, trials):
    isi_cov_histograms(trials, mode="regular")
    return


@app.cell
def _(
    calculate_pvalues_and_print,
    compute_cv,
    compute_fr,
    conditions,
    np,
    path,
    pd,
    plot_mn_cv_single_mode,
    plot_mn_fr_single_mode,
    plt,
    posthoc_dunn,
    select_mns_randomly,
    select_mns_regular,
    t_end,
    t_start,
):
    def fr_analysis_single_mode(trials, mode="regular", pd=pd, batch_name="", save_plot=False, save_cv_plot=False, show_stats=True, 
            title="", stats=None):
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


    def fr_analysis_combined_batches(trials, pd=pd, stats=None):
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
                    ax.plot([1, 2, 3], mean_fr, marker="o", color="red", linestyle='')
                    ax.grid()
                    ax.scatter(1 + 0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[0]])),                    
                               mn_rate_mean_mean[conditions[0]],
                               color=(0.0039, 0.451, 0.698), alpha=0.6)
                    ax.scatter(2 + 0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[1]])),
                               mn_rate_mean_mean[conditions[1]],
                               color=(0.8709, 0.5608, 0.0196), alpha=0.6)
                    ax.scatter(3 + 0.1*np.random.normal(size=len(mn_rate_mean_mean[conditions[2]])),
                               mn_rate_mean_mean[conditions[2]],
                               color=(0.0078, 0.6196, 0.451), alpha=0.6)
                
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
                            "HD-EMG Mode" if mode == "regular" else "Random Mode"
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
            # fig.text(
            #     0.5,
            #     0.02,
            #     "* p < 0.05, ** p < 0.01, *** p < 0.001",
            #     ha="center",
            #     fontsize=12,
            # )

            # Ajustar layout
            fig.tight_layout()
            fig.subplots_adjust(bottom=0.08, left=0.1)

            # Salvar figura
            fig.savefig(
                "diabetes/figures/mn_firing_rate_combined_batches.png",
                dpi=300,
                bbox_inches="tight",
            )
            plt.show()
            plt.close(fig)

            print(
                "Figura combinada salva como: diabetes/figures/mn_firing_rate_combined_batches.png"
            )

    return (fr_analysis_combined_batches,)


@app.cell
def _(fr_analysis_combined_batches, np, pd):
    fr_analysis_combined_batches(np.arange(10), pd=pd, stats=None)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
