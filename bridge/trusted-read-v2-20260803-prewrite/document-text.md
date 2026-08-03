# HDsEMG_rev_gdocs_v2

- Document ID: 1nHSJ8t90oEvxLQ1dZhF-E8HsKcfKzIktMI5ZSNZNU08
- Revision ID: AIroW37U6KTUeuD-lZ1hSBkw3YHZU0-UAjHdQdFy7yYIkjCPxROMjJj3IebvroVmpS0gCjcZe0h76VC8KbQZ2fY4l_AvaxAHjNa1FGk48_I
- Selected tab: t.0
- Protected controls: 0
- Opaque controls: 0
- Authoritative dropdowns: 0

Protected-control annotations are preservation instructions. Do not insert their displayed placeholder text to recreate a native control.

## Tab 1 (t.0)

[P00001 | 1:153 | NORMAL_TEXT]
Lower apparent motor-unit discharge rates in simulated diabetic peripheral neuropathy reflect HD-sEMG-like selection rather than lower population rates

[P00002 | 153:154 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00003 | 154:219 | NORMAL_TEXT]
Renato Naville Watanabe, Rebeka Lorena Batichotti, Marcos Duarte

[P00004 | 219:220 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00005 | 220:320 | NORMAL_TEXT]
Biomedical Engineering Program, Federal University of ABC, São Bernardo do Campo, São Paulo, Brazil

[P00006 | 320:321 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00007 | 321:343 | NORMAL_TEXT]
Corresponding author:

[P00008 | 343:367 | NORMAL_TEXT]
Renato Naville Watanabe

[P00009 | 367:405 | NORMAL_TEXT]
E-mail: renato.watanabe@ufabc.edu.br

[P00010 | 405:414 | HEADING_1]
Abstract

[P00011 | 414:2083 | NORMAL_TEXT]
Decomposition-based EMG studies have reported lower motor-unit (MU) discharge rates in diabetic peripheral neuropathy (DPN) than in controls at matched relative contraction intensities. Whether this reflects physiology or selective representation of active MUs remains unclear. We used a neuromuscular force-control model to simulate 50 paired subjects under Normal and DPN conditions. For each subject, we compared mean MU discharge rates from three representations: an HD-sEMG-like sample comprising the 10 lowest-rate MUs with discharge rates of 5–15 pps and an interspike-interval coefficient of variation of 0.3 or less; an unrestricted random sample of 10 active MUs; and the complete active-MU population. At 20% MVC, HD-sEMG-like selection yielded a lower rate in DPN (mean paired difference, DPN minus Normal: −1.10 pps; 95% BCa CI [−1.28, −0.92]; p < 0.001). Conversely, random sampling yielded a higher rate in DPN (1.01 pps; 95% BCa CI [0.27, 1.76]; p = 0.024), as did the complete population (1.03 pps; 95% BCa CI [0.93, 1.13]; p < 0.001). Uniform sampling from the eligible subset also yielded a lower DPN rate, but with a smaller difference, showing that eligibility reversed the direction and lower-rate prioritization amplified it. The higher full-population firing rate in DPN is physiologically plausible within the model and was consistent with compensation for the reduced force-generating capacity assigned to DPN MUs. These simulations show that MU selection can reverse between-condition discharge-rate differences; therefore, lower rates in HD-sEMG-like samples do not necessarily indicate lower rates across the complete active-MU population.

[P00012 | 2083:2084 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00013 | 2084:2220 | NORMAL_TEXT]
Keywords: Diabetic peripheral neuropathy, High-density surface electromyography, Motor unit, Computational modeling, EMG decomposition

[P00014 | 2220:2235 | HEADING_1]
1 Introduction

[P00015 | 2235:3090 | NORMAL_TEXT]
Motor-unit (MU) discharge behavior is a fundamental component of neuromuscular control because MU recruitment and rate coding shape muscle force generation and movement (Enoka and Farina 2021). High-density surface electromyography (HD-sEMG) is widely used to study this behavior non-invasively. By recording muscle electrical activity with a grid of closely spaced surface electrodes, HD-sEMG provides spatially distributed signals from which the discharge times of individual MUs can be estimated (Li et al. 2015). Signal decomposition separates the interference EMG signal into its constituent MU action-potential trains, enabling the estimation of recruitment and derecruitment thresholds, discharge rates, discharge variability, MU action-potential properties, and conduction velocity (Farina and Holobar 2016; Negro et al. 2016; Valli et al. 2024).

[P00016 | 3090:4125 | NORMAL_TEXT]
HD-sEMG and related decomposition-based methods have been used to investigate MU behavior in diabetes, but the available studies encompass different clinical phenotypes, muscles, contraction intensities, and outcomes. In individuals with confirmed DPN, lower mean MU discharge rates have been reported using intramuscular quantitative EMG and, in severe DPN, using HD-sEMG during contractions performed at matched relative intensities (Allen, Kimpinski, et al. 2014; Favretto et al. 2023). Studies in other diabetes populations have instead emphasized attenuated firing-rate modulation or greater discharge variability (K. Watanabe et al. 2013; Senefeld et al. 2020). More recently, lower MU discharge rates have also been reported in young individuals with uncomplicated type 1 diabetes (Valli et al. 2025). Collectively, these findings indicate altered MU discharge behavior across diabetes populations, but they do not establish that a lower mean discharge rate is a uniform property of DPN or of the complete active-MU population.

[P00017 | 4125:5113 | NORMAL_TEXT]
Interpreting a lower mean discharge rate in the identified MUs is particularly challenging because DPN is associated with motor-axon and MU loss, collateral reinnervation, slowed nerve conduction, altered MU contractile properties, and reduced muscle force-generating capacity (Allen, Kimpinski, et al. 2014; Allen, Major, et al. 2014; Favretto et al. 2023). These changes could alter afferent input, motoneuron excitability, MU force production, and the neural strategy used to maintain a target force; they therefore remain plausible physiological contributors to the reported discharge behavior. Reduced MU force-generating capacity may also require compensatory recruitment or greater discharge rates among other active MUs. At the same time, the mean obtained from a decomposed sample depends on which MUs are identified and retained. Consequently, an observed reduction may reflect altered physiology, selective representation of the active-MU population, or a combination of both.

[P00018 | 5113:6380 | NORMAL_TEXT]
HD-sEMG acquisition, decomposition, and subsequent analysis contain several potential selection mechanisms. Surface detection may favor MUs whose action potentials have larger amplitudes at the skin, while temporal superposition can make rapidly discharging MU action-potential trains more difficult to separate (Caillet et al. 2022; Negro et al. 2016). Decomposition-quality and analytical inclusion criteria may further restrict the accepted range of discharge rates or exclude MUs with high interspike-interval variability (Allen et al. 2015; Valli et al. 2024; Holobar and Zazula 2007a, 2007b). These mechanisms arise at different stages and need not produce the same effects. The present study did not simulate raw EMG signals, electrode geometry, MU action-potential amplitude, or the decomposition process itself. Instead, it isolated the consequences of an operational HD-sEMG-like selection procedure based on firing-rate eligibility, an interspike-interval coefficient-of-variation threshold, and preferential selection of the lower-rate eligible MUs. If the MU populations in Normal and DPN conditions have different firing-rate or variability distributions, applying the same procedure could sample systematically different portions of those populations.

[P00019 | 6380:7485 | NORMAL_TEXT]
To examine this possibility, we used a proof-of-concept computational model of neuromuscular force control to simulate paired Normal and DPN conditions during constant isometric contractions. Unlike experimental recordings, the simulations provided access to every active MU. We could therefore compare HD-sEMG-like samples of 10 MUs with unrestricted random samples of the same size and with the complete active-MU population of each simulated subject. We hypothesized that applying an HD-sEMG-like MU-selection procedure would reproduce the lower mean discharge rates reported in DPN, whereas this apparent decrease would not be observed when MUs were sampled without these restrictions or when the complete active-MU populations were compared. The prespecified primary comparison was performed at 20% MVC, with additional simulations at 10% and 50% MVC used to evaluate the influence of contraction intensity. This design allowed us to determine whether an apparent between-condition decrease produced by MU selection accurately represented the direction of the underlying population-level difference.

[P00020 | 7485:7486 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00021 | 7486:7496 | HEADING_1]
2 Methods

[P00022 | 7496:7520 | HEADING_2]
The computational model

[P00023 | 7520:8443 | NORMAL_TEXT]
We developed a computational model to simulate relevant human neurophysiological characteristics for producing a constant isometric muscle force, replicating the conditions of the experimental studies mentioned earlier. The model comprises four components designed to simulate relevant behaviors: 1) a pool of 400 neurons to generate descending commands; 2) a pool of 250 motoneurons, each modeled as a two-compartment neuron (soma and dendrite) with calcium dynamics whose firing behavior follows a gamma-point process; 3) corresponding “muscle fibers” whose force was modeled as a second-order system driven by the motoneurons (muscle-tendon dynamics were excluded as we focused on constant isometric muscle force at low levels); and 4) a controller consisting of a proportional-integral feedback loop representing visual feedback to maintain a target force level by modulating the firing rate of the descending command.

[P00024 | 8443:8917 | NORMAL_TEXT]
A schematic diagram of the model is depicted in Figure 1, and its mathematical formulation is detailed in the Appendix. This model is based on one previously developed by our group (R. N. Watanabe et al. 2013). The computational model was implemented in Python using the NEURON (Hines, Davison, and Muller 2009; Hines 1993) and PyNN (Davison et al. 2008) libraries. The computational code developed for this work is freely available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00025 | 8917:8918 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00026 | 8918:8920 | NORMAL_TEXT]
[INLINE_OBJECT i.0]

[P00027 | 8920:9355 | NORMAL_TEXT]
Figure 1. Schematic of the force-control model. Descending commands with gamma-distributed interspike intervals project to subsets of motoneurons. Motoneuron discharges drive calcium dynamics and individual motor-unit forces, whose sum gives the total force (F). A delayed proportional-integral feedback controller adjusts the mean descending-command discharge rate according to the difference between the target and generated forces.

[P00028 | 9355:9356 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00029 | 9356:9378 | HEADING_2]
Simulation conditions

[P00030 | 9378:9658 | NORMAL_TEXT]
To investigate the potential effects of DPN on motoneuron firing characteristics, simulations were conducted under two conditions with varied parameters: the Normal condition represented a group of healthy subjects, and the DPN condition represented a group of patients with DPN.

[P00031 | 9658:10727 | NORMAL_TEXT]
Motor-unit parameters were systematically adjusted across the two simulated conditions (Table 1). In the DPN condition, the twitch amplitudes of the smallest and largest motor units (Amin and Amax) were each reduced by a factor of 1.4, whereas their twitch times to peak (Tc,small and Tc,large) were increased by the same factor. These changes represented diabetes-related alterations in skeletal-muscle structure and calcium regulation (Klueber and Feczko 1994; Eshima, Poole, and Kano 2014). The minimum and maximum motor-nerve conduction velocities (vmin and vmax) were multiplied by 0.85. The number of descending-command neurons (NCST) was reduced from 400 to 200 to represent diabetes-associated white-matter alterations (Aye et al. 2012; Xiong et al. 2016). The number of motoneurons, force-feedback delay, and gamma order of the independent descending-command processes were held constant across conditions. All other parameters were retained from the previous model (R. N. Watanabe and Kohn 2015). The resulting condition-specific values are shown in Table 1.

[P00032 | 10727:10728 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00033 | 10728:11093 | NORMAL_TEXT]
Table 1. Parameters adjusted in the two simulated conditions. Twitch amplitudes for the smallest and largest motor units (Amin and Amax), twitch times to peak (Tc,small and Tc,large), minimum and maximum motor-nerve conduction velocities (vmin and vmax), and the number of descending-command neurons (NCST) were modified to represent the Normal and DPN conditions.

[P00034 | 11093:11094 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00035 | 11097:11107 | NORMAL_TEXT | TABLE row=0 col=0]
Parameter

[P00036 | 11108:11115 | NORMAL_TEXT | TABLE row=0 col=1]
Normal

[P00037 | 11116:11120 | NORMAL_TEXT | TABLE row=0 col=2]
DPN

[P00038 | 11122:11131 | NORMAL_TEXT | TABLE row=1 col=0]
Amin (N)

[P00039 | 11132:11137 | NORMAL_TEXT | TABLE row=1 col=1]
0.04

[P00040 | 11138:11145 | NORMAL_TEXT | TABLE row=1 col=2]
0.0286

[P00041 | 11147:11156 | NORMAL_TEXT | TABLE row=2 col=0]
Amax (N)

[P00042 | 11157:11159 | NORMAL_TEXT | TABLE row=2 col=1]
4

[P00043 | 11160:11165 | NORMAL_TEXT | TABLE row=2 col=2]
2.86

[P00044 | 11167:11181 | NORMAL_TEXT | TABLE row=3 col=0]
Tc,small (ms)

[P00045 | 11182:11186 | NORMAL_TEXT | TABLE row=3 col=1]
110

[P00046 | 11187:11191 | NORMAL_TEXT | TABLE row=3 col=2]
154

[P00047 | 11193:11207 | NORMAL_TEXT | TABLE row=4 col=0]
Tc,large (ms)

[P00048 | 11208:11211 | NORMAL_TEXT | TABLE row=4 col=1]
25

[P00049 | 11212:11215 | NORMAL_TEXT | TABLE row=4 col=2]
35

[P00050 | 11217:11228 | NORMAL_TEXT | TABLE row=5 col=0]
vmin (m/s)

[P00051 | 11229:11232 | NORMAL_TEXT | TABLE row=5 col=1]
44

[P00052 | 11233:11238 | NORMAL_TEXT | TABLE row=5 col=2]
37.4

[P00053 | 11240:11251 | NORMAL_TEXT | TABLE row=6 col=0]
vmax (m/s)

[P00054 | 11252:11255 | NORMAL_TEXT | TABLE row=6 col=1]
53

[P00055 | 11256:11262 | NORMAL_TEXT | TABLE row=6 col=2]
45.05

[P00056 | 11264:11269 | NORMAL_TEXT | TABLE row=7 col=0]
NCST

[P00057 | 11270:11274 | NORMAL_TEXT | TABLE row=7 col=1]
400

[P00058 | 11275:11279 | NORMAL_TEXT | TABLE row=7 col=2]
200

[P00059 | 11280:11281 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00060 | 11281:11897 | NORMAL_TEXT]
To introduce variability and account for biological fluctuations inherent in physiological systems, each parameter value for every simulation trial was subjected to perturbation. A random deviation from the default value was generated following a zero-mean normal distribution with a 5% coefficient of variation, thereby ensuring a degree of stochasticity while maintaining overall parameter ranges within physiologically plausible bounds. Although no formal sensitivity analysis was performed, this requirement was partially addressed by incorporating parameter variability to represent physiological fluctuations.

[P00061 | 11897:12830 | NORMAL_TEXT]
For each simulation condition, 50 trials of a 10-s isometric contraction at 20% of the maximum voluntary contraction (MVC) were conducted. The model's MVC was determined independently for each condition in an additional simulation trial in which all motoneurons were recruited at the maximum rate for 10 seconds; the MVC was estimated as the average force over the last 6 seconds of the simulation. All contractions were therefore performed at 20% of each condition's own maximum, matching the relative-intensity design of the experimental studies. To evaluate the potential influence of contraction intensity on the observed selection bias, we performed additional simulations at 10% and 50% of the maximum voluntary contraction (MVC). For each of these levels, 10 trials per condition (Normal and DPN) were conducted following the same computational protocols and parameter variability described for the primary 20% MVC condition.

[P00062 | 12830:13136 | NORMAL_TEXT]
The simulations were numerically integrated using the implicit Euler method, with derivatives estimated by Newton’s method. The numerical integration time step was 0.05 ms. These are typical values previously employed in published studies on neural computational simulation (R. N. Watanabe and Kohn 2015).

[P00063 | 13136:13137 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00064 | 13137:13146 | HEADING_2]
Analysis

[P00065 | 13146:14545 | NORMAL_TEXT]
Motoneuron activity was analyzed over the steady-state interval from 4 to 10 s; the first 4 s were discarded to avoid transient effects. Two sampling modes were defined. In the HD-sEMG mode, active motor units were eligible when their mean firing rate was greater than 5 and less than 15 pulses per second (pps) and their interspike interval coefficient of variation (ISI-CoV) was less than or equal to 0.3. These criteria reflect the firing behavior and reliability restrictions used in studies of motor units amenable to HD-sEMG decomposition (Negro et al. 2016; Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Almeida, Riddell, and Cafarelli 2008; K. Watanabe et al. 2013; Valli et al. 2025). When more than 10 motor units met these criteria, the 10 eligible units with the lowest mean firing rates were selected, approximating the number of identified motor units commonly reported in experimental studies. Although surface recordings may preferentially detect larger, higher-threshold motor units (Caillet et al. 2022), the present operational mode modeled discharge-based selection only and did not include an explicit amplitude- or motor-unit-size-dependent detection stage. In the Random mode, 10 unique motor units were sampled without replacement from the complete pool active during the steady-state interval, without applying the HD-sEMG eligibility criteria.

[P00066 | 14545:15229 | NORMAL_TEXT]
For each motor unit, mean firing rate was calculated as the number of discharges during the 6-s steady-state interval divided by the interval duration. Interspike intervals were calculated as the temporal differences between successive discharges (Tomar and Kostal 2021), and ISI-CoV was calculated as the sample standard deviation divided by the mean of those intervals. Reliable estimation required more than three interspike intervals; units with three or fewer intervals were assigned an ISI-CoV of 1.0 and therefore did not satisfy the HD-sEMG eligibility criterion. Mean firing rate and ISI-CoV were subsequently averaged across the selected motor units within each simulation.

[P00067 | 15229:16519 | NORMAL_TEXT]
For each simulated subject and condition, the mean firing rate across the complete population of motor units active during the steady-state interval was defined as the simulation truth. Because all active motor units were accessible in the simulation, this trial-specific full-population value was known exactly and served as the reference against which the HD-sEMG and Random sampling modes were evaluated. As a sensitivity analysis, 10 motor units were also sampled without replacement from the subset meeting the same firing-rate and ISI-CoV eligibility criteria, but without preferentially selecting the units with the lowest firing rates. This eligibility-restricted random analysis was used to distinguish the effect of the eligibility criteria from the additional effect of lowest-firing-rate prioritization. As an additional sensitivity analysis, the HD-sEMG-like selection rule was reapplied to the same simulations while varying the eligibility thresholds. The ISI-CoV threshold was varied from 0.15 to 0.50 and the firing-rate bounds were varied independently, with each combination evaluated both with lowest-rate prioritization and with all eligible MUs retained. Because every selection was recomputed from the stored discharge times, no additional simulations were required.

[P00068 | 16519:17439 | NORMAL_TEXT]
Additional motor-unit-level analyses were descriptive and were not used for group-level inference. For Figure 4, 100 active motor units were uniformly sampled without replacement from each simulated subject and condition at 20% MVC, without applying the HD-sEMG eligibility criteria, and their mean firing rate and ISI-CoV were plotted. For Figure 5, discharge rasters were plotted for paired simulated subject 30; across all 50 paired subjects, the minimum and maximum identifiers of the selected motor units and their within-subject span, defined as the maximum minus the minimum identifier, were summarized descriptively. For Figure 6, ISI-CoV values from all recorded motor units were pooled across the 50 simulated subjects within each condition to visualize their distributions and the proportion satisfying the ISI-CoV threshold. These pooled motor-unit observations were used only for descriptive visualization.

[P00069 | 17439:17789 | NORMAL_TEXT]
At 10% and 50% MVC, the same steady-state definitions and HD-sEMG, Random, and simulation-truth analyses were applied to 10 paired simulated subjects at each force level. These additional-force analyses were treated as secondary, exploratory evaluations of whether the direction of the selection effect was maintained across contraction intensities.

[P00070 | 17789:18436 | NORMAL_TEXT]
Each trial identifier represented one simulated subject evaluated under both the Normal and DPN conditions, and observations with the same trial identifier constituted a pair. Mean firing rate was the primary outcome, and simulation-level mean ISI-CoV was a secondary outcome. Within each sampling mode or full-population reference, one mean value per simulated subject and condition was used as the unit of statistical inference. Reported values are mean ± sample SD across simulated subjects. For the simulation-truth series, the SD represents between-subject variation in the trial-specific true values rather than uncertainty in those values.

[P00071 | 18436:19637 | NORMAL_TEXT]
The primary inferential comparison was specified a priori as the paired Normal–DPN difference in mean firing rate under the HD-sEMG mode at 20% MVC. The Random, eligibility-restricted random, simulation-truth, ISI-CoV, and additional-force comparisons were secondary or exploratory; their p-values were nominal and were not adjusted for multiple comparisons. For each condition, the group mean and its bias-corrected and accelerated (BCa) 95% bootstrap confidence interval were calculated. The mean paired difference between conditions (DPN minus Normal) and its BCa 95% bootstrap confidence interval were also estimated. Confidence intervals were based on 100,000 bootstrap resamples of the simulations, sampled with replacement; paired resampling was used for the between-condition difference to preserve the Normal–DPN correspondence within each simulated subject. Two-sided Wilcoxon signed-rank tests were selected a priori for paired comparisons. The primary comparison used a significance level of 0.05. Analyses were performed in Python using NumPy (Harris et al. 2020), SciPy (Virtanen et al. 2020), and Matplotlib (Hunter 2007); all code is available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00072 | 19637:19638 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00073 | 19638:19648 | HEADING_1]
3 Results

[P00074 | 19648:20252 | NORMAL_TEXT]
Figure 2 shows the mean motor-unit (MU) firing rates obtained from 50 paired simulated subjects under the Normal and DPN conditions. For each subject and condition, 10 active MUs were selected using two sampling strategies. In the HD-sEMG mode, the 10 MUs with the lowest firing rates were selected from those meeting the HD-sEMG-like eligibility criteria: firing rates between 5 and 15 pps and an interspike interval coefficient of variation (ISI-CoV) of 0.3 or less. In the Random mode, 10 active MUs were uniformly sampled from the complete active-MU pool without applying these eligibility criteria.

[P00075 | 20252:21220 | NORMAL_TEXT]
In the HD-sEMG mode, mean firing rate was significantly lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 9.14 ± 0.45 pps, 95% BCa CI [9.02, 9.27]; DPN, 8.04 ± 0.62 pps, 95% BCa CI [7.89, 8.23]). The mean paired difference (DPN minus Normal) was −1.10 pps (95% BCa CI [−1.28, −0.92]; Wilcoxon signed-rank W = 12.0, p < 0.001). In the Random mode, the difference was in the opposite direction: mean firing rate was significantly higher in the DPN condition (Normal, 13.05 ± 1.99 pps, 95% BCa CI [12.51, 13.61]; DPN, 14.06 ± 1.83 pps, 95% BCa CI [13.53, 14.54]). The mean paired difference was 1.01 pps (95% BCa CI [0.27, 1.76]; W = 404.0, p = 0.024). The full-population simulation truth likewise showed a higher mean firing rate in the DPN condition (Normal, 13.00 ± 0.27 pps, 95% BCa CI [12.93, 13.08]; DPN, 14.04 ± 0.40 pps, 95% BCa CI [13.93, 14.14]). The mean paired difference was 1.03 pps (95% BCa CI [0.93, 1.13]; W = 0.0, p < 0.001).

[P00076 | 21220:21623 | NORMAL_TEXT]
The number of MUs active during the steady-state interval was also lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 174.5 ± 2.9 of 250 MUs; DPN, 161.8 ± 3.1 of 250 MUs). The mean paired difference (DPN minus Normal) was −12.7 MUs (95% CI [−13.5, −11.9]; Wilcoxon signed-rank W = 0.0, p < 0.001), with fewer active MUs in the DPN condition in all 50 paired simulated subjects.

[P00077 | 21623:21624 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00078 | 21624:21626 | NORMAL_TEXT]
[INLINE_OBJECT kix.l2a7tks2gwfh]

[P00079 | 21626:22242 | NORMAL_TEXT]
Figure 2. Mean motor-unit (MU) firing rate in the Normal and diabetic peripheral neuropathy (DPN) conditions under HD-sEMG-like (left) and Random (right) sampling. Each blue point represents the mean firing rate of 10 sampled MUs from one simulated subject (n = 50 per condition). Black plus signs and error bars indicate the across-subject mean and 95% BCa confidence interval. Red horizontal lines indicate the across-subject mean of the subject-specific simulation truths calculated using all active MUs; the same reference values are shown in both panels. Paired Normal–DPN comparisons: *p < 0.05; ***p < 0.001.

[P00080 | 22242:22243 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00081 | 22243:22294 | HEADING_3]
Contributions of the individual selection criteria

[P00082 | 22294:23031 | NORMAL_TEXT]
To separate the effect of the eligibility criteria from that of lowest-rate prioritization, 10 MUs were uniformly sampled from the subset meeting the same firing-rate and ISI-CoV eligibility criteria used in the HD-sEMG mode, but without preferentially selecting the MUs with the lowest firing rates. Under this eligibility-restricted random sampling, mean firing rate remained significantly lower in the DPN condition (mean ± SD: Normal, 12.20 ± 0.50 pps, 95% BCa CI [12.06, 12.33]; DPN, 11.71 ± 0.72 pps, 95% BCa CI [11.51, 11.91]). The mean paired difference (DPN minus Normal) was −0.48 pps (95% BCa CI [−0.73, −0.24]; Wilcoxon signed-rank W = 261.0, p < 0.001), smaller in magnitude than the −1.10 pps observed in the HD-sEMG mode.

[P00083 | 23031:24075 | NORMAL_TEXT]
The selection rule was then reapplied to the same simulations while varying the eligibility thresholds. Figure 3 shows the paired difference in mean firing rate as a function of the ISI-CoV eligibility threshold under both selection strategies, together with the all-MU simulation truth. The lower mean firing rate in DPN persisted across ISI-CoV thresholds from 0.20 to 0.36 (paired differences −1.34 to −0.64 pps; all p < 0.001), attenuated at 0.38 (−0.37 pps; p = 0.010), and was no longer statistically significant at 0.40 (−0.22 pps; p = 0.13); at 0.45 and above the estimated difference reversed to the direction of the simulation truth. The upper firing-rate bound had no influence on the result: the paired difference was unchanged (−1.10 pps) whether the bound was set at 15, 20, or 30 pps or removed entirely, because the ten lowest-rate eligible MUs fell well below any of these values. The lower firing-rate bound modulated the magnitude (−1.25 pps with no lower bound; −0.41 pps with a 7-pps bound) without changing its direction.

[P00084 | 24075:24382 | NORMAL_TEXT]
Together, these analyses identify the ISI-CoV criterion as the component that determines the direction of the between-condition difference, with preferential selection of the lowest-rate eligible MUs approximately doubling its magnitude and the upper firing-rate bound contributing nothing under this rule.

[P00085 | 24382:24383 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00086 | 24383:24385 | NORMAL_TEXT]
[INLINE_OBJECT kix.2gty90uryvul]

[P00087 | 24385:24898 | NORMAL_TEXT]
Figure 3. Sensitivity of the between-condition difference in mean MU firing rate to the ISI-CoV eligibility threshold at 20% MVC. Blue circles show the HD-sEMG-like rule (the 10 lowest-rate eligible MUs); green squares show sampling of all eligible MUs, without lowest-rate prioritization. The red dashed line indicates the all-MU simulation truth (+1.03 pps) and the grey dotted line marks the threshold used in the main analysis (0.30). Values below zero indicate a lower mean firing rate in the DPN condition.

[P00088 | 24898:24899 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00089 | 24899:25391 | NORMAL_TEXT]
In the HD-sEMG mode, mean ISI-CoV was significantly lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 0.245 ± 0.015, 95% BCa CI [0.241, 0.250]; DPN, 0.225 ± 0.021, 95% BCa CI [0.218, 0.230]). The mean paired difference (DPN minus Normal) was −0.021 (95% BCa CI [−0.027, −0.014]; Wilcoxon signed-rank W = 142.0, p < 0.001). Figure 4 separately provides a descriptive MU-level view of the relationship between firing rate and ISI-CoV across the 50 simulated subjects.

[P00090 | 25391:25392 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00091 | 25392:25394 | NORMAL_TEXT]
[INLINE_OBJECT kix.5y8i2pd70ypw]

[P00092 | 25394:26161 | NORMAL_TEXT]
Figure 4. Relationship between mean firing rate and the interspike interval coefficient of variation (ISI-CoV) in the Normal and DPN conditions. For each simulated subject and condition, 100 active MUs were uniformly sampled without applying the HD-sEMG-like eligibility criteria, yielding 5,000 MU observations per condition across 50 subjects. Each point represents one MU and is shown descriptively rather than as an independent unit of group-level inference. Blue and orange indicate the Normal and DPN conditions, respectively. Within each condition, lighter, intermediate, and darker shades indicate earlier-recruited, intermediate, and later-recruited MUs, respectively. The inset enlarges the region containing MUs with lower ISI-CoV and higher firing rates.

[P00093 | 26161:26162 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00094 | 26162:26806 | NORMAL_TEXT]
Figure 5 shows MU discharge rasters for one paired simulated subject (simulation 30), illustrating the distribution of MUs selected by the HD-sEMG mode within the active pool. In this example, the selected MU identifiers spanned 88–146 in the Normal condition and 88–193 in the DPN condition. Across the 50 paired simulated subjects, the within-subject span of selected MU identifiers was larger on average in DPN (mean ± SD: Normal, 90.6 ± 24.3; DPN, 117.2 ± 29.5), with a larger DPN span in 37 of the 50 pairs. Across all subjects, selected MU identifiers ranged from 27 to 207 in the Normal condition and from 6 to 247 in the DPN condition.

[P00095 | 26806:26807 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00096 | 26807:26809 | NORMAL_TEXT]
[INLINE_OBJECT kix.3n3ik6tifowj]

[P00097 | 26809:27298 | NORMAL_TEXT]
Figure 5. Motor-unit (MU) discharge rasters for simulated subject 30 under the Normal (top) and DPN (bottom) conditions. Each point represents one MU discharge, with MUs ordered by identifier on the vertical axis. Red points show discharges from the 10 MUs selected by the HD-sEMG-like mode, while gray points show discharges from the remaining simulated MUs. The blue dashed line at 4,000 ms marks the beginning of the steady-state interval used for the firing-rate and ISI-CoV analyses.

[P00098 | 27298:27299 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00099 | 27299:27721 | NORMAL_TEXT]
Figure 6 presents a histogram of the interspike interval coefficient of variation (ISI-CoV) across all motor units for each simulated condition. Across all motor units, the average coefficient of variation (CoV) was found to be lower in the DPN condition than in the Normal condition. The proportion of motor units with an ISI-CoV of less than 0.3 increased from the Normal condition (76.9%) to the DPN condition (85.8%).

[P00100 | 27721:27722 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00101 | 27722:27724 | NORMAL_TEXT]
[INLINE_OBJECT kix.r8rr961cvyv3]

[P00102 | 27724:28592 | NORMAL_TEXT]
Figure 6. Pooled distributions of the interspike interval coefficient of variation (ISI-CoV) for individual motor units (MUs) under the Normal (left) and DPN (right) conditions across 50 simulated subjects. Red dashed lines mark the HD-sEMG-like eligibility threshold of ISI-CoV = 0.3, and shaded regions indicate values below this threshold. Panel annotations show the number of MUs below the threshold and the total number included in each condition. The terminal bin includes MUs assigned an ISI-CoV of 1.0 because three or fewer interspike intervals were available during the steady-state analysis window, preventing reliable estimation; these MUs therefore did not satisfy the eligibility criterion. The x-axis is limited to 1.0 to emphasize values relevant to MU selection; ISI-CoV values above 1.0 are not displayed but remain included in the annotated totals.

[P00103 | 28592:28593 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00104 | 28593:29330 | NORMAL_TEXT]
Additional simulations at 10% and 50% MVC included 10 paired simulated subjects at each force level. At 10% MVC, the HD-sEMG mode yielded a lower mean firing rate in DPN (mean ± SD: Normal, 9.31 ± 0.39 pps; DPN, 8.21 ± 0.46 pps), with a mean paired difference of −1.10 pps (95% BCa CI [−1.38, −0.63]; W = 1.0, p = 0.004). Random sampling yielded Normal and DPN means of 10.32 ± 2.06 and 11.39 ± 2.32 pps, respectively, but the paired difference was not statistically significant (1.07 pps, 95% BCa CI [−0.70, 3.80]; W = 23.0, p = 0.695). In contrast, the simulation truth showed a higher mean firing rate in DPN (Normal, 10.09 ± 0.47 pps; DPN, 11.53 ± 0.40 pps; paired difference, 1.44 pps, 95% BCa CI [0.92, 1.83]; W = 0.0, p = 0.002).

[P00105 | 29330:31040 | NORMAL_TEXT]
At 50% MVC, the HD-sEMG mode again yielded a lower mean firing rate in DPN, although the difference was not statistically significant (Normal, 8.62 ± 0.66 pps; DPN, 8.28 ± 0.83 pps; paired difference, −0.34 pps, 95% BCa CI [−0.80, 0.22]; W = 15.0, p = 0.232). Random sampling also showed no significant difference (Normal, 17.65 ± 2.01 pps; DPN, 17.11 ± 2.06 pps; paired difference, −0.55 pps, 95% BCa CI [−2.01, 1.76]; W = 18.0, p = 0.375). The simulation truth nevertheless showed a higher mean firing rate in DPN (Normal, 16.86 ± 0.20 pps; DPN, 17.41 ± 0.37 pps; paired difference, 0.55 pps, 95% BCa CI [0.37, 0.80]; W = 0.0, p = 0.002). Thus, the direction of the HD-sEMG-mode difference was reproduced at both additional force levels, whereas the simulation truth showed the opposite direction; however, evidence for the HD-sEMG-mode difference was statistically significant only at 10% MVC. These supplementary comparisons each included 10 paired simulated subjects and were correspondingly imprecise. The influence of this sample size is illustrated by the Random mode at 10% MVC, where the estimated difference (1.07 pps) was similar in magnitude to the difference obtained at 20% MVC with 50 paired subjects (1.01 pps) but was not statistically significant (p = 0.695) and had a substantially wider confidence interval ([−0.70, 3.80] versus [0.27, 1.76] pps). At 50% MVC, the interval for the HD-sEMG-mode difference ([−0.80, 0.22] pps) was compatible both with a reduction of approximately 0.8 pps and with no difference. The absence of statistical significance at this force level therefore reflects limited resolution and should not be interpreted as evidence that the selection effect was absent.

[P00106 | 31040:31041 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00107 | 31041:31054 | HEADING_1]
4 Discussion

[P00108 | 31054:32414 | NORMAL_TEXT]
We investigated whether the lower motor-unit (MU) discharge rates previously reported in patients with diabetic peripheral neuropathy (DPN) during matched relative-force contractions could arise from selection biases associated with high-density surface electromyography (HD-sEMG) decomposition. The prespecified primary comparison at 20% MVC supported this possibility. Under HD-sEMG-like selection, mean MU firing rate was lower in the DPN condition than in the Normal condition (8.04 ± 0.62 vs. 9.14 ± 0.45 pps; paired difference, −1.10 pps; p < 0.001), consistent with previous experimental reports (Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Valli et al. 2025). By contrast, unrestricted random sampling of 10 active MUs yielded a higher mean firing rate in DPN (14.06 ± 1.83 vs. 13.05 ± 1.99 pps; paired difference, 1.01 pps; p = 0.024). The full-population simulation truth was likewise higher in DPN (14.04 ± 0.40 vs. 13.00 ± 0.27 pps; paired difference, 1.03 pps; p < 0.001). The results therefore supported the selection-bias component of our hypothesis, but not the specific prediction that removing the selection criteria would eliminate the between-condition difference. Instead, the HD-sEMG-like selection procedure reversed, rather than merely attenuated, the direction of the underlying difference in the model.

[P00109 | 32414:33686 | NORMAL_TEXT]
Discharge regularity has been central to MU identification since the development of surface-EMG decomposition methods (Holobar and Zazula 2007a, 2007b). Criteria intended to ensure reliable decomposition cannot simply be removed from experimental analyses, because doing so may compromise identification accuracy. Surface recordings may also favor MUs that generate larger detectable potentials, while superimposition can impede identification of MUs discharging at higher rates (Caillet et al. 2022; Negro et al. 2016). Although recent algorithms seek to identify a broader range of MUs (Grison et al. 2025; Jiang et al. 2025), the representativeness of the identified sample remains important when groups differ in MU discharge behavior. The present model did not generate raw surface EMG or apply a decomposition algorithm. Instead, it operationalized selected features of HD-sEMG identification by restricting eligible MUs to firing rates between 5 and 15 pps and an interspike interval coefficient of variation (ISI-CoV) of 0.3 or less, followed by selection of the 10 eligible MUs with the lowest firing rates. The findings therefore concern the consequences of this HD-sEMG-like selection rule rather than the performance of any particular decomposition algorithm.

[P00110 | 33686:35216 | NORMAL_TEXT]
The eligibility-restricted random-sampling analysis clarified how the modeled selection procedure produced the primary result. When 10 MUs were sampled randomly from the eligible subset, without preferentially selecting those with the lowest firing rates, mean firing rate remained lower in DPN (11.71 ± 0.72 vs. 12.20 ± 0.50 pps; paired difference, −0.48 pps; p < 0.001). The joint firing-rate and ISI-CoV eligibility criteria were therefore sufficient to reverse the direction observed under unrestricted random sampling and in the full-population reference, whereas preferential selection of the lowest-firing eligible MUs increased the magnitude of the difference to −1.10 pps. Varying the eligibility thresholds isolated these contributions. The ISI-CoV criterion determined the direction of the effect, lowest-rate prioritization approximately doubled its magnitude, and the upper firing-rate bound contributed nothing under this selection rule. The direction was preserved across the range of ISI-CoV thresholds commonly applied in experimental studies but not at substantially more permissive thresholds, indicating that the bias depends on the reliability criterion being restrictive enough to sample a distinct portion of the MU population. Similarly, because the model did not include a spatial or motor-unit-action-potential-amplitude detection stage, the findings show that explicit size-based detection was not required to reproduce the apparent reduction; they do not establish that motor-unit size is unimportant.

[P00111 | 35216:36225 | NORMAL_TEXT]
The ISI-CoV findings provide additional context for this selection mechanism. Within the HD-sEMG-like samples, the simulation-level mean ISI-CoV was modestly but significantly lower in DPN than in the Normal condition (0.225 ± 0.021 vs. 0.245 ± 0.015; p < 0.001). At the descriptive MU level, Figure 4 shows the joint distribution of firing rate and ISI-CoV, while Figure 6 shows that the pooled proportion of MUs below the ISI-CoV eligibility threshold was greater in DPN than in the Normal condition (85.8% vs. 76.9%). Together, these descriptive distributions indicate that the same eligibility rule operated on differently shaped MU populations in the two simulated conditions, thereby admitting different subsets of MUs. However, because the MU-level observations in Figures 3 and 5 were pooled for descriptive purposes, these figures do not provide independent subject-level evidence that DPN reduces ISI-CoV at a given firing rate, nor do they isolate ISI-CoV as the cause of the firing-rate reversal.

[P00112 | 36225:37718 | NORMAL_TEXT]
The higher full-population firing rate in DPN, together with the smaller number of active MUs, is physiologically plausible within the model and, in our view, most likely reflects compensation for the reduced force-generating capacity assigned to DPN MUs. Their twitch-force parameters were reduced by a factor of 1.4 while the feedback controller was required to maintain the same relative target force, so greater neural drive was needed to sustain that force. In the model, this compensation was achieved through rate coding rather than recruitment: the DPN condition sustained the target force with fewer active MUs discharging at higher rates. The concurrent prolongation of twitch time to peak may explain why this route was favored, because longer twitches fuse more effectively at a given discharge rate and therefore yield more force per additional impulse than recruiting further units would. This pattern is also consistent with experimental reports that lower discharge rates in DPN are not accompanied by an increase in the number of identified MUs. Because several DPN-related parameters were altered concurrently and no parameter-ablation analysis was performed, the precise contribution of reduced MU force capacity cannot be isolated from the other modeled alterations; nevertheless, the direct relationship between reduced force per MU and the neural drive required to sustain the target force makes compensation the most likely explanation for both full-population results.

[P00113 | 37718:39361 | NORMAL_TEXT]
The supplementary analyses extended the comparison to 10% and 50% MVC. The HD-sEMG-like estimate remained lower in DPN at both force levels, whereas the full-population reference remained higher in DPN. At 10% MVC, the HD-sEMG-like difference was statistically significant (−1.10 pps; p = 0.004); at 50% MVC, the estimated difference was smaller and not statistically significant (−0.34 pps; 95% CI [−0.80, 0.22]; p = 0.232). Moreover, unrestricted random sampling did not yield a statistically significant between-condition difference at either supplementary force level. These exploratory analyses therefore demonstrate qualitative consistency in the direction of the HD-sEMG-like estimates, but with 10 paired simulated subjects per force level they had limited precision, and the resulting intervals were correspondingly wide. At 50% MVC, the interval estimate spanned values ranging from a reduction of approximately 0.8 pps to a small increase, so the absence of statistical significance indicates insufficient resolution rather than evidence that the selection effect disappears at higher contraction intensities. At the same time, the point estimate at 50% MVC was smaller than at 20% MVC and its interval excluded the difference observed at that level, so genuine attenuation of the selection effect at higher forces also remains plausible. These analyses were not designed to compare effect magnitudes across force levels, and distinguishing attenuation from limited precision would require a larger number of paired simulated subjects at each level, together with a formal test of the interaction between force level and condition.

[P00114 | 39361:40672 | NORMAL_TEXT]
Computational models cannot reproduce the full biological and measurement complexity of the human neuromuscular system, but they provide a platform for testing hypotheses that are difficult to isolate experimentally (Farina and Negro 2015; R. N. Watanabe and Kohn 2015). The present findings do not constitute direct empirical evidence that the complete MU population in patients with DPN has normal or increased firing rates. We did not collect patient data, generate raw EMG, or process signals with an actual decomposition algorithm. The model also lacked a volume conductor, electrode geometry, MU action-potential amplitudes, and an explicit spatial detection stage. Muscle–tendon dynamics and afferent feedback from muscle spindles and Golgi tendon organs were not included, and some pathological parameter changes were estimated because precise quantitative human data were unavailable. In addition, several DPN-related parameters were varied together, preventing attribution of the results to any single alteration. Future work should incorporate spatially realistic EMG generation and decomposition, evaluate the selection rule against experimental data, and use parameter-ablation analyses to determine which physiological and measurement factors contribute most strongly to the observed differences.

[P00115 | 40672:41576 | NORMAL_TEXT]
In summary, applying an HD-sEMG-like selection rule to the simulated MU populations produced a lower mean firing rate in DPN even though unrestricted sampling and the full-population reference showed the opposite direction at the primary force level. This proof-of-concept does not demonstrate that previously reported reductions in DPN are entirely methodological artifacts. It shows, however, that a lower firing rate in an HD-sEMG-decomposed sample need not represent a reduction across the complete active-MU population. Comparisons between Normal and DPN groups should therefore consider whether pathological changes in MU discharge distributions alter which units satisfy identification and reliability criteria. Experimental validation and decomposition methods that are less sensitive to such distributional differences will be necessary to determine the extent of this bias in human recordings.

[P00116 | 41576:41577 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00117 | 41577:41586 | HEADING_1]
Appendix

[P00118 | 41586:41610 | HEADING_2]
The computational model

[P00119 | 41610:41986 | NORMAL_TEXT]
The model comprises a pool of 250 motoneurons, each represented by coupled somatic and dendritic compartments. Motoneuron parameters were taken from an earlier model (R. N. Watanabe et al. 2013; R. N. Watanabe and Kohn 2015) and varied exponentially between the minimum and maximum values across the pool. Symbols and parameter values relevant to this study are listed below.

[P00120 | 41986:41987 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00121 | 41987:42129 | NORMAL_TEXT]
Table 2. Symbols, variables, and parameter values used in the computational model. Condition-specific values are identified where applicable.

[P00122 | 42129:42130 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00123 | 42133:42140 | NORMAL_TEXT | TABLE row=0 col=0]
Symbol

[P00124 | 42141:42153 | NORMAL_TEXT | TABLE row=0 col=1]
Description

[P00125 | 42154:42159 | NORMAL_TEXT | TABLE row=0 col=2]
Unit

[P00126 | 42160:42175 | NORMAL_TEXT | TABLE row=0 col=3]
Value or range

[P00127 | 42177:42179 | NORMAL_TEXT | TABLE row=1 col=0]
C

[P00128 | 42180:42210 | NORMAL_TEXT | TABLE row=1 col=1]
Specific membrane capacitance

[P00129 | 42211:42218 | NORMAL_TEXT | TABLE row=1 col=2]
µF/cm²

[P00130 | 42219:42221 | NORMAL_TEXT | TABLE row=1 col=3]
1

[P00131 | 42223:42226 | NORMAL_TEXT | TABLE row=2 col=0]
Rₐ

[P00132 | 42227:42245 | NORMAL_TEXT | TABLE row=2 col=1]
Axial resistivity

[P00133 | 42246:42250 | NORMAL_TEXT | TABLE row=2 col=2]
Ω·m

[P00134 | 42251:42256 | NORMAL_TEXT | TABLE row=2 col=3]
0.07

[P00135 | 42258:42263 | NORMAL_TEXT | TABLE row=3 col=0]
NCST

[P00136 | 42264:42301 | NORMAL_TEXT | TABLE row=3 col=1]
Number of descending-command neurons

[P00137 | 42302:42304 | NORMAL_TEXT | TABLE row=3 col=2]
-

[P00138 | 42305:42329 | NORMAL_TEXT | TABLE row=3 col=3]
400 (Normal); 200 (DPN)

[P00139 | 42331:42335 | NORMAL_TEXT | TABLE row=4 col=0]
NMU

[P00140 | 42336:42358 | NORMAL_TEXT | TABLE row=4 col=1]
Number of motor units

[P00141 | 42359:42361 | NORMAL_TEXT | TABLE row=4 col=2]
-

[P00142 | 42362:42366 | NORMAL_TEXT | TABLE row=4 col=3]
250

[P00143 | 42368:42370 | NORMAL_TEXT | TABLE row=5 col=0]
A

[P00144 | 42371:42399 | NORMAL_TEXT | TABLE row=5 col=1]
Motor-unit twitch amplitude

[P00145 | 42400:42402 | NORMAL_TEXT | TABLE row=5 col=2]
N

[P00146 | 42403:42438 | NORMAL_TEXT | TABLE row=5 col=3]
0.04–4 (Normal); 0.0286–2.86 (DPN)

[P00147 | 42440:42443 | NORMAL_TEXT | TABLE row=6 col=0]
Tc

[P00148 | 42444:42508 | NORMAL_TEXT | TABLE row=6 col=1]
Motor-unit twitch time to peak (smallest to largest motor unit)

[P00149 | 42509:42512 | NORMAL_TEXT | TABLE row=6 col=2]
ms

[P00150 | 42513:42543 | NORMAL_TEXT | TABLE row=6 col=3]
110–25 (Normal); 154–35 (DPN)

[P00151 | 42545:42549 | NORMAL_TEXT | TABLE row=7 col=0]
ENa

[P00152 | 42550:42576 | NORMAL_TEXT | TABLE row=7 col=1]
Sodium reversal potential

[P00153 | 42577:42580 | NORMAL_TEXT | TABLE row=7 col=2]
mV

[P00154 | 42581:42584 | NORMAL_TEXT | TABLE row=7 col=3]
50

[P00155 | 42586:42590 | NORMAL_TEXT | TABLE row=8 col=0]
EKs

[P00156 | 42591:42625 | NORMAL_TEXT | TABLE row=8 col=1]
Slow-potassium reversal potential

[P00157 | 42626:42629 | NORMAL_TEXT | TABLE row=8 col=2]
mV

[P00158 | 42630:42634 | NORMAL_TEXT | TABLE row=8 col=3]
-80

[P00159 | 42636:42640 | NORMAL_TEXT | TABLE row=9 col=0]
EKf

[P00160 | 42641:42675 | NORMAL_TEXT | TABLE row=9 col=1]
Fast-potassium reversal potential

[P00161 | 42676:42679 | NORMAL_TEXT | TABLE row=9 col=2]
mV

[P00162 | 42680:42684 | NORMAL_TEXT | TABLE row=9 col=3]
-80

[P00163 | 42686:42689 | NORMAL_TEXT | TABLE row=10 col=0]
Kp

[P00164 | 42690:42732 | NORMAL_TEXT | TABLE row=10 col=1]
Proportional gain of the force controller

[P00165 | 42733:42739 | NORMAL_TEXT | TABLE row=10 col=2]
pps/N

[P00166 | 42740:42745 | NORMAL_TEXT | TABLE row=10 col=3]
0.05

[P00167 | 42747:42750 | NORMAL_TEXT | TABLE row=11 col=0]
Ki

[P00168 | 42751:42789 | NORMAL_TEXT | TABLE row=11 col=1]
Integral gain of the force controller

[P00169 | 42790:42800 | NORMAL_TEXT | TABLE row=11 col=2]
pps/(N·s)

[P00170 | 42801:42807 | NORMAL_TEXT | TABLE row=11 col=3]
0.005

[P00171 | 42809:42813 | NORMAL_TEXT | TABLE row=12 col=0]
CaT

[P00172 | 42814:42851 | NORMAL_TEXT | TABLE row=12 col=1]
Calcium-bound troponin concentration

[P00173 | 42852:42854 | NORMAL_TEXT | TABLE row=12 col=2]
M

[P00174 | 42855:42857 | NORMAL_TEXT | TABLE row=12 col=3]
-

[P00175 | 42859:42861 | NORMAL_TEXT | TABLE row=13 col=0]
F

[P00176 | 42862:42879 | NORMAL_TEXT | TABLE row=13 col=1]
Motor-unit force

[P00177 | 42880:42882 | NORMAL_TEXT | TABLE row=13 col=2]
N

[P00178 | 42883:42885 | NORMAL_TEXT | TABLE row=13 col=3]
-

[P00179 | 42887:42889 | NORMAL_TEXT | TABLE row=14 col=0]
v

[P00180 | 42890:42922 | NORMAL_TEXT | TABLE row=14 col=1]
Motor-nerve conduction velocity

[P00181 | 42923:42927 | NORMAL_TEXT | TABLE row=14 col=2]
m/s

[P00182 | 42928:42961 | NORMAL_TEXT | TABLE row=14 col=3]
44–53 (Normal); 37.4–45.05 (DPN)

[P00183 | 42963:42965 | NORMAL_TEXT | TABLE row=15 col=0]
n

[P00184 | 42966:43013 | NORMAL_TEXT | TABLE row=15 col=1]
Activation state of the fast potassium channel

[P00185 | 43014:43016 | NORMAL_TEXT | TABLE row=15 col=2]
-

[P00186 | 43017:43019 | NORMAL_TEXT | TABLE row=15 col=3]
-

[P00187 | 43021:43023 | NORMAL_TEXT | TABLE row=16 col=0]
m

[P00188 | 43024:43063 | NORMAL_TEXT | TABLE row=16 col=1]
Activation state of the sodium channel

[P00189 | 43064:43066 | NORMAL_TEXT | TABLE row=16 col=2]
-

[P00190 | 43067:43069 | NORMAL_TEXT | TABLE row=16 col=3]
-

[P00191 | 43071:43073 | NORMAL_TEXT | TABLE row=17 col=0]
h

[P00192 | 43074:43115 | NORMAL_TEXT | TABLE row=17 col=1]
Inactivation state of the sodium channel

[P00193 | 43116:43118 | NORMAL_TEXT | TABLE row=17 col=2]
-

[P00194 | 43119:43121 | NORMAL_TEXT | TABLE row=17 col=3]
-

[P00195 | 43123:43125 | NORMAL_TEXT | TABLE row=18 col=0]
p

[P00196 | 43126:43173 | NORMAL_TEXT | TABLE row=18 col=1]
Activation state of the slow potassium channel

[P00197 | 43174:43176 | NORMAL_TEXT | TABLE row=18 col=2]
-

[P00198 | 43177:43179 | NORMAL_TEXT | TABLE row=18 col=3]
-

[P00199 | 43181:43184 | NORMAL_TEXT | TABLE row=19 col=0]
Vs

[P00200 | 43185:43209 | NORMAL_TEXT | TABLE row=19 col=1]
Soma membrane potential

[P00201 | 43210:43213 | NORMAL_TEXT | TABLE row=19 col=2]
mV

[P00202 | 43214:43216 | NORMAL_TEXT | TABLE row=19 col=3]
-

[P00203 | 43218:43221 | NORMAL_TEXT | TABLE row=20 col=0]
Vd

[P00204 | 43222:43250 | NORMAL_TEXT | TABLE row=20 col=1]
Dendrite membrane potential

[P00205 | 43251:43254 | NORMAL_TEXT | TABLE row=20 col=2]
mV

[P00206 | 43255:43257 | NORMAL_TEXT | TABLE row=20 col=3]
-

[P00207 | 43259:43262 | NORMAL_TEXT | TABLE row=21 col=0]
Cs

[P00208 | 43263:43289 | NORMAL_TEXT | TABLE row=21 col=1]
Soma membrane capacitance

[P00209 | 43290:43293 | NORMAL_TEXT | TABLE row=21 col=2]
µF

[P00210 | 43294:43296 | NORMAL_TEXT | TABLE row=21 col=3]
-

[P00211 | 43298:43301 | NORMAL_TEXT | TABLE row=22 col=0]
Cd

[P00212 | 43302:43332 | NORMAL_TEXT | TABLE row=22 col=1]
Dendrite membrane capacitance

[P00213 | 43333:43336 | NORMAL_TEXT | TABLE row=22 col=2]
µF

[P00214 | 43337:43339 | NORMAL_TEXT | TABLE row=22 col=3]
-

[P00215 | 43341:43346 | NORMAL_TEXT | TABLE row=23 col=0]
gL,s

[P00216 | 43347:43380 | NORMAL_TEXT | TABLE row=23 col=1]
Conductance of the soma membrane

[P00217 | 43381:43384 | NORMAL_TEXT | TABLE row=23 col=2]
mS

[P00218 | 43385:43387 | NORMAL_TEXT | TABLE row=23 col=3]
-

[P00219 | 43389:43394 | NORMAL_TEXT | TABLE row=24 col=0]
gL,d

[P00220 | 43395:43432 | NORMAL_TEXT | TABLE row=24 col=1]
Conductance of the dendrite membrane

[P00221 | 43433:43436 | NORMAL_TEXT | TABLE row=24 col=2]
mS

[P00222 | 43437:43439 | NORMAL_TEXT | TABLE row=24 col=3]
-

[P00223 | 43441:43445 | NORMAL_TEXT | TABLE row=25 col=0]
gNa

[P00224 | 43446:43465 | NORMAL_TEXT | TABLE row=25 col=1]
Sodium conductance

[P00225 | 43466:43473 | NORMAL_TEXT | TABLE row=25 col=2]
mS/cm²

[P00226 | 43474:43477 | NORMAL_TEXT | TABLE row=25 col=3]
30

[P00227 | 43479:43483 | NORMAL_TEXT | TABLE row=26 col=0]
gKf

[P00228 | 43484:43511 | NORMAL_TEXT | TABLE row=26 col=1]
Fast-potassium conductance

[P00229 | 43512:43519 | NORMAL_TEXT | TABLE row=26 col=2]
mS/cm²

[P00230 | 43520:43525 | NORMAL_TEXT | TABLE row=26 col=3]
2.25

[P00231 | 43527:43531 | NORMAL_TEXT | TABLE row=27 col=0]
gKs

[P00232 | 43532:43559 | NORMAL_TEXT | TABLE row=27 col=1]
Slow-potassium conductance

[P00233 | 43560:43567 | NORMAL_TEXT | TABLE row=27 col=2]
mS/cm²

[P00234 | 43568:43572 | NORMAL_TEXT | TABLE row=27 col=3]
0.1

[P00235 | 43573:43574 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00236 | 43574:43870 | NORMAL_TEXT]
The somatic compartment of each motoneuron includes sodium, slow-potassium, and fast-potassium channels represented with Hodgkin–Huxley-type kinetics (Hodgkin and Huxley 1952; Destexhe and Paré 1999; Cisi and Kohn 2008). The somatic and dendritic membrane potentials, Vs and Vd, are governed by:

[P00237 | 43870:43932 | NORMAL_TEXT]
dVs/dt = −{gL,s[Vs(t) − EL] + gc[Vs(t) − Vd(t)] + Iion(t)}/Cs

[P00238 | 43932:43994 | NORMAL_TEXT]
dVd/dt = −{gL,d[Vd(t) − EL] + gc[Vd(t) − Vs(t)] + Isyn(t)}/Cd

[P00239 | 43994:44300 | NORMAL_TEXT]
Here, Cs and Cd are the somatic and dendritic membrane capacitances; gL,s and gL,d are their leak conductances; and gc is the coupling conductance. Their values match those used by R. N. Watanabe and Kohn (2015). The somatic ionic current is the sum of sodium, fast-potassium, and slow-potassium currents:

[P00240 | 44300:44387 | NORMAL_TEXT]
Iion(t) = gNa m³(t)h(t)[Vs(t) − ENa] + gKf n⁴(t)[Vs(t) − EKf] + gKs p²(t)[Vs(t) − EKs]

[P00241 | 44387:44494 | NORMAL_TEXT]
The gating variables m, h, and n follow Hodgkin–Huxley-type first-order kinetics (Destexhe and Paré 1999):

[P00242 | 44494:44550 | NORMAL_TEXT]
dx/dt = αx(Vs)[1 − x(t)] − βx(Vs)x(t),    x ∈ {m, h, n}

[P00243 | 44550:44592 | NORMAL_TEXT]
The voltage-dependent rate functions are:

[P00244 | 44592:44710 | NORMAL_TEXT]
αm(Vs) = −0.32(Vs − vt − 13)/{exp[−(Vs − vt − 13)/4] − 1},    βm(Vs) = 0.28(Vs − vt − 40)/{exp[(Vs − vt − 40)/5] − 1}

[P00245 | 44710:44798 | NORMAL_TEXT]
αh(Vs) = 0.00512 exp[−(Vs − vt − 17)/18],    βh(Vs) = 0.16/{1 + exp[−(Vs − vt − 40)/5]}

[P00246 | 44798:44901 | NORMAL_TEXT]
αn(Vs) = −0.00128(Vs − vt − 15)/{exp[−(Vs − vt − 15)/5] − 1},    βn(Vs) = 0.02 exp[−(Vs − vt − 10)/40]

[P00247 | 44901:44976 | NORMAL_TEXT]
The slow-potassium activation variable p follows Nussbaumer et al. (2002):

[P00248 | 44976:45007 | NORMAL_TEXT]
dp/dt = [p∞(Vs) − p(t)]/τp(Vs)

[P00249 | 45007:45013 | NORMAL_TEXT]
where

[P00250 | 45013:45109 | NORMAL_TEXT]
p∞(Vs) = 1/{1 + exp[−(Vs + 35)/10]},    τp(Vs) = 4/{3.3 exp[(Vs + 35)/20] + exp[−(Vs + 35)/20]}

[P00251 | 45109:45252 | NORMAL_TEXT]
Here, vt is the motoneuron firing threshold and has the value used by R. N. Watanabe and Kohn (2015); Vs(t) is the somatic membrane potential.

[P00252 | 45252:45707 | NORMAL_TEXT]
Each motor unit’s calcium dynamics follow the model developed by Kim and Heckman (2023), including sarcoplasmic calcium, calcium–calsequestrin reactions within the sarcoplasmic reticulum, calcium release and uptake, cytosolic calcium buffering, calcium–troponin binding, and the resulting activation. Motor-unit force was generated from the calcium-dynamics output with a second-order linear model (Fuglevand, Winter, and Patla 1993; Cisi and Kohn 2008):

[P00253 | 45707:45776 | NORMAL_TEXT]
d²Fi/dt² = −(2/Tc,i)(dFi/dt) − Fi(t)/Tc,i² + (Ai/Tc,i)[CaTi(t)/CaT0]

[P00254 | 45776:46023 | NORMAL_TEXT]
Here, Fi(t) is the force produced by motor unit i, Tc,i is its twitch time to peak, Ai is its maximum twitch amplitude, CaTi(t) is its calcium-bound troponin concentration, and CaT0 = 0.0001 M is the normalization concentration used by the model.

[P00255 | 46023:46298 | NORMAL_TEXT]
The descending command comprises NCST independent neurons (Figure 1; R. N. Watanabe et al. 2013). Each descending-command neuron connects randomly to approximately 10% of the motoneurons, and only excitatory synapses were used. Each synapse generates a current according to:

[P00256 | 46298:46330 | NORMAL_TEXT]
Isyn(t) = gsyn(t)[Vd(t) − Esyn]

[P00257 | 46330:46498 | NORMAL_TEXT]
The synaptic conductance gsyn(t) decays exponentially with a time constant τsyn = 0.6 ms; each incoming spike increases it by 600 nS, and the synaptic delay is 0.2 ms.

[P00258 | 46498:46829 | NORMAL_TEXT]
The mean discharge rate of each gamma-distributed descending-command process was modulated by a proportional–integral force controller (Figure 1), with Kp = 0.05 pps/N and Ki = 0.005 pps/(N·s). A 60-ms delay was included in the force-feedback loop to represent the visual feedback typically provided during isometric contractions.

[P00259 | 46829:46830 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00260 | 46830:46843 | HEADING_1]
5 References

[P00261 | 46843:47151 | NORMAL_TEXT]
[Allen, Matti D., Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Length Dependent Loss of Motor Axons and Altered Motor Unit Properties in Human Diabetic Polyneuropathy.”](http://paperpile.com/b/ku2MlM/PRcA)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/PRcA)[125 (4): 836–43.](http://paperpile.com/b/ku2MlM/PRcA)

[P00262 | 47151:47428 | NORMAL_TEXT]
[Allen, Matti D., Brendan Major, Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Skeletal Muscle Morphology and Contractile Function in Relation to Muscle Denervation in Diabetic Neuropathy.”](http://paperpile.com/b/ku2MlM/jR7N)[Journal of Applied Physiology (Bethesda, Md. : 1985)](http://paperpile.com/b/ku2MlM/jR7N)[116 (5): 545–52.](http://paperpile.com/b/ku2MlM/jR7N)

[P00263 | 47428:47842 | NORMAL_TEXT]
[Allen, Matti D., Daniel W. Stashuk, Kurt Kimpinski, Timothy J. Doherty, Maddison L. Hourigan, and Charles L. Rice. 2015. “Increased Neuromuscular Transmission Instability and Motor Unit Remodelling with Diabetic Neuropathy as Assessed Using Novel near Fibre Motor Unit Potential Parameters.”](http://paperpile.com/b/ku2MlM/LtlU)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/LtlU)[126 (4): 794–802.](http://paperpile.com/b/ku2MlM/LtlU)

[P00264 | 47842:48079 | NORMAL_TEXT]
[Almeida, S., M. C. Riddell, and E. Cafarelli. 2008. “Slower Conduction Velocity and Motor Unit Discharge Frequency Are Associated with Muscle Fatigue during Isometric Exercise in Type 1 Diabetes Mellitus.”](http://paperpile.com/b/ku2MlM/V9si)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/V9si)[37 (2): 231–40.](http://paperpile.com/b/ku2MlM/V9si)

[P00265 | 48079:48401 | NORMAL_TEXT]
[Aye, Tandy, Naama Barnea-Goraly, Christian Ambler, Sherry Hoang, Kristin Schleifer, Yaena Park, Jessica Drobny, Darrell M. Wilson, Allan L. Reiss, and Bruce A. Buckingham. 2012. “White Matter Structural Differences in Young Children with Type 1 Diabetes: A Diffusion Tensor Imaging Study.”](http://paperpile.com/b/ku2MlM/1pPD)[Diabetes Care](http://paperpile.com/b/ku2MlM/1pPD)[35 (11): 2167–73.](http://paperpile.com/b/ku2MlM/1pPD)

[P00266 | 48401:48683 | NORMAL_TEXT]
[Caillet, Arnault H., Andrew T. M. Phillips, Dario Farina, and Luca Modenese. 2022. “Estimation of the Firing Behaviour of a Complete Motoneuron Pool by Combining Electromyography Signal Decomposition and Realistic Motoneuron Modelling.”](http://paperpile.com/b/ku2MlM/p4VN)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/p4VN)[18 (9): e1010556.](http://paperpile.com/b/ku2MlM/p4VN)

[P00267 | 48683:48895 | NORMAL_TEXT]
[Cisi, Rogerio R. L., and André F. Kohn. 2008. “Simulation System of Spinal Cord Motor Nuclei and Associated Nerves and Muscles, in a Web-Based Architecture.”](http://paperpile.com/b/ku2MlM/8qUP)[Journal of Computational Neuroscience](http://paperpile.com/b/ku2MlM/8qUP)[25 (3): 520–42.](http://paperpile.com/b/ku2MlM/8qUP)

[P00268 | 48895:49128 | NORMAL_TEXT]
[Davison, Andrew P., Daniel Brüderle, Jochen Eppler, Jens Kremkow, Eilif Muller, Dejan Pecevski, Laurent Perrinet, and Pierre Yger. 2008. “PyNN: A Common Interface for Neuronal Network Simulators.”](http://paperpile.com/b/ku2MlM/9z19)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/9z19)[2:11.](http://paperpile.com/b/ku2MlM/9z19)

[P00269 | 49128:49306 | NORMAL_TEXT]
[Destexhe, A., and D. Paré. 1999. “Impact of Network Activity on the Integrative Properties of Neocortical Pyramidal Neurons in Vivo.”](http://paperpile.com/b/ku2MlM/ap2G)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/ap2G)[81 (4): 1531–47.](http://paperpile.com/b/ku2MlM/ap2G)

[P00270 | 49306:49449 | NORMAL_TEXT]
[Enoka, Roger M., and Dario Farina. 2021. “Force Steadiness: From Motor Units to Voluntary Actions.”](http://paperpile.com/b/ku2MlM/GtoK)[Physiology (Bethesda, Md.)](http://paperpile.com/b/ku2MlM/GtoK)[36 (2): 114–30.](http://paperpile.com/b/ku2MlM/GtoK)

[P00271 | 49449:49592 | NORMAL_TEXT]
[Eshima, Hiroaki, David C. Poole, and Yutaka Kano. 2014. “In Vivo Calcium Regulation in Diabetic Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/zhBj)[Cell Calcium](http://paperpile.com/b/ku2MlM/zhBj)[56 (5): 381–89.](http://paperpile.com/b/ku2MlM/zhBj)

[P00272 | 49592:49795 | NORMAL_TEXT]
[Farina, Dario, and Ales Holobar. 2016. “Characterization of Human Motor Units from Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/jbAP)[Proceedings of the IEEE. Institute of Electrical and Electronics Engineers](http://paperpile.com/b/ku2MlM/jbAP)[104 (2): 353–73.](http://paperpile.com/b/ku2MlM/jbAP)

[P00273 | 49795:49977 | NORMAL_TEXT]
[Farina, Dario, and Francesco Negro. 2015. “Common Synaptic Input to Motor Neurons, Motor Unit Synchronization, and Force Control.”](http://paperpile.com/b/ku2MlM/4xcD)[Exercise and Sport Sciences Reviews](http://paperpile.com/b/ku2MlM/4xcD)[43 (1): 23–33.](http://paperpile.com/b/ku2MlM/4xcD)

[P00274 | 49977:50417 | NORMAL_TEXT]
[Favretto, Mateus André, Felipe Rettore Andreis, Sandra Cossul, Francesco Negro, Anderson Souza Oliveira, and Jefferson Luiz Brum Marques. 2023. “Differences in Motor Unit Behavior during Isometric Contractions in Patients with Diabetic Peripheral Neuropathy at Various Disease Severities.”](http://paperpile.com/b/ku2MlM/5qJ6)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/5qJ6)[68 (February):102725.](http://paperpile.com/b/ku2MlM/5qJ6)

[P00275 | 50417:50590 | NORMAL_TEXT]
[Fuglevand, A. J., D. A. Winter, and A. E. Patla. 1993. “Models of Recruitment and Rate Coding Organization in Motor-Unit Pools.”](http://paperpile.com/b/ku2MlM/tjpv)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/tjpv)[70 (6): 2470–88.](http://paperpile.com/b/ku2MlM/tjpv)

[P00276 | 50590:50868 | NORMAL_TEXT]
[Grison, Agnese, Irene Mendez Guerra, Alexander Kenneth Clarke, Silvia Muceli, Jaime Ibáñez, and Dario Farina. 2025. “Unlocking the Full Potential of High-Density Surface EMG: Novel Non-Invasive High-Yield Motor Unit Decomposition.”](http://paperpile.com/b/ku2MlM/QyGL)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/QyGL)[603 (8): 2281–2300.](http://paperpile.com/b/ku2MlM/QyGL)

[P00277 | 50868:51064 | NORMAL_TEXT]
[Harris, Charles R., K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, et al. 2020. “Array Programming with NumPy.”](http://paperpile.com/b/ku2MlM/HVd0)[Nature](http://paperpile.com/b/ku2MlM/HVd0)[585 (7825): 357–62.](http://paperpile.com/b/ku2MlM/HVd0)

[P00278 | 51064:51219 | NORMAL_TEXT]
[Hines, Michael L. 1993.](http://paperpile.com/b/ku2MlM/Vcj2)[“NEURON — A Program for Simulation of Nerve Equations.” In](http://paperpile.com/b/ku2MlM/Vcj2)[Neural Systems: Analysis and Modeling](http://paperpile.com/b/ku2MlM/Vcj2)[, 127–36. Boston, MA: Springer US.](http://paperpile.com/b/ku2MlM/Vcj2)

[P00279 | 51219:51347 | NORMAL_TEXT]
[Hines, Michael L., Andrew P. Davison, and Eilif Muller. 2009. “NEURON and Python.”](http://paperpile.com/b/ku2MlM/jjzD)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/jjzD)[3 (January):1.](http://paperpile.com/b/ku2MlM/jjzD)

[P00280 | 51347:51539 | NORMAL_TEXT]
[Hodgkin, A. L., and A. F. Huxley. 1952. “A Quantitative Description of Membrane Current and Its Application to Conduction and Excitation in Nerve.”](http://paperpile.com/b/ku2MlM/nbxX)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/nbxX)[117 (4): 500–544.](http://paperpile.com/b/ku2MlM/nbxX)

[P00281 | 51539:51772 | NORMAL_TEXT]
[Holobar, Aleš, and Damjan Zazula. 2007a.](http://paperpile.com/b/ku2MlM/C6Et)[“Gradient Convolution Kernel Compensation Applied to Surface Electromyograms.” In](http://paperpile.com/b/ku2MlM/C6Et)[Independent Component Analysis and Signal Separation](http://paperpile.com/b/ku2MlM/C6Et)[, 617–24. Berlin, Heidelberg: Springer Berlin Heidelberg.](http://paperpile.com/b/ku2MlM/C6Et)

[P00282 | 51772:52000 | NORMAL_TEXT]
[Holobar, Aleš, and Damjan Zazula. 2007b. “Multichannel Blind Source Separation](http://paperpile.com/b/ku2MlM/nHk7)[Using Convolution Kernel Compensation.”](http://paperpile.com/b/ku2MlM/nHk7)[IEEE Transactions on Signal Processing: A Publication of the IEEE Signal Processing Society](http://paperpile.com/b/ku2MlM/nHk7)[55 (9): 4487–96.](http://paperpile.com/b/ku2MlM/nHk7)

[P00283 | 52000:52112 | NORMAL_TEXT]
[Hunter, John D. 2007. “Matplotlib: A 2D Graphics Environment.”](http://paperpile.com/b/ku2MlM/SRer)[Computing in Science & Engineering](http://paperpile.com/b/ku2MlM/SRer)[9 (3): 90–95.](http://paperpile.com/b/ku2MlM/SRer)

[P00284 | 52112:52342 | NORMAL_TEXT]
[Jiang, Xi, Weiyu Guo, Ziwei Cui, Chuang Lin, and Jingyong Su. 2025. “Decomposition of High-Density sEMG Signals: Extracting Multiple Spikes from Single Time Windows.”](http://paperpile.com/b/ku2MlM/K78i)[Biomedical Signal Processing and Control](http://paperpile.com/b/ku2MlM/K78i)[107 (107771): 107771.](http://paperpile.com/b/ku2MlM/K78i)

[P00285 | 52342:52518 | NORMAL_TEXT]
[Kim, Hojeong, and Charles J. Heckman. 2023. “A Dynamic Calcium-Force Relationship Model for Sag Behavior in Fast Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/ueNw)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/ueNw)[19 (6): e1011178.](http://paperpile.com/b/ku2MlM/ueNw)

[P00286 | 52518:52713 | NORMAL_TEXT]
[Klueber, K. M., and J. D. Feczko. 1994. “Ultrastructural, Histochemical, and Morphometric Analysis of Skeletal Muscle in a Murine Model of Type I Diabetes.”](http://paperpile.com/b/ku2MlM/2p6W)[The Anatomical Record](http://paperpile.com/b/ku2MlM/2p6W)[239 (1): 18–34.](http://paperpile.com/b/ku2MlM/2p6W)

[P00287 | 52713:52990 | NORMAL_TEXT]
[Li, Xiaoyan, Ales Holobar, Marco Gazzoni, Roberto Merletti, William Zev Rymer, and Ping Zhou. 2015. “Examination of Poststroke Alteration in Motor Unit Firing Behavior Using High-Density Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/py9H)[IEEE Transactions on Bio-Medical Engineering](http://paperpile.com/b/ku2MlM/py9H)[62 (5): 1242–52.](http://paperpile.com/b/ku2MlM/py9H)

[P00288 | 52990:53235 | NORMAL_TEXT]
[Negro, Francesco, Silvia Muceli, Anna Margherita Castronovo, Ales Holobar, and Dario Farina. 2016. “Multi-Channel Intramuscular and Surface EMG Decomposition by Convolutive Blind Source Separation.”](http://paperpile.com/b/ku2MlM/N3dD)[Journal of Neural Engineering](http://paperpile.com/b/ku2MlM/N3dD)[13 (2): 026027.](http://paperpile.com/b/ku2MlM/N3dD)

[P00289 | 53235:53441 | NORMAL_TEXT]
[Nussbaumer, R. M., D. G. Ruegg, L. M. Studer, and J-P Gabriel. 2002. “Computer Simulation of the Motoneuron Pool-Muscle Complex. I. Input System and Motoneuron Pool.”](http://paperpile.com/b/ku2MlM/JGxw)[Biological Cybernetics](http://paperpile.com/b/ku2MlM/JGxw)[86 (4): 317–33.](http://paperpile.com/b/ku2MlM/JGxw)

[P00290 | 53441:53684 | NORMAL_TEXT]
[Senefeld, Jonathon W., Kevin G. Keenan, Kevin S. Ryan, Sarah E. D’Astice, Francesco Negro, and Sandra K. Hunter. 2020. “Greater Fatigability and Motor Unit Discharge Variability in Human Type 2 Diabetes.”](http://paperpile.com/b/ku2MlM/TuGo)[Physiological Reports](http://paperpile.com/b/ku2MlM/TuGo)[8 (13): e14503.](http://paperpile.com/b/ku2MlM/TuGo)

[P00291 | 53684:53847 | NORMAL_TEXT]
[Tomar, Rimjhim, and Lubomir Kostal. 2021. “Variability and Randomness of the Instantaneous Firing Rate.”](http://paperpile.com/b/ku2MlM/Gmym)[Frontiers in Computational Neuroscience](http://paperpile.com/b/ku2MlM/Gmym)[15 (June):620410.](http://paperpile.com/b/ku2MlM/Gmym)

[P00292 | 53847:54221 | NORMAL_TEXT]
[Valli, Giacomo, Paul Ritsche, Andrea Casolo, Francesco Negro, and Giuseppe De Vito. 2024. “Tutorial: Analysis of Central and Peripheral Motor Unit Properties from Decomposed High-Density Surface EMG Signals with Openhdemg.”](http://paperpile.com/b/ku2MlM/o27l)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/o27l)[74 (February):102850.](http://paperpile.com/b/ku2MlM/o27l)

[P00293 | 54221:54587 | NORMAL_TEXT]
[Valli, Giacomo, Rui Wu, Dean Minnock, Giuseppe Sirago, Giosuè Annibalini, Andrea Casolo, Alessandro Del Vecchio, Luana Toniolo, Elena Barbieri, and Giuseppe De Vito. 2025. “Can Non-Invasive Motor Unit Analysis Reveal Distinct Neural Strategies of Force Production in Young with Uncomplicated Type 1 Diabetes?”](http://paperpile.com/b/ku2MlM/zcHs)[European Journal of Applied Physiology](http://paperpile.com/b/ku2MlM/zcHs)[125 (1): 247–59.](http://paperpile.com/b/ku2MlM/zcHs)

[P00294 | 54587:54818 | NORMAL_TEXT]
[Virtanen, Pauli, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, et al. 2020. “SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.”](http://paperpile.com/b/ku2MlM/f7C0)[Nature Methods](http://paperpile.com/b/ku2MlM/f7C0)[17 (3): 261–72.](http://paperpile.com/b/ku2MlM/f7C0)

[P00295 | 54818:55069 | NORMAL_TEXT]
[Watanabe, Kohei, Marco Gazzoni, Ales Holobar, Toshiaki Miyamoto, Kazuhito Fukuda, Roberto Merletti, and Toshio Moritani. 2013. “Motor Unit Firing Pattern of Vastus Lateralis Muscle in Type 2 Diabetes Mellitus Patients.”](http://paperpile.com/b/ku2MlM/7cHw)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/7cHw)[48 (5): 806–13](http://paperpile.com/b/ku2MlM/7cHw)[.](http://paperpile.com/b/ku2MlM/7cHw)

[P00296 | 55069:55320 | NORMAL_TEXT]
[Watanabe, Renato N., and Andre F. Kohn. 2015. “Fast Oscillatory Commands from the Motor Cortex Can Be Decoded by the Spinal Cord for Force Control.”](http://paperpile.com/b/ku2MlM/zbS9)[The Journal of Neuroscience : The Official Journal of the Society for Neuroscience](http://paperpile.com/b/ku2MlM/zbS9)[35 (40): 13687–97.](http://paperpile.com/b/ku2MlM/zbS9)

[P00297 | 55320:55619 | NORMAL_TEXT]
[Watanabe, Renato N., Fernando H. Magalhães, Leonardo A. Elias, Vitor M. Chaud, Emanuele M. Mello, and André F. Kohn. 2013. “Influences of Premotoneuronal Command Statistics on the Scaling of Motor Output Variability during Isometric Plantar Flexion.”](http://paperpile.com/b/ku2MlM/0RVK)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/0RVK)[110 (11): 2592–2606.](http://paperpile.com/b/ku2MlM/0RVK)

[P00298 | 55619:55927 | NORMAL_TEXT]
[Xiong, Y., Y. Sui, Z. Xu, Q. Zhang, M. M. Karaman, K. Cai, T. M. Anderson, W. Zhu, J. Wang, and X. J. Zhou. 2016. “A Diffusion Tensor Imaging Study on White Matter Abnormalities in Patients with Type 2 Diabetes Using Tract-Based Spatial Statistics.”](http://paperpile.com/b/ku2MlM/ypmV)[AJNR. American Journal of Neuroradiology](http://paperpile.com/b/ku2MlM/ypmV)[37 (8): 1462–69.](http://paperpile.com/b/ku2MlM/ypmV)

