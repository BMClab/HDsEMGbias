# HDsEMG_rev_gdocs

- Document ID: 1q9JPv3uQm6c1VW3Gh_aCiSs1MNyepxrVoqJ3N6-XzAU
- Revision ID: AIroW34FWqDjtBLpN7aEEantw2wEKJjV6cjsQ5uYjuqgKCC3Z72ZGaznEFlN-sHgWY6L_3a2TwKv4C-O4ThKbH1RuFpbmGVWAGVD6pNkC_Y
- Selected tab: t.0
- Protected controls: 0
- Opaque controls: 0
- Authoritative dropdowns: 0

Protected-control annotations are preservation instructions. Do not insert their displayed placeholder text to recreate a native control.

## Tab 1 (t.0)

[P00001 | 1:132 | NORMAL_TEXT]
Computational modeling reveals a potential selection bias in high-density surface electromyography analysis of diabetic neuropathy

[P00002 | 132:133 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00003 | 133:198 | NORMAL_TEXT]
Renato Naville Watanabe, Rebeka Lorena Batichotti, Marcos Duarte

[P00004 | 198:199 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00005 | 199:299 | NORMAL_TEXT]
Biomedical Engineering Program, Federal University of ABC, São Bernardo do Campo, São Paulo, Brazil

[P00006 | 299:300 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00007 | 300:322 | NORMAL_TEXT]
Corresponding author:

[P00008 | 322:346 | NORMAL_TEXT]
Renato Naville Watanabe

[P00009 | 346:384 | NORMAL_TEXT]
E-mail: renato.watanabe@ufabc.edu.br

[P00010 | 384:393 | HEADING_1]
Abstract

[P00011 | 393:2268 | NORMAL_TEXT]
Experimental studies using high-density surface electromyography (HD-sEMG) have reported lower motor-unit (MU) discharge rates in patients with diabetic peripheral neuropathy (DPN) than in healthy controls during matched-force contractions. Whether this difference reflects altered physiology or selection bias in the MUs identified by HD-sEMG decomposition remains unclear. We used a computational model of the neuromuscular system to investigate MU firing behavior under simulated normal and DPN conditions. For each of 50 paired simulated subjects, we compared two strategies for sampling 10 active MUs: HD-sEMG-like selection and uniform random selection from the complete active-MU pool. HD-sEMG-like sampling yielded lower mean MU firing rates in DPN (mean±SD: Normal, 9.14±0.45 pps; DPN, 8.04±0.62 pps; p<0.001), consistent with experimental reports. By contrast, random sampling yielded higher mean firing rates in DPN (Normal, 13.05±1.99 pps; DPN, 14.06±1.83 pps; p=0.024). Because all active MUs were available in the simulations, we also calculated each subject’s full-population mean firing rate, defined as the simulation truth. The across-subject simulation-truth values were likewise higher in DPN (Normal, 13.00±0.27 pps; DPN, 14.04±0.40 pps; p<0.001). Thus, HD-sEMG-like selection reversed the direction of the underlying between-condition difference. In the model, the higher firing rates in DPN were consistent with compensation for reduced MU force-generating capacity while maintaining the same target force. These findings demonstrate that lower discharge rates in HD-sEMG-decomposed samples can arise from MU selection bias and, therefore, do not necessarily reflect a genuine reduction in firing rates across the entire motor unit population. HD-sEMG findings should consequently be interpreted with caution when comparing normal and DPN populations.

[P00012 | 2268:2269 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00013 | 2269:2405 | NORMAL_TEXT]
Keywords: Diabetic peripheral neuropathy, High-density surface electromyography, Motor unit, Computational modeling, EMG decomposition

[P00014 | 2405:2420 | HEADING_1]
1 Introduction

[P00015 | 2420:3520 | NORMAL_TEXT]
The intricate discharge patterns of motoneurons constitute a fundamental aspect of neuromuscular control, governing muscle force generation and the execution of movement; these patterns can be interpreted as control signals underlying all motor actions (Enoka and Farina 2021). Currently, high-density surface electromyography (HD-sEMG) is considered the most established non-invasive technique for analyzing motor unit (MU) discharge behavior in humans (Valli et al. 2024). This method involves recording muscle electrical activity from the skin's surface using a grid of closely spaced electrodes, thereby providing detailed spatial information across a muscle (Li et al. 2015). HD-sEMG facilitates the study of properties such as MU recruitment and derecruitment thresholds, discharge rates, motor unit action potential (MUAP) shape, and conduction velocity. The core process for extracting this information from the complex interference EMG signal is EMG signal decomposition, which involves breaking down the signal into its constituent MUAP trains (Farina and Holobar 2016; Negro et al. 2016).

[P00016 | 3520:4440 | NORMAL_TEXT]
Recently, HD-sEMG has been applied to investigate motoneuron firing rates in diabetic patients, particularly in the context of diabetic peripheral neuropathy (DPN). In these studies, when individuals are asked to produce the same level of force, it has consistently been observed that individuals with DPN exhibit reduced MU discharge rates without an increase in the number of motor units recruited compared to healthy controls (Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; K. Watanabe et al. 2013; Valli et al. 2025). The authors of these studies have speculated that the reduced MU discharge rates could be attributed to attenuated afferent input, changes in motoneuron properties, neuromuscular remodeling, or changes in muscle fiber properties (Allen, Kimpinski, et al. 2014; K. Watanabe et al. 2013; Allen, Kimpinski, et al. 2014; Allen, Major, et al. 2014; K. Watanabe et al. 2013).

[P00017 | 4440:5404 | NORMAL_TEXT]
This finding is unexpected because it would imply greater efficiency in motor recruitment in individuals with a pathology than in healthy individuals, and none of the speculations put forward can satisfactorily explain this unprecedented efficiency. Patients with DPN present alterations such as reduced conduction velocity of the motoneuron axon, prolonged duration of motor unit contraction, reduced volume of the corticospinal tract, and reinnervation of muscle fibers (Favretto et al. 2023; Almeida, Riddell, and Cafarelli 2008; K. Watanabe et al. 2013; Allen, Kimpinski, et al. 2014; Xiong et al. 2016; Aye et al. 2012). In addition, altered calcium uptake has been reported in the muscles of individuals with DPN; some studies showed decreased calcium uptake (Klueber and Feczko 1994), while others showed increased uptake (Eshima, Poole, and Kano 2014). Nevertheless, none of these alterations would explain reduced MU discharge rates in patients with DPN.

[P00018 | 5404:6712 | NORMAL_TEXT]
However, it is known that the use of HD-sEMG introduces a bias toward the identification of primarily high-threshold motor units, as these produce larger signal amplitudes that are more easily detected by electrodes on the skin surface (Caillet et al. 2022). Furthermore, the decomposition methods employed in HD-sEMG adopt certain criteria that, in our view, might also result in bias during MU identification. First, there is an inherent bias towards identifying motoneurons with lower discharge frequencies, because MUAPs from higher-frequency motoneurons are more likely to be superimposed, impeding their accurate identification. Second, the identification methods exclude motoneurons with low firing rates, and third, they exclude those with a large interspike interval coefficient of variation (ISI-CoV) because they are considered unreliable for MU identification (Valli et al. 2024; Allen et al. 2015; Negro et al. 2016; Ales Holobar and Zazula 2007). These four biases can result in an identified sample that does not adequately represent the pool of recruited motor units. This may make it impossible to compare groups of individuals if one group presents relatively more alterations precisely in the motor units with characteristics most affected by surface detection and identification methods.

[P00019 | 6712:7793 | NORMAL_TEXT]
In this context, we hypothesize that the previously observed reduced MU discharge rates in individuals with DPN relative to healthy controls are, in fact, an artifact introduced by surface detection and by the methods employed for the decomposition of HD-sEMG signals. That is, if these biases are removed, there will be no difference in the MU discharge rates of individuals with DPN compared to healthy controls. To test this hypothesis, assuming that current HD-sEMG measurement and decomposition methods are inadequate for such comparisons, we will employ detailed computational modeling and simulation of a pool of MUs driven by descending commands. This approach allows us to fully manipulate the properties of these components to incorporate the physiological alterations observed in individuals with DPN and represent force production in both healthy individuals and those with DPN. In this way, we will be able to replicate the relevant aspects of the cited original experiments and investigate simulated motoneuron firing behavior under specific pathological conditions.

[P00020 | 7793:7794 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00021 | 7794:7804 | HEADING_1]
2 Methods

[P00022 | 7804:7828 | HEADING_2]
The computational model

[P00023 | 7828:8751 | NORMAL_TEXT]
We developed a computational model to simulate relevant human neurophysiological characteristics for producing a constant isometric muscle force, replicating the conditions of the experimental studies mentioned earlier. The model comprises four components designed to simulate relevant behaviors: 1) a pool of 400 neurons to generate descending commands; 2) a pool of 250 motoneurons, each modeled as a two-compartment neuron (soma and dendrite) with calcium dynamics whose firing behavior follows a gamma-point process; 3) corresponding “muscle fibers” whose force was modeled as a second-order system driven by the motoneurons (muscle-tendon dynamics were excluded as we focused on constant isometric muscle force at low levels); and 4) a controller consisting of a proportional-integral feedback loop representing visual feedback to maintain a target force level by modulating the firing rate of the descending command.

[P00024 | 8751:9229 | NORMAL_TEXT]
A schematic diagram of the model is depicted in Figure 1, and its mathematical formulation is detailed in the Appendix. This model is based on one previously developed by our group (Watanabe et al., 2013). The computational model was implemented in Python using the NEURON (M. L. Hines, Davison, and Muller 2009; M. Hines 1993) and PyNN (Davison et al. 2008) libraries. The computational code developed for this work is freely available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00025 | 9229:9230 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00026 | 9230:9232 | NORMAL_TEXT]
[INLINE_OBJECT i.0]

[P00027 | 9232:9708 | NORMAL_TEXT]
Figure 1. Schematic diagram representing force generation (F) by motor units recruited by descending commands with firing rate frequency distributed across a range. Each command activates a subset of motoneurons, leading to calcium influx (Ca²⁺) and muscle contraction through a calcium dynamics model. The total force (F) is the sum of the individual forces of the motor units. A feedback loop with a delay modulates the intervals between peaks based on the force generated.

[P00028 | 9708:9709 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00029 | 9709:9731 | HEADING_2]
Simulation conditions

[P00030 | 9731:10011 | NORMAL_TEXT]
To investigate the potential effects of DPN on motoneuron firing characteristics, simulations were conducted under two conditions with varied parameters: the normal condition represented a group of healthy subjects, and the DPN condition represented a group of patients with DPN.

[P00031 | 10011:11166 | NORMAL_TEXT]
Motor unit parameters were systematically adjusted across the two simulated conditions (see Table 1). For the DPN group, to represent the neuromuscular changes observed in diabetic neuropathy, the minimum and maximum motor unit twitch forces ([EQUATION], [EQUATION]) were reduced by a factor of 1.4, while the minimum and maximum motor unit time of contraction ([EQUATION], [EQUATION]) were concurrently increased by the same factor. To represent the conduction velocity of the nerves in diabetic neuropathy, conduction velocities of the motor nerve ([EQUATION]) were decreased by a factor of 0.85. To represent the decreased volume of the corticospinal tract in diabetic neuropathy, the number of neurons of corticospinal tract ([EQUATION]) was also reduced from 400 to 200. Importantly, the number of motoneurons, force feedback delay, and gamma order of the independent processes of the descending command remained constant across the two scenarios. All the other parameters were kept the same as used previously [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9). The parameter values that changed to represent normal and altered states are shown in Table 1. 

[P00032 | 11166:11167 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00033 | 11167:11548 | NORMAL_TEXT]
Table 1. Parameters adjusted in the two simulated conditions to represent diabetic neuropathy. Contraction force values ([EQUATION], [EQUATION]), contraction time ([EQUATION], [EQUATION]), motor conduction velocity ([EQUATION]) and number of neurons in the corticospinal tract ([EQUATION]) were modified to simulate normal and diabetic peripheral neuropathy (DPN) conditions.

[P00034 | 11548:11549 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00035 | 11552:11562 | NORMAL_TEXT | TABLE row=0 col=0]
Parameter

[P00036 | 11563:11570 | NORMAL_TEXT | TABLE row=0 col=1]
Normal

[P00037 | 11571:11575 | NORMAL_TEXT | TABLE row=0 col=2]
DPN

[P00038 | 11577:11591 | NORMAL_TEXT | TABLE row=1 col=0]
[EQUATION] (N)

[P00039 | 11592:11597 | NORMAL_TEXT | TABLE row=1 col=1]
0.04

[P00040 | 11598:11605 | NORMAL_TEXT | TABLE row=1 col=2]
0.0286

[P00041 | 11607:11621 | NORMAL_TEXT | TABLE row=2 col=0]
[EQUATION] (N)

[P00042 | 11622:11624 | NORMAL_TEXT | TABLE row=2 col=1]
4

[P00043 | 11625:11630 | NORMAL_TEXT | TABLE row=2 col=2]
2.86

[P00044 | 11632:11651 | NORMAL_TEXT | TABLE row=3 col=0]
[EQUATION] (ms)

[P00045 | 11652:11656 | NORMAL_TEXT | TABLE row=3 col=1]
110

[P00046 | 11657:11661 | NORMAL_TEXT | TABLE row=3 col=2]
154

[P00047 | 11663:11681 | NORMAL_TEXT | TABLE row=4 col=0]
[EQUATION](ms)

[P00048 | 11682:11685 | NORMAL_TEXT | TABLE row=4 col=1]
25

[P00049 | 11686:11689 | NORMAL_TEXT | TABLE row=4 col=2]
35

[P00050 | 11691:11706 | NORMAL_TEXT | TABLE row=5 col=0]
[EQUATION](m/s)

[P00051 | 11707:11710 | NORMAL_TEXT | TABLE row=5 col=1]
44

[P00052 | 11711:11716 | NORMAL_TEXT | TABLE row=5 col=2]
37.4

[P00053 | 11718:11733 | NORMAL_TEXT | TABLE row=6 col=0]
[EQUATION](m/s)

[P00054 | 11734:11737 | NORMAL_TEXT | TABLE row=6 col=1]
53

[P00055 | 11738:11744 | NORMAL_TEXT | TABLE row=6 col=2]
45.05

[P00056 | 11746:11750 | NORMAL_TEXT | TABLE row=7 col=0]
[EQUATION]

[P00057 | 11751:11755 | NORMAL_TEXT | TABLE row=7 col=1]
400

[P00058 | 11756:11760 | NORMAL_TEXT | TABLE row=7 col=2]
200

[P00059 | 11761:11762 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00060 | 11762:12378 | NORMAL_TEXT]
To introduce variability and account for biological fluctuations inherent in physiological systems, each parameter value for every simulation trial was subjected to perturbation. A random deviation from the default value was generated following a zero-mean normal distribution with a 5% coefficient of variation, thereby ensuring a degree of stochasticity while maintaining overall parameter ranges within physiologically plausible bounds. Although no formal sensitivity analysis was performed, this requirement was partially addressed by incorporating parameter variability to represent physiological fluctuations.

[P00061 | 12378:13125 | NORMAL_TEXT]
For each simulation condition, 50 trials of a 10-s isometric contraction at 20% of the maximum voluntary contraction (MVC) were conducted. The model's MVC was determined in a separate simulation trial in which all motoneurons were recruited at the maximum rate for 10 seconds; the MVC was estimated as the average force over the last 6 seconds of the simulation. To evaluate the potential influence of contraction intensity on the observed selection bias, we performed additional simulations at 10% and 50% of the maximum voluntary contraction (MVC). For each of these levels, 10 trials per condition (Normal and DPN) were conducted following the same computational protocols and parameter variability described for the primary 20% MVC condition.

[P00062 | 13125:13426 | NORMAL_TEXT]
The simulations were numerically integrated using the implicit Euler method, with derivatives estimated by Newton’s method. The numerical integration time step was 0.05 ms. These are typical values previously employed in published studies on neural computational simulation (Watanabe and Kohn, 2015).

[P00063 | 13426:13427 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00064 | 13427:13436 | HEADING_2]
Analysis

[P00065 | 13436:15081 | NORMAL_TEXT]
Motoneuron activity was analyzed using two distinct sampling modes. First, a targeted selection mode was utilized, designated as the HD-sEMG mode. This mode focused on simulated motoneurons exhibiting specific discharge characteristics corresponding to the typical firing behavior and reliability indices of motor units amenable to consistent and accurate identification via current HD-sEMG decomposition methods (Negro et al. 2016). These characteristics included mean discharge frequencies ranging from 5 to 15 pulses per second (pps) and an interspike interval coefficient of variation (ISI-CoV) below 0.3. These criteria are consistent with those used in previous studies reporting reduced motoneuron discharge rates in diabetic patient populations (Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Almeida, Riddell, and Cafarelli 2008; K. Watanabe et al. 2013; Valli et al. 2025). Furthermore, to replicate the nature of surface detection in HD-sEMG (Caillet et al. 2022), only the largest motor units exhibiting the aforementioned characteristics were selected. We chose to select the ten largest simulated motoneurons, approximating the total number of identified motor units common in experimental studies. Second, a Random sampling mode was employed, in which motoneurons were randomly sampled from the entire simulated motoneuron pool. This technique aimed to capture the global dynamics of the simulated motoneuron population. The first 4 s of the simulated signals were discarded from the analyses to avoid transient effects, but for completeness we also present the results for the whole motor unit pool. 

[P00066 | 15081:15988 | NORMAL_TEXT]
Motoneuron activity was assessed by analyzing two signals derived from the recorded spike times of the simulation: instantaneous firing rate and interspike intervals. Interspike intervals were determined by calculating the temporal differences between successive action potential occurrences. Instantaneous firing rate was computed as the reciprocal of the interspike intervals (Tomar and Kostal 2021). From these two signals, two metrics were computed: the mean firing rate and the coefficient of variation of the interspike intervals (ISI-CoV). These two metrics were used to filter units in the HD-sEMG selection mode. An additional analysis of the existing simulations was performed by applying a random sampling of ten motor units from the entire population of units that met the HD-sEMG eligibility criteria (mean discharge rate of 5–15 pps and an ISI-CoV < 0.3), rather than prioritizing unit size. 

[P00067 | 15988:16377 | NORMAL_TEXT]
For each simulated subject/trial, the target measurand was the mean firing rate across the complete population of active motor units during the steady-state interval. Because all motor units were accessible in the simulation, this trial-specific true value was known exactly and served as the full-population reference against which the HD-sEMG and Random sampling methods were evaluated.

[P00068 | 16377:17722 | NORMAL_TEXT]
The average firing rate served as the dependent variable for comparing the Normal and DPN groups. Within each selection mode (HD-sEMG and Random), firing rates were first averaged across the selected motor units in each simulation, making the simulation the unit of statistical inference. Normal and DPN observations were paired by simulation. Reported values are mean ± SD across ‘simulated subjects’. For the simulation-truth series, the SD represents between-subject variation in the trial-specific true values, not uncertainty in those values. For each group, the mean firing rate and its bias-corrected and accelerated (BCa) 95% bootstrap confidence interval were calculated. The mean paired difference between groups (DPN minus Normal) and its BCa 95% bootstrap confidence interval were also estimated. Confidence intervals were based on 100,000 bootstrap resamples of the simulations, sampled with replacement; paired resampling was used when estimating the between-group difference to preserve the Normal–DPN correspondence within each simulation. Two-sided Wilcoxon signed-rank tests were used to obtain p-values for the paired comparisons because the data were not normally distributed. A significance level of 0.05 was adopted. The analyzes were performed in Python, and all code is available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00069 | 17722:17723 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00070 | 17723:17733 | HEADING_1]
3 Results

[P00071 | 17733:18337 | NORMAL_TEXT]
Figure 2 shows the mean motor-unit (MU) firing rates obtained from 50 paired simulated subjects under the Normal and DPN conditions. For each subject and condition, 10 active MUs were selected using two sampling strategies. In the HD-sEMG mode, the 10 MUs with the lowest firing rates were selected from those meeting the HD-sEMG-like eligibility criteria: firing rates between 5 and 15 pps and an interspike interval coefficient of variation (ISI-CoV) of 0.3 or less. In the Random mode, 10 active MUs were uniformly sampled from the complete active-MU pool without applying these eligibility criteria.

[P00072 | 18337:19305 | NORMAL_TEXT]
In the HD-sEMG mode, mean firing rate was significantly lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 9.14 ± 0.45 pps, 95% BCa CI [9.02, 9.27]; DPN, 8.04 ± 0.62 pps, 95% BCa CI [7.89, 8.23]). The mean paired difference (DPN minus Normal) was −1.10 pps (95% BCa CI [−1.28, −0.92]; Wilcoxon signed-rank W = 12.0, p < 0.001). In the Random mode, the difference was in the opposite direction: mean firing rate was significantly higher in the DPN condition (Normal, 13.05 ± 1.99 pps, 95% BCa CI [12.51, 13.61]; DPN, 14.06 ± 1.83 pps, 95% BCa CI [13.53, 14.54]). The mean paired difference was 1.01 pps (95% BCa CI [0.27, 1.76]; W = 404.0, p = 0.024). The full-population simulation truth likewise showed a higher mean firing rate in the DPN condition (Normal, 13.00 ± 0.27 pps, 95% BCa CI [12.93, 13.08]; DPN, 14.04 ± 0.40 pps, 95% BCa CI [13.93, 14.14]). The mean paired difference was 1.03 pps (95% BCa CI [0.93, 1.13]; W = 0.0, p < 0.001).

[P00073 | 19305:19306 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00074 | 19306:19308 | NORMAL_TEXT]
[INLINE_OBJECT i.1]

[P00075 | 19308:19924 | NORMAL_TEXT]
Figure 2. Mean motor-unit (MU) firing rate in the Normal and diabetic peripheral neuropathy (DPN) conditions under HD-sEMG-like (left) and Random (right) sampling. Each blue point represents the mean firing rate of 10 sampled MUs from one simulated subject (n = 50 per condition). Black plus signs and error bars indicate the across-subject mean and 95% BCa confidence interval. Red horizontal lines indicate the across-subject mean of the subject-specific simulation truths calculated using all active MUs; the same reference values are shown in both panels. Paired Normal–DPN comparisons: *p < 0.05; ***p < 0.001.

[P00076 | 19924:19925 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00077 | 19925:20547 | NORMAL_TEXT]
When the analysis was repeated using a random sample of ten motor units satisfying the firing-rate and ISI-CoV eligibility criteria, the mean firing rate remained significantly lower in the DPN condition (Normal: 12.15 ± 0.72 pps, 95% BCa CI [11.95, 12.35]; DPN: 11.69 ± 0.73 pps, 95% BCa CI [11.49, 11.89]). The mean paired difference (DPN minus Normal) was −0.47 pps (95% BCa CI [−0.76, −0.18]; Wilcoxon signed-rank W = 334.5, p = 0.006). Thus, applying the eligibility criteria without subsequently prioritizing the lowest-firing-rate motor units was sufficient to reproduce the decrease observed in the DPN condition.

[P00078 | 20547:20987 | NORMAL_TEXT]
In the HD-sEMG mode, the mean ISI-CoV was significantly lower in the DPN condition than in the Normal condition (Normal: 0.245 ± 0.015, 95% BCa CI [0.241, 0.249]; DPN: 0.225 ± 0.021, 95% BCa CI [0.218, 0.230]). The mean paired difference was −0.021 (95% BCa CI [−0.027, −0.014]; Wilcoxon signed-rank W = 142.0, p < 0.001). Figure 3 illustrates the relationship between ISI-CoV and firing rate for each motor unit across the 50 simulations.

[P00079 | 20987:20988 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00080 | 20988:20990 | NORMAL_TEXT]
[INLINE_OBJECT i.2]

[P00081 | 20990:21546 | NORMAL_TEXT]
Figure 3. Relationship between interspike interval coefficient of variation (ISI CoV) and mean firing rate, obtained from the Random Mode selection. Each point represents a simulated motor unit under one of the experimental conditions: normal (blue) and DPN (orange). Lighter colors correspond to smaller motor units recruited early, medium intensity colors represent intermediate-sized motor units, and darker colors indicate motor units recruited last. The inset plot magnifies regions of motor units with larger firing rates and smaller ISI-CoV values.

[P00082 | 21546:21547 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00083 | 21547:22231 | NORMAL_TEXT]
Figure 4 illustrates a representative simulation outcome, depicting the activation times of individual motor units. Motor units selected via the HD-sEMG mode are highlighted in red. A notable observation is that, under the simulated DPN condition, the distribution of selected motor unit activation times is more dispersed compared to the Normal condition. This observed pattern, while demonstrated by a single representative example here, was consistent across all simulations. Under Normal conditions, across 50 simulations, the lowest index among the selected motor units was 10, and the highest was 207. In the DPN condition, the lowest unit index was 6, and the highest was 218.

[P00084 | 22231:22232 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00085 | 22232:22234 | NORMAL_TEXT]
[INLINE_OBJECT i.3]

[P00086 | 22234:22692 | NORMAL_TEXT]
Figure 4. Activation times of motor units simulated under the different conditions: normal (top panel) and DPN (bottom panel). Each point indicates a motor unit firing over time (horizontal axis), with the motoneurons organized by identifier on the vertical axis. The motor units selected by the HD-sEMG mode are highlighted in red, while the others are shown in gray. The vertical dashed line marks a temporal reference point common to the two conditions. 

[P00087 | 22692:22693 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00088 | 22693:23118 | NORMAL_TEXT]
Figure 5 presents a histogram of the interspike interval coefficient of variation (ISI-CoV) across all motor units for each experimental condition. Across all motor units, the average coefficient of variation (CoV) was found to be lower in the DPN condition than in the Normal condition. The proportion of motor units with an ISI-CoV of less than 0.3 increased from the Normal condition (76.9%) to the DPN condition (85.4%).

[P00089 | 23118:23119 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00090 | 23119:23121 | NORMAL_TEXT]
[INLINE_OBJECT i.4]

[P00091 | 23121:23401 | NORMAL_TEXT]
Figure 5. Histograms of the interspike interval coefficient of variation (ISI CoV) of motor units under the simulated conditions: normal (left) and DPN (right). The red vertical dashed lines mark the threshold of ISI-CoV = 0.3, used as a criterion for firing in the HD-sEMG mode.

[P00092 | 23401:23402 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00093 | 23402:24727 | NORMAL_TEXT]
Additional simulations at 10% and 50% MVC revealed that the bias qualitatively persists across different force levels, although with different magnitudes. At 10% MVC, the HD-sEMG mode showed a lower mean firing rate in the DPN condition (Normal: 9.31 ± 0.39 pps, 95% BCa CI [9.05, 9.52]; DPN: 8.21 ± 0.46 pps, 95% BCa CI [7.94, 8.48]), with a mean paired difference of −1.10 pps (95% BCa CI [−1.38, −0.64]; W = 1.0, p = 0.004). In Random mode, the mean paired difference was 1.99 pps in the opposite direction (Normal: 10.04 ± 2.09 pps; DPN: 12.03 ± 1.82 pps; 95% BCa CI [0.30, 4.06]); however, the Wilcoxon comparison did not reach statistical significance (W = 10.0, p = 0.084). At 50% MVC, the HD-sEMG also showed a lower mean firing rate in the DPN condition but not statistically significant (Normal: 8.62 ± 0.66 pps; DPN: 8.28 ± 0.83 pps; mean paired difference: −0.34 pps, 95% BCa CI [−0.81, 0.22]; W = 15.0, p = 0.232). Random mode likewise showed no difference (Normal: 17.13 ± 1.87 pps; DPN: 17.24 ± 2.03 pps; mean paired difference: 0.11 pps, 95% BCa CI [−1.23, 1.45]; W = 24.0, p = 0.770). These findings demonstrate that the apparent firing rate reduction in the simulated DPN condition is consistently reproduced by the decomposition-specific selection criteria, regardless of the muscle contraction intensity.

[P00094 | 24727:24728 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00095 | 24728:24741 | HEADING_1]
4 Discussion

[P00096 | 24741:25703 | NORMAL_TEXT]
We hypothesized that the reduced motoneuron firing rates previously reported in patients with DPN — observed when matching the relative force levels of healthy individuals — are an artifact arising from biases in HD-sEMG signal decomposition. To test this, we conducted extensive simulations using a computational model of the neuromuscular system. Our results support this hypothesis: when we applied the specific selection criteria used in HD-sEMG algorithms (the HD-sEMG mode) — specifically the exclusion of motoneurons with high firing rates and high interspike interval variability (ISI-CoV) — we successfully replicated the firing rate reduction observed in DPN patients in experimental literature (Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Valli et al. 2025). However, when the entire motoneuron pool was sampled without these biases (the Random mode), the average firing rate was comparable to that of healthy controls.

[P00097 | 25703:26722 | NORMAL_TEXT]
The regularity of discharge patterns has been a cornerstone for motor unit identification since the inception of decomposition methods (Aleš Holobar and Zazula 2007). With current decomposition methods, one cannot simply remove these selection criteria, as doing so would compromise decomposition accuracy and lead to identification failure. Furthermore, the acquisition method itself, based on skin surface electrodes, introduces a bias toward the identification of primarily high-threshold motor units. Although recent algorithms aim to capture a broader range of motor units (Grison et al. 2025; Jiang et al. 2025), discharge regularity remains a restrictive filter in the methods currently applied to diabetic populations (Negro et al. 2016). This creates a systematic selection bias: motor units with irregular patterns or high discharge rates (often obscured by superimposition) are underrepresented. We argue that this bias leads to a fundamental misinterpretation of motoneuron behavior in pathological states.

[P00098 | 26722:27729 | NORMAL_TEXT]
One instance of such misinterpretation might be the observation of decreased motoneuron firing rates in patients with DPN relative to healthy individuals, despite maintaining equivalent muscle contraction force. This suggests a potential increase in neuromuscular efficiency relative to non-diabetic individuals, which is incongruent with the established understanding of pathological alterations in diabetic patients (Valli et al. 2025). However, as shown in Figure 2, which encompasses all motoneurons of the simulated population, this decrease is not observed. The increased mean firing rate observed in the DPN condition during the full-population reference analysis (14.04 ± 0.40 pps vs. 13.00 ± 0.27 pps) is an expected finding. Given that the motor units (MUs) in the DPN condition have reduced force-generating capacity—decreased by a factor of 1.4 in our simulation—the neuromuscular system requires a higher discharge rate to achieve the same target force (20% MVC) compared to healthy controls. 

[P00099 | 27729:29078 | NORMAL_TEXT]
The observed disparity can be further elucidated by examining the ISI-CoV of the motoneurons. While the overall ISI-CoV remained consistent across conditions, aligning with findings reported in the existing literature (Favretto et al. 2023; Senefeld et al. 2020), Figure 3 reveals a nuanced relationship. Specifically, at equivalent firing rates, the ISI-CoV exhibited a decrease in the simulated pathological condition. This results in lower firing rates for the selected motor units for the DPN condition at the HD-sEMG mode. Additionally, we observed that motor units firing at higher frequencies — which are not captured by decomposition methods — exhibited increased firing rates in the DPN condition. Despite the possible bias in motor unit selection by decomposition methods, it is worth analyzing the origin of the difference observed experimentally in the discharge rates of decomposed motor units. It is apparent that the selected motor units are predominantly situated within the intermediate range of the motor unit pool, although a wide spectrum of motor units is identified, particularly under the DPN condition. In this condition, more motor units exhibit firing characteristics that meet the identification criteria of HD-EMG decomposition methods, primarily due to the increased number of motor units with an ISI-CoV less than 0.3.

[P00100 | 29078:29921 | NORMAL_TEXT]
The finding that the significant reduction in discharge rates for the DPN condition was preserved when the analysis was repeated using a random sample of ten eligible units confirms that this result is robust to the specific selection rule. This indicates that the observed decrease is primarily driven by the discharge regularity (ISI-CoV) criterion rather than motor unit size. In addition, the qualitative consistency of the results across 10%, 20%, and 50% MVC suggests that the identified selection bias is a robust artifact of decomposition criteria rather than a force-dependent physiological phenomenon. While the recruited motoneuron population and discharge distributions naturally shift with force, the regularity-based filter (ISI-CoV < 0.3) consistently produces an apparent firing rate reduction in the simulated DPN condition. 

[P00101 | 29921:30647 | NORMAL_TEXT]
This study serves as a focused proof-of-concept demonstrating that the selection criteria of current HD-sEMG decomposition are sufficient to reproduce the apparent reduction in discharge rates reported in DPN. Notably, the central result is independent of the size-based detection step; the ISI-CoV < 0.3 regularity criterion alone reproduces the observed reduction (Normal 9.14 ± 0.45 pps vs. DPN 8.04 ± 0.62 pps, p < 0.001). While a spatially realistic detection stage would alter the specific units selected, it would not eliminate this fundamental regularity-based bias. Nevertheless, integrating such models like models from the volume conductor remains a valuable future extension for this open computational framework.

[P00102 | 30647:32049 | NORMAL_TEXT]
While computational models cannot fully replicate the biological complexity of the human neuromuscular system, they provide a unique platform to test hypotheses that are inaccessible experimentally (Farina and Negro 2015; R. N. Watanabe and Kohn 2015). We acknowledge that our results do not constitute direct empirical proof that DPN patients maintain normal firing rates. We did not record patient data, nor did we run raw EMG signals through a decomposition algorithm; rather, we simulated the outcome of such decomposition based on known criteria. However, the fact that a physiologically realistic model can make the pathological "deficit" disappear simply by removing observation criteria suggests that current experimental interpretations should be treated with significant caution. Anyway, the present findings must be interpreted in light of the model's limitations. We did not incorporate muscle-tendon dynamics or afferent feedback mechanisms (e.g., muscle spindles, Golgi tendon organs), which are known to be affected in DPN. Additionally, certain pathological parameters, such as the specific reduction in corticospinal tract neurons, were estimated due to a lack of precise quantitative human data. Future research should aim to bridge this gap by integrating comprehensive biomechanical elements and, ideally, applying these findings to develop bias-corrected decomposition algorithms.

[P00103 | 32049:32633 | NORMAL_TEXT]
In summary, this study demonstrates that the apparent reduction in motoneuron firing rates in DPN may be a methodological artifact rather than a physiological adaptation. The selection bias inherent in current HD-sEMG decomposition methods favors the identification of lower-frequency units, particularly as disease pathology alters discharge variability. These results highlight the need for re-evaluating reduced firing rates in DPN and suggest that future efforts should focus on validating decomposition methods that are robust to pathological alterations in motor unit behavior.

[P00104 | 32633:32634 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00105 | 32634:32643 | HEADING_1]
Appendix

[P00106 | 32643:32667 | HEADING_2]
The computational model

[P00107 | 32667:33082 | NORMAL_TEXT]
The model consists of a pool of 250 motoneurons, each modeled as a two-compartment neuron with a soma and a dendrite. The parameters of the neurons are based on data of a previous model [(R. N. Watanabe et al. 2013; R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/0RVK+zbS9) and vary exponentially between the minimal and maximal values along the motoneuron population. Here is a list of all the parameters used in model relevant to this study:

[P00108 | 33082:33083 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00109 | 33083:33134 | NORMAL_TEXT]
Table 2. List of relevant parameters of the model.

[P00110 | 33134:33135 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00111 | 33138:33148 | NORMAL_TEXT | TABLE row=0 col=0]
Parameter

[P00112 | 33149:33161 | NORMAL_TEXT | TABLE row=0 col=1]
Description

[P00113 | 33162:33167 | NORMAL_TEXT | TABLE row=0 col=2]
Unit

[P00114 | 33168:33181 | NORMAL_TEXT | TABLE row=0 col=3]
Values Range

[P00115 | 33183:33191 | NORMAL_TEXT | TABLE row=1 col=0]
[EQUATION]

[P00116 | 33192:33213 | NORMAL_TEXT | TABLE row=1 col=1]
Membrane capacitance

[P00117 | 33214:33225 | NORMAL_TEXT | TABLE row=1 col=2]
[EQUATION]

[P00118 | 33226:33228 | NORMAL_TEXT | TABLE row=1 col=3]
1

[P00119 | 33230:33238 | NORMAL_TEXT | TABLE row=2 col=0]
[EQUATION]

[P00120 | 33239:33256 | NORMAL_TEXT | TABLE row=2 col=1]
Axial resistance

[P00121 | 33257:33264 | NORMAL_TEXT | TABLE row=2 col=2]
[EQUATION]

[P00122 | 33265:33270 | NORMAL_TEXT | TABLE row=2 col=3]
0.07

[P00123 | 33272:33276 | NORMAL_TEXT | TABLE row=3 col=0]
[EQUATION]

[P00124 | 33277:33307 | NORMAL_TEXT | TABLE row=3 col=1]
Number of descending commands

[P00125 | 33308:33310 | NORMAL_TEXT | TABLE row=3 col=2]
-

[P00126 | 33311:33315 | NORMAL_TEXT | TABLE row=3 col=3]
400

[P00127 | 33317:33321 | NORMAL_TEXT | TABLE row=4 col=0]
[EQUATION]

[P00128 | 33322:33344 | NORMAL_TEXT | TABLE row=4 col=1]
Number of motor units

[P00129 | 33345:33347 | NORMAL_TEXT | TABLE row=4 col=2]
-

[P00130 | 33348:33352 | NORMAL_TEXT | TABLE row=4 col=3]
250

[P00131 | 33354:33358 | NORMAL_TEXT | TABLE row=5 col=0]
[EQUATION]

[P00132 | 33359:33387 | NORMAL_TEXT | TABLE row=5 col=1]
Motor unit twitch amplitude

[P00133 | 33388:33390 | NORMAL_TEXT | TABLE row=5 col=2]
N

[P00134 | 33391:33400 | NORMAL_TEXT | TABLE row=5 col=3]
0.04 - 4

[P00135 | 33402:33410 | NORMAL_TEXT | TABLE row=6 col=0]
[EQUATION]

[P00136 | 33411:33442 | NORMAL_TEXT | TABLE row=6 col=1]
Motor unit twitch time to peak

[P00137 | 33443:33446 | NORMAL_TEXT | TABLE row=6 col=2]
ms

[P00138 | 33447:33456 | NORMAL_TEXT | TABLE row=6 col=3]
110 - 25

[P00139 | 33458:33467 | NORMAL_TEXT | TABLE row=7 col=0]
[EQUATION]

[P00140 | 33468:33494 | NORMAL_TEXT | TABLE row=7 col=1]
Sodium reversal potential

[P00141 | 33495:33498 | NORMAL_TEXT | TABLE row=7 col=2]
mV

[P00142 | 33499:33502 | NORMAL_TEXT | TABLE row=7 col=3]
50

[P00143 | 33504:33513 | NORMAL_TEXT | TABLE row=8 col=0]
[EQUATION]

[P00144 | 33514:33548 | NORMAL_TEXT | TABLE row=8 col=1]
Slow potassium reversal potential

[P00145 | 33549:33552 | NORMAL_TEXT | TABLE row=8 col=2]
mV

[P00146 | 33553:33557 | NORMAL_TEXT | TABLE row=8 col=3]
-80

[P00147 | 33559:33568 | NORMAL_TEXT | TABLE row=9 col=0]
[EQUATION]

[P00148 | 33569:33603 | NORMAL_TEXT | TABLE row=9 col=1]
Fast potassium reversal potential

[P00149 | 33604:33607 | NORMAL_TEXT | TABLE row=9 col=2]
mV

[P00150 | 33608:33612 | NORMAL_TEXT | TABLE row=9 col=3]
-80

[P00151 | 33614:33622 | NORMAL_TEXT | TABLE row=10 col=0]
[EQUATION]

[P00152 | 33623:33660 | NORMAL_TEXT | TABLE row=10 col=1]
Proportional constant of the control

[P00153 | 33661:33667 | NORMAL_TEXT | TABLE row=10 col=2]
pps/N

[P00154 | 33668:33673 | NORMAL_TEXT | TABLE row=10 col=3]
0.05

[P00155 | 33675:33683 | NORMAL_TEXT | TABLE row=11 col=0]
[EQUATION]

[P00156 | 33684:33717 | NORMAL_TEXT | TABLE row=11 col=1]
Integral constant of the control

[P00157 | 33718:33725 | NORMAL_TEXT | TABLE row=11 col=2]
pps/Ns

[P00158 | 33726:33732 | NORMAL_TEXT | TABLE row=11 col=3]
0.005

[P00159 | 33734:33740 | NORMAL_TEXT | TABLE row=12 col=0]
[EQUATION]

[P00160 | 33741:33764 | NORMAL_TEXT | TABLE row=12 col=1]
Calcium-bound troponin

[P00161 | 33765:33769 | NORMAL_TEXT | TABLE row=12 col=2]
mol

[P00162 | 33770:33772 | NORMAL_TEXT | TABLE row=12 col=3]
-

[P00163 | 33774:33778 | NORMAL_TEXT | TABLE row=13 col=0]
[EQUATION]

[P00164 | 33779:33811 | NORMAL_TEXT | TABLE row=13 col=1]
Force produced by a muscle unit

[P00165 | 33812:33814 | NORMAL_TEXT | TABLE row=13 col=2]
N

[P00166 | 33815:33817 | NORMAL_TEXT | TABLE row=13 col=3]
-

[P00167 | 33819:33823 | NORMAL_TEXT | TABLE row=14 col=0]
[EQUATION]

[P00168 | 33824:33850 | NORMAL_TEXT | TABLE row=14 col=1]
Nerve conduction velocity

[P00169 | 33851:33855 | NORMAL_TEXT | TABLE row=14 col=2]
m/s

[P00170 | 33856:33862 | NORMAL_TEXT | TABLE row=14 col=3]
44-53

[P00171 | 33864:33868 | NORMAL_TEXT | TABLE row=15 col=0]
[EQUATION]

[P00172 | 33869:33905 | NORMAL_TEXT | TABLE row=15 col=1]
State of the fast potassium channel

[P00173 | 33906:33908 | NORMAL_TEXT | TABLE row=15 col=2]
-

[P00174 | 33909:33911 | NORMAL_TEXT | TABLE row=15 col=3]
-

[P00175 | 33913:33917 | NORMAL_TEXT | TABLE row=16 col=0]
[EQUATION]

[P00176 | 33918:33957 | NORMAL_TEXT | TABLE row=16 col=1]
Activation state of the sodium channel

[P00177 | 33958:33960 | NORMAL_TEXT | TABLE row=16 col=2]
-

[P00178 | 33961:33963 | NORMAL_TEXT | TABLE row=16 col=3]
-

[P00179 | 33965:33969 | NORMAL_TEXT | TABLE row=17 col=0]
[EQUATION]

[P00180 | 33970:34011 | NORMAL_TEXT | TABLE row=17 col=1]
Inactivation state of the sodium channel

[P00181 | 34012:34014 | NORMAL_TEXT | TABLE row=17 col=2]
-

[P00182 | 34015:34017 | NORMAL_TEXT | TABLE row=17 col=3]
-

[P00183 | 34019:34023 | NORMAL_TEXT | TABLE row=18 col=0]
[EQUATION]

[P00184 | 34024:34060 | NORMAL_TEXT | TABLE row=18 col=1]
State of the slow potassium channel

[P00185 | 34061:34063 | NORMAL_TEXT | TABLE row=18 col=2]
-

[P00186 | 34064:34066 | NORMAL_TEXT | TABLE row=18 col=3]
-

[P00187 | 34068:34076 | NORMAL_TEXT | TABLE row=19 col=0]
[EQUATION]

[P00188 | 34077:34101 | NORMAL_TEXT | TABLE row=19 col=1]
Soma membrane potential

[P00189 | 34102:34105 | NORMAL_TEXT | TABLE row=19 col=2]
mV

[P00190 | 34106:34108 | NORMAL_TEXT | TABLE row=19 col=3]
-

[P00191 | 34110:34118 | NORMAL_TEXT | TABLE row=20 col=0]
[EQUATION]

[P00192 | 34119:34147 | NORMAL_TEXT | TABLE row=20 col=1]
Dendrite membrane potential

[P00193 | 34148:34151 | NORMAL_TEXT | TABLE row=20 col=2]
mV

[P00194 | 34152:34154 | NORMAL_TEXT | TABLE row=20 col=3]
-

[P00195 | 34156:34164 | NORMAL_TEXT | TABLE row=21 col=0]
[EQUATION]

[P00196 | 34165:34191 | NORMAL_TEXT | TABLE row=21 col=1]
Soma membrane capacitance

[P00197 | 34192:34197 | NORMAL_TEXT | TABLE row=21 col=2]
[EQUATION]

[P00198 | 34198:34200 | NORMAL_TEXT | TABLE row=21 col=3]
-

[P00199 | 34202:34210 | NORMAL_TEXT | TABLE row=22 col=0]
[EQUATION]

[P00200 | 34211:34241 | NORMAL_TEXT | TABLE row=22 col=1]
Dendrite membrane capacitance

[P00201 | 34242:34247 | NORMAL_TEXT | TABLE row=22 col=2]
[EQUATION]

[P00202 | 34248:34250 | NORMAL_TEXT | TABLE row=22 col=3]
-

[P00203 | 34252:34262 | NORMAL_TEXT | TABLE row=23 col=0]
[EQUATION]

[P00204 | 34263:34296 | NORMAL_TEXT | TABLE row=23 col=1]
conductance of the soma membrane

[P00205 | 34297:34300 | NORMAL_TEXT | TABLE row=23 col=2]
mS

[P00206 | 34301:34303 | NORMAL_TEXT | TABLE row=23 col=3]
-

[P00207 | 34305:34315 | NORMAL_TEXT | TABLE row=24 col=0]
[EQUATION]

[P00208 | 34316:34353 | NORMAL_TEXT | TABLE row=24 col=1]
conductance of the dendrite membrane

[P00209 | 34354:34357 | NORMAL_TEXT | TABLE row=24 col=2]
mS

[P00210 | 34358:34359 | NORMAL_TEXT | TABLE row=24 col=3]
⟦EMPTY PARAGRAPH⟧

[P00211 | 34361:34373 | NORMAL_TEXT | TABLE row=25 col=0]
[EQUATION]

[P00212 | 34374:34394 | NORMAL_TEXT | TABLE row=25 col=1]
Sodium conductance 

[P00213 | 34395:34398 | NORMAL_TEXT | TABLE row=25 col=2]
mS

[P00214 | 34399:34408 | NORMAL_TEXT | TABLE row=25 col=3]
[EQUATION]

[P00215 | 34410:34422 | NORMAL_TEXT | TABLE row=26 col=0]
[EQUATION]

[P00216 | 34423:34451 | NORMAL_TEXT | TABLE row=26 col=1]
Fast potassium conductance 

[P00217 | 34452:34455 | NORMAL_TEXT | TABLE row=26 col=2]
mS

[P00218 | 34456:34461 | NORMAL_TEXT | TABLE row=26 col=3]
2.25

[P00219 | 34463:34475 | NORMAL_TEXT | TABLE row=27 col=0]
[EQUATION]

[P00220 | 34476:34504 | NORMAL_TEXT | TABLE row=27 col=1]
Slow potassium conductance 

[P00221 | 34505:34508 | NORMAL_TEXT | TABLE row=27 col=2]
mS

[P00222 | 34509:34513 | NORMAL_TEXT | TABLE row=27 col=3]
0.1

[P00223 | 34514:34515 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00224 | 34515:34908 | NORMAL_TEXT]
The somatic compartment of each motor neuron includes sodium, slow potassium, and fast potassium channels, modeled using the structure of the Hodgkin-Huxley model [(Hodgkin and Huxley 1952)](https://paperpile.com/c/ku2MlM/nbxX) and is described elsewhere [(Destexhe and Paré 1999; Cisi and Kohn 2008)](https://paperpile.com/c/ku2MlM/ap2G+8qUP). The differential equations that describe the membrane potentials of the soma (Vs) and dendrite (Vd) models of each motoneuron are:

[P00225 | 34908:34996 | NORMAL_TEXT]
[EQUATION]

[P00226 | 34996:35084 | NORMAL_TEXT]
[EQUATION]

[P00227 | 35084:35513 | NORMAL_TEXT]
The values of [EQUATION]and [EQUATION] (capacitance of the soma membrane, capacitance of the dendrite membrane, conductance of the soma membrane, conductance of the dendrite membrane and conductance between soma and dendrite, respectively) are the same used by [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9). The ionic current of the soma is the sum of the currents of the sodium, fast potassium and slow potassium channels:

[P00228 | 35513:35639 | NORMAL_TEXT]
[EQUATION]

[P00229 | 35639:35747 | NORMAL_TEXT]
The differential equation of the [EQUATION], [EQUATION] and  [EQUATION] state variables are as used in [(Destexhe and Paré 1999)](https://paperpile.com/c/ku2MlM/ap2G):

[P00230 | 35747:35790 | NORMAL_TEXT]
[EQUATION]

[P00231 | 35790:35898 | NORMAL_TEXT]
with [EQUATION] being the state variables [EQUATION], [EQUATION] or [EQUATION]. The constants [EQUATION] and [EQUATION] for each state variable are: 

[P00232 | 35898:36039 | NORMAL_TEXT]
[EQUATION] and [EQUATION]

[P00233 | 36039:36141 | NORMAL_TEXT]
[EQUATION] and [EQUATION]

[P00234 | 36141:36254 | NORMAL_TEXT]
[EQUATION]and [EQUATION]

[P00235 | 36254:36338 | NORMAL_TEXT]
The differential equation of the [EQUATION] state is as used in [(Nussbaumer et al. 2002)](https://paperpile.com/c/ku2MlM/JGxw): 

[P00236 | 36338:36374 | NORMAL_TEXT]
[EQUATION]

[P00237 | 36374:36379 | NORMAL_TEXT]
with

[P00238 | 36379:36482 | NORMAL_TEXT]
[EQUATION]and [EQUATION]

[P00239 | 36482:36655 | NORMAL_TEXT]
The values of [EQUATION]are the motoneuron threshold for firing and are the same used in [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9) and [EQUATION] is the membrane potential of the soma. 

[P00240 | 36655:37344 | NORMAL_TEXT]
The calcium dynamics of each motor unit follows the model developed previously by [(Kim and Heckman 2023)](https://paperpile.com/c/ku2MlM/ueNw). This model accounts for several key processes, including the concentration of sarcoplasmic calcium, the reaction of calcium and calsequestrin within the sarcoplasmic reticulum, calcium release and uptake through the sarcoplasmic reticulum membrane, calcium buffering, calcium-troponin binding, and the resulting muscle unit activation level. Muscle force is generated from the activation of the calcium dynamics model using a second-order linear model [(Cisi and Kohn 2008; Fuglevand, Winter, and Patla 1993)](https://paperpile.com/c/ku2MlM/8qUP+tjpv). The differential equation of the force generation for each motor unit is:

[P00241 | 37344:37454 | NORMAL_TEXT]
[EQUATION]

[P00242 | 37454:37775 | NORMAL_TEXT]
In the equation above [EQUATION]is force the motor unit [EQUATION] produces through time, [EQUATION] is the contraction time of the motor unit [EQUATION], [EQUATION] is the maximum twitch force of the motor unit [EQUATION] has and [EQUATION] is the muscle unit calcium-troponin binding through time obtained from the calcium dynamics model.

[P00243 | 37775:38105 | NORMAL_TEXT]
The descending command consists of [EQUATION] independent neurons (see Figure 1) (R. N. Watanabe et al. 2013). Each descending command connects to approximately 10% of the motoneurons, randomly. For this work, only excitatory synapses were used. Each synapse from the descending command generates a current following the equation below:

[P00244 | 38105:38134 | NORMAL_TEXT]
[EQUATION]

[P00245 | 38134:38331 | NORMAL_TEXT]
The dynamics of [EQUATION] follows a first-order dynamics with time constant [EQUATION] ms with each incoming spike adding a conductance of [EQUATION] nS. The synaptic delay is 0.2 ms.

[P00246 | 38331:38877 | NORMAL_TEXT]
The mean discharge rate of the gamma distribution of each descending command is modulated by the level of force produced, following a proportional-integral controller, with a force level specified at the beginning of the simulation as a reference, with the proportional constant [EQUATION] and the integral constant [EQUATION] (see Figure 1). A 60 ms temporal delay was incorporated into the force feedback loop to simulate the visual feedback, typically provided to participants during isometric contraction paradigms.

[P00247 | 38877:38878 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00248 | 38878:38891 | HEADING_1]
6 References

[P00249 | 38891:39199 | NORMAL_TEXT]
[Allen, Matti D., Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Length Dependent Loss of Motor Axons and Altered Motor Unit Properties in Human Diabetic Polyneuropathy.”](http://paperpile.com/b/ku2MlM/PRcA)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/PRcA)[125 (4): 836–43.](http://paperpile.com/b/ku2MlM/PRcA)

[P00250 | 39199:39476 | NORMAL_TEXT]
[Allen, Matti D., Brendan Major, Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Skeletal Muscle Morphology and Contractile Function in Relation to Muscle Denervation in Diabetic Neuropathy.”](http://paperpile.com/b/ku2MlM/jR7N)[Journal of Applied Physiology (Bethesda, Md. : 1985)](http://paperpile.com/b/ku2MlM/jR7N)[116 (5): 545–52.](http://paperpile.com/b/ku2MlM/jR7N)

[P00251 | 39476:39890 | NORMAL_TEXT]
[Allen, Matti D., Daniel W. Stashuk, Kurt Kimpinski, Timothy J. Doherty, Maddison L. Hourigan, and Charles L. Rice. 2015. “Increased Neuromuscular Transmission Instability and Motor Unit Remodelling with Diabetic Neuropathy as Assessed Using Novel near Fibre Motor Unit Potential Parameters.”](http://paperpile.com/b/ku2MlM/LtlU)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/LtlU)[126 (4): 794–802.](http://paperpile.com/b/ku2MlM/LtlU)

[P00252 | 39890:40127 | NORMAL_TEXT]
[Almeida, S., M. C. Riddell, and E. Cafarelli. 2008. “Slower Conduction Velocity and Motor Unit Discharge Frequency Are Associated with Muscle Fatigue during Isometric Exercise in Type 1 Diabetes Mellitus.”](http://paperpile.com/b/ku2MlM/V9si)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/V9si)[37 (2): 231–40.](http://paperpile.com/b/ku2MlM/V9si)

[P00253 | 40127:40449 | NORMAL_TEXT]
[Aye, Tandy, Naama Barnea-Goraly, Christian Ambler, Sherry Hoang, Kristin Schleifer, Yaena Park, Jessica Drobny, Darrell M. Wilson, Allan L. Reiss, and Bruce A. Buckingham. 2012. “White Matter Structural Differences in Young Children with Type 1 Diabetes: A Diffusion Tensor Imaging Study.”](http://paperpile.com/b/ku2MlM/1pPD)[Diabetes Care](http://paperpile.com/b/ku2MlM/1pPD)[35 (11): 2167–73.](http://paperpile.com/b/ku2MlM/1pPD)

[P00254 | 40449:40731 | NORMAL_TEXT]
[Caillet, Arnault H., Andrew T. M. Phillips, Dario Farina, and Luca Modenese. 2022. “Estimation of the Firing Behaviour of a Complete Motoneuron Pool by Combining Electromyography Signal Decomposition and Realistic Motoneuron Modelling.”](http://paperpile.com/b/ku2MlM/p4VN)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/p4VN)[18 (9): e1010556.](http://paperpile.com/b/ku2MlM/p4VN)

[P00255 | 40731:41025 | NORMAL_TEXT]
[Cardoso de Oliveira, Marina, Renato Naville Watanabe, and André Fabio Kohn. 2022. “Electrophysiological and Functional Signs of Guillain-Barré Syndrome Predicted by a Multiscale Neuromuscular Computational Model.”](http://paperpile.com/b/ku2MlM/GVkn)[Journal of Neural Engineering](http://paperpile.com/b/ku2MlM/GVkn)[19 (5). https://doi.org/](http://paperpile.com/b/ku2MlM/GVkn)[10.1088/1741-2552/ac91f8](http://dx.doi.org/10.1088/1741-2552/ac91f8)[.](http://paperpile.com/b/ku2MlM/GVkn)

[P00256 | 41025:41237 | NORMAL_TEXT]
[Cisi, Rogerio R. L., and André F. Kohn. 2008. “Simulation System of Spinal Cord Motor Nuclei and Associated Nerves and Muscles, in a Web-Based Architecture.”](http://paperpile.com/b/ku2MlM/8qUP)[Journal of Computational Neuroscience](http://paperpile.com/b/ku2MlM/8qUP)[25 (3): 520–42.](http://paperpile.com/b/ku2MlM/8qUP)

[P00257 | 41237:41470 | NORMAL_TEXT]
[Davison, Andrew P., Daniel Brüderle, Jochen Eppler, Jens Kremkow, Eilif Muller, Dejan Pecevski, Laurent Perrinet, and Pierre Yger. 2008. “PyNN: A Common Interface for Neuronal Network Simulators.”](http://paperpile.com/b/ku2MlM/9z19)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/9z19)[2:11.](http://paperpile.com/b/ku2MlM/9z19)

[P00258 | 41470:41648 | NORMAL_TEXT]
[Destexhe, A., and D. Paré. 1999. “Impact of Network Activity on the Integrative Properties of Neocortical Pyramidal Neurons in Vivo.”](http://paperpile.com/b/ku2MlM/ap2G)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/ap2G)[81 (4): 1531–47.](http://paperpile.com/b/ku2MlM/ap2G)

[P00259 | 41648:41791 | NORMAL_TEXT]
[Enoka, Roger M., and Dario Farina. 2021. “Force Steadiness: From Motor Units to Voluntary Actions.”](http://paperpile.com/b/ku2MlM/GtoK)[Physiology (Bethesda, Md.)](http://paperpile.com/b/ku2MlM/GtoK)[36 (2): 114–30.](http://paperpile.com/b/ku2MlM/GtoK)

[P00260 | 41791:41934 | NORMAL_TEXT]
[Eshima, Hiroaki, David C. Poole, and Yutaka Kano. 2014. “In Vivo Calcium Regulation in Diabetic Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/zhBj)[Cell Calcium](http://paperpile.com/b/ku2MlM/zhBj)[56 (5): 381–89.](http://paperpile.com/b/ku2MlM/zhBj)

[P00261 | 41934:42137 | NORMAL_TEXT]
[Farina, Dario, and Ales Holobar. 2016. “Characterization of Human Motor Units from Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/jbAP)[Proceedings of the IEEE. Institute of Electrical and Electronics Engineers](http://paperpile.com/b/ku2MlM/jbAP)[104 (2): 353–73.](http://paperpile.com/b/ku2MlM/jbAP)

[P00262 | 42137:42319 | NORMAL_TEXT]
[Farina, Dario, and Francesco Negro. 2015. “Common Synaptic Input to Motor Neurons, Motor Unit Synchronization, and Force Control.”](http://paperpile.com/b/ku2MlM/4xcD)[Exercise and Sport Sciences Reviews](http://paperpile.com/b/ku2MlM/4xcD)[43 (1): 23–33.](http://paperpile.com/b/ku2MlM/4xcD)

[P00263 | 42319:42759 | NORMAL_TEXT]
[Favretto, Mateus André, Felipe Rettore Andreis, Sandra Cossul, Francesco Negro, Anderson Souza Oliveira, and Jefferson Luiz Brum Marques. 2023. “Differences in Motor Unit Behavior during Isometric Contractions in Patients with Diabetic Peripheral Neuropathy at Various Disease Severities.”](http://paperpile.com/b/ku2MlM/5qJ6)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/5qJ6)[68 (February):102725.](http://paperpile.com/b/ku2MlM/5qJ6)

[P00264 | 42759:42932 | NORMAL_TEXT]
[Fuglevand, A. J., D. A. Winter, and A. E. Patla. 1993. “Models of Recruitment and Rate Coding Organization in Motor-Unit Pools.”](http://paperpile.com/b/ku2MlM/tjpv)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/tjpv)[70 (6): 2470–88.](http://paperpile.com/b/ku2MlM/tjpv)

[P00265 | 42932:43210 | NORMAL_TEXT]
[Grison, Agnese, Irene Mendez Guerra, Alexander Kenneth Clarke, Silvia Muceli, Jaime Ibáñez, and Dario Farina. 2025. “Unlocking the Full Potential of High-Density Surface EMG: Novel Non-Invasive High-Yield Motor Unit Decomposition.”](http://paperpile.com/b/ku2MlM/QyGL)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/QyGL)[603 (8): 2281–2300.](http://paperpile.com/b/ku2MlM/QyGL)

[P00266 | 43210:43406 | NORMAL_TEXT]
[Harris, Charles R., K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, et al. 2020. “Array Programming with NumPy.”](http://paperpile.com/b/ku2MlM/HVd0)[Nature](http://paperpile.com/b/ku2MlM/HVd0)[585 (7825): 357–62.](http://paperpile.com/b/ku2MlM/HVd0)

[P00267 | 43406:43503 | NORMAL_TEXT]
[Heckman, C. J., and Roger M. Enoka. 2012. “Motor Unit.”](http://paperpile.com/b/ku2MlM/mzRP)[Comprehensive Physiology](http://paperpile.com/b/ku2MlM/mzRP)[2 (4): 2629–82.](http://paperpile.com/b/ku2MlM/mzRP)

[P00268 | 43503:43656 | NORMAL_TEXT]
[Hines, Michael. 1993. “NEURON — A Program for Simulation of Nerve Equations.” In](http://paperpile.com/b/ku2MlM/Vcj2)[Neural Systems: Analysis and Modeling](http://paperpile.com/b/ku2MlM/Vcj2)[, 127–36. Boston, MA: Springer US.](http://paperpile.com/b/ku2MlM/Vcj2)

[P00269 | 43656:43784 | NORMAL_TEXT]
[Hines, Michael L., Andrew P. Davison, and Eilif Muller. 2009. “NEURON and Python.”](http://paperpile.com/b/ku2MlM/jjzD)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/jjzD)[3 (January):1.](http://paperpile.com/b/ku2MlM/jjzD)

[P00270 | 43784:43976 | NORMAL_TEXT]
[Hodgkin, A. L., and A. F. Huxley. 1952. “A Quantitative Description of Membrane Current and Its Application to Conduction and Excitation in Nerve.”](http://paperpile.com/b/ku2MlM/nbxX)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/nbxX)[117 (4): 500–544.](http://paperpile.com/b/ku2MlM/nbxX)

[P00271 | 43976:44208 | NORMAL_TEXT]
[Holobar, Aleš, and Damjan Zazula. 2007. “Gradient Convolution Kernel Compensation Applied to Surface Electromyograms.” In](http://paperpile.com/b/ku2MlM/C6Et)[Independent Component Analysis and Signal Separation](http://paperpile.com/b/ku2MlM/C6Et)[, 617–24. Berlin, Heidelberg: Springer Berlin Heidelberg.](http://paperpile.com/b/ku2MlM/C6Et)

[P00272 | 44208:44435 | NORMAL_TEXT]
[Holobar, Ales, and Damjan Zazula. 2007. “Multichannel Blind Source Separation Using Convolution Kernel Compensation.”](http://paperpile.com/b/ku2MlM/nHk7)[IEEE Transactions on Signal Processing: A Publication of the IEEE Signal Processing Society](http://paperpile.com/b/ku2MlM/nHk7)[55 (9): 4487–96.](http://paperpile.com/b/ku2MlM/nHk7)

[P00273 | 44435:44547 | NORMAL_TEXT]
[Hunter, John D. 2007. “Matplotlib: A 2D Graphics Environment.”](http://paperpile.com/b/ku2MlM/SRer)[Computing in Science & Engineering](http://paperpile.com/b/ku2MlM/SRer)[9 (3): 90–95.](http://paperpile.com/b/ku2MlM/SRer)

[P00274 | 44547:44777 | NORMAL_TEXT]
[Jiang, Xi, Weiyu Guo, Ziwei Cui, Chuang Lin, and Jingyong Su. 2025. “Decomposition of High-Density sEMG Signals: Extracting Multiple Spikes from Single Time Windows.”](http://paperpile.com/b/ku2MlM/K78i)[Biomedical Signal Processing and Control](http://paperpile.com/b/ku2MlM/K78i)[107 (107771): 107771.](http://paperpile.com/b/ku2MlM/K78i)

[P00275 | 44777:45164 | NORMAL_TEXT]
[Junquera-Godoy, I., J. L. Martinez-De-Juan, G. González Lorente, J. M. Carot-Sierra, J. Gomis-Tena, J. Saiz, R. López Mateu, et al. 2025. “Surface Electromyography for Characterizing Neuromuscular Changes in Diabetic Peripheral Neuropathy.”](http://paperpile.com/b/ku2MlM/wc3t)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/wc3t)[82 (June):102991.](http://paperpile.com/b/ku2MlM/wc3t)

[P00276 | 45164:45340 | NORMAL_TEXT]
[Kim, Hojeong, and Charles J. Heckman. 2023. “A Dynamic Calcium-Force Relationship Model for Sag Behavior in Fast Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/ueNw)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/ueNw)[19 (6): e1011178.](http://paperpile.com/b/ku2MlM/ueNw)

[P00277 | 45340:45603 | NORMAL_TEXT]
[Klein Horsman, M. D., H. F. J. M. Koopman, F. C. T. van der Helm, L. Poliacu Prosé, and H. E. J. Veeger. 2007. “Morphological Muscle and Joint Parameters for Musculoskeletal Modelling of the Lower Extremity.”](http://paperpile.com/b/ku2MlM/HeGb)[Clinical Biomechanics (Bristol, Avon)](http://paperpile.com/b/ku2MlM/HeGb)[22 (2): 239–47.](http://paperpile.com/b/ku2MlM/HeGb)

[P00278 | 45603:45798 | NORMAL_TEXT]
[Klueber, K. M., and J. D. Feczko. 1994. “Ultrastructural, Histochemical, and Morphometric Analysis of Skeletal Muscle in a Murine Model of Type I Diabetes.”](http://paperpile.com/b/ku2MlM/2p6W)[The Anatomical Record](http://paperpile.com/b/ku2MlM/2p6W)[239 (1): 18–34.](http://paperpile.com/b/ku2MlM/2p6W)

[P00279 | 45798:46142 | NORMAL_TEXT]
[Lecce, Edoardo, Alessio Bellini, Giuseppe Greco, Fiorella Martire, Alessandro Scotto di Palumbo, Massimo Sacchetti, and Ilenia Bazzucchi. 2025. “Physiological Mechanisms of Neuromuscular Impairment in Diabetes-Related Complications: Can Physical Exercise Help Prevent It?”](http://paperpile.com/b/ku2MlM/cyvg)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/cyvg)[, February. https://doi.org/](http://paperpile.com/b/ku2MlM/cyvg)[10.1113/JP287589](http://dx.doi.org/10.1113/JP287589)[.](http://paperpile.com/b/ku2MlM/cyvg)

[P00280 | 46142:46516 | NORMAL_TEXT]
[Liang, Lucy, Arianna Damiani, Matteo Del Brocco, Evan R. Rogers, Maria K. Jantz, Lee E. Fisher, Robert A. Gaunt, Marco Capogrosso, Scott F. Lempka, and Elvira Pirondini. 2023. “A Systematic Review of Computational Models for the Design of Spinal Cord Stimulation Therapies: From Neural Circuits to Patient-Specific Simulations.”](http://paperpile.com/b/ku2MlM/kXVU)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/kXVU)[601 (15): 3103–21.](http://paperpile.com/b/ku2MlM/kXVU)

[P00281 | 46516:46793 | NORMAL_TEXT]
[Li, Xiaoyan, Ales Holobar, Marco Gazzoni, Roberto Merletti, William Zev Rymer, and Ping Zhou. 2015. “Examination of Poststroke Alteration in Motor Unit Firing Behavior Using High-Density Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/py9H)[IEEE Transactions on Bio-Medical Engineering](http://paperpile.com/b/ku2MlM/py9H)[62 (5): 1242–52.](http://paperpile.com/b/ku2MlM/py9H)

[P00282 | 46793:47038 | NORMAL_TEXT]
[Negro, Francesco, Silvia Muceli, Anna Margherita Castronovo, Ales Holobar, and Dario Farina. 2016. “Multi-Channel Intramuscular and Surface EMG Decomposition by Convolutive Blind Source Separation.”](http://paperpile.com/b/ku2MlM/N3dD)[Journal of Neural Engineering](http://paperpile.com/b/ku2MlM/N3dD)[13 (2): 026027.](http://paperpile.com/b/ku2MlM/N3dD)

[P00283 | 47038:47244 | NORMAL_TEXT]
[Nussbaumer, R. M., D. G. Ruegg, L. M. Studer, and J-P Gabriel. 2002. “Computer Simulation of the Motoneuron Pool-Muscle Complex. I. Input System and Motoneuron Pool.”](http://paperpile.com/b/ku2MlM/JGxw)[Biological Cybernetics](http://paperpile.com/b/ku2MlM/JGxw)[86 (4): 317–33.](http://paperpile.com/b/ku2MlM/JGxw)

[P00284 | 47244:47549 | NORMAL_TEXT]
[Perantie, Dana C., Jenny Wu, Jonathan M. Koller, Audrey Lim, Stacie L. Warren, Kevin J. Black, Michelle Sadler, Neil H. White, and Tamara Hershey. 2007. “Regional Brain Volume Differences Associated with Hyperglycemia and Severe Hypoglycemia in Youth with Type 1 Diabetes.”](http://paperpile.com/b/ku2MlM/IDFc)[Diabetes Care](http://paperpile.com/b/ku2MlM/IDFc)[30 (9): 2331–37.](http://paperpile.com/b/ku2MlM/IDFc)

[P00285 | 47549:47632 | NORMAL_TEXT]
[Perkel, Jeffrey M. 2015. “Programming: Pick up Python.”](http://paperpile.com/b/ku2MlM/xpwa)[Nature](http://paperpile.com/b/ku2MlM/xpwa)[518 (7537): 125–26.](http://paperpile.com/b/ku2MlM/xpwa)

[P00286 | 47632:47875 | NORMAL_TEXT]
[Senefeld, Jonathon W., Kevin G. Keenan, Kevin S. Ryan, Sarah E. D’Astice, Francesco Negro, and Sandra K. Hunter. 2020. “Greater Fatigability and Motor Unit Discharge Variability in Human Type 2 Diabetes.”](http://paperpile.com/b/ku2MlM/TuGo)[Physiological Reports](http://paperpile.com/b/ku2MlM/TuGo)[8 (13): e14503.](http://paperpile.com/b/ku2MlM/TuGo)

[P00287 | 47875:48161 | NORMAL_TEXT]
[Singh-Peters, Lynette A., Gareth R. Jones, Kenji A. Kenno, and Jennifer M. Jakobi. 2007. “Strength and Contractile Properties Are Similar between Persons with Type 2 Diabetes and Age-,weight-, Gender- and Physical Activitymatched Controls.”](http://paperpile.com/b/ku2MlM/FCjz)[Canadian Journal of Diabetes](http://paperpile.com/b/ku2MlM/FCjz)[31 (4): 357–64.](http://paperpile.com/b/ku2MlM/FCjz)

[P00288 | 48161:48324 | NORMAL_TEXT]
[Tomar, Rimjhim, and Lubomir Kostal. 2021. “Variability and Randomness of the Instantaneous Firing Rate.”](http://paperpile.com/b/ku2MlM/Gmym)[Frontiers in Computational Neuroscience](http://paperpile.com/b/ku2MlM/Gmym)[15 (June):620410.](http://paperpile.com/b/ku2MlM/Gmym)

[P00289 | 48324:48698 | NORMAL_TEXT]
[Valli, Giacomo, Paul Ritsche, Andrea Casolo, Francesco Negro, and Giuseppe De Vito. 2024. “Tutorial: Analysis of Central and Peripheral Motor Unit Properties from Decomposed High-Density Surface EMG Signals with Openhdemg.”](http://paperpile.com/b/ku2MlM/o27l)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/o27l)[74 (February):102850.](http://paperpile.com/b/ku2MlM/o27l)

[P00290 | 48698:49064 | NORMAL_TEXT]
[Valli, Giacomo, Rui Wu, Dean Minnock, Giuseppe Sirago, Giosuè Annibalini, Andrea Casolo, Alessandro Del Vecchio, Luana Toniolo, Elena Barbieri, and Giuseppe De Vito. 2025. “Can Non-Invasive Motor Unit Analysis Reveal Distinct Neural Strategies of Force Production in Young with Uncomplicated Type 1 Diabetes?”](http://paperpile.com/b/ku2MlM/zcHs)[European Journal of Applied Physiology](http://paperpile.com/b/ku2MlM/zcHs)[125 (1): 247–59.](http://paperpile.com/b/ku2MlM/zcHs)

[P00291 | 49064:49295 | NORMAL_TEXT]
[Virtanen, Pauli, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, et al. 2020. “SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.”](http://paperpile.com/b/ku2MlM/f7C0)[Nature Methods](http://paperpile.com/b/ku2MlM/f7C0)[17 (3): 261–72.](http://paperpile.com/b/ku2MlM/f7C0)

[P00292 | 49295:49546 | NORMAL_TEXT]
[Watanabe, Kohei, Marco Gazzoni, Ales Holobar, Toshiaki Miyamoto, Kazuhito Fukuda, Roberto Merletti, and Toshio Moritani. 2013. “Motor Unit Firing Pattern of Vastus Lateralis Muscle in Type 2 Diabetes Mellitus Patients.”](http://paperpile.com/b/ku2MlM/7cHw)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/7cHw)[48 (5): 806–13](http://paperpile.com/b/ku2MlM/7cHw)[.](http://paperpile.com/b/ku2MlM/7cHw)

[P00293 | 49546:49797 | NORMAL_TEXT]
[Watanabe, Renato N., and Andre F. Kohn. 2015. “Fast Oscillatory Commands from the Motor Cortex Can Be Decoded by the Spinal Cord for Force Control.”](http://paperpile.com/b/ku2MlM/zbS9)[The Journal of Neuroscience : The Official Journal of the Society for Neuroscience](http://paperpile.com/b/ku2MlM/zbS9)[35 (40): 13687–97.](http://paperpile.com/b/ku2MlM/zbS9)

[P00294 | 49797:50096 | NORMAL_TEXT]
[Watanabe, Renato N., Fernando H. Magalhães, Leonardo A. Elias, Vitor M. Chaud, Emanuele M. Mello, and André F. Kohn. 2013. “Influences of Premotoneuronal Command Statistics on the Scaling of Motor Output Variability during Isometric Plantar Flexion.”](http://paperpile.com/b/ku2MlM/0RVK)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/0RVK)[110 (11): 2592–2606.](http://paperpile.com/b/ku2MlM/0RVK)

[P00295 | 50096:50258 | NORMAL_TEXT]
[Wolpert, Daniel M., Zoubin Ghahramani, and J. Randall Flanagan. 2001. “Perspectives and Problems in Motor Learning.”](http://paperpile.com/b/ku2MlM/6WoP)[Trends in Cognitive Sciences](http://paperpile.com/b/ku2MlM/6WoP)[5 (11): 487–94.](http://paperpile.com/b/ku2MlM/6WoP)

[P00296 | 50258:50566 | NORMAL_TEXT]
[Xiong, Y., Y. Sui, Z. Xu, Q. Zhang, M. M. Karaman, K. Cai, T. M. Anderson, W. Zhu, J. Wang, and X. J. Zhou. 2016. “A Diffusion Tensor Imaging Study on White Matter Abnormalities in Patients with Type 2 Diabetes Using Tract-Based Spatial Statistics.”](http://paperpile.com/b/ku2MlM/ypmV)[AJNR. American Journal of Neuroradiology](http://paperpile.com/b/ku2MlM/ypmV)[37 (8): 1462–69.](http://paperpile.com/b/ku2MlM/ypmV)

