# HDsEMG_rev_gdocs

- Document ID: 1q9JPv3uQm6c1VW3Gh_aCiSs1MNyepxrVoqJ3N6-XzAU
- Revision ID: AIroW37R7Vvpp1sKfIWYZEp5L_5b8Kpxfrm4gcn37NZ8pvsgPtNOPYSe45i21fkqCfabc6NrSaw3RcxUReyr56tW2Vzx83djBRQ4jtcM71s
- Selected tab: t.0
- Protected controls: 0
- Opaque controls: 0
- Authoritative dropdowns: 0

Protected-control annotations are preservation instructions. Do not insert their displayed placeholder text to recreate a native control.

## Tab 1 (t.0)

[P00001 | 1:161 | NORMAL_TEXT]
Computational modeling shows that HD-sEMG-like motor-unit selection can reverse apparent discharge-rate differences in simulated diabetic peripheral neuropathy

[P00002 | 161:162 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00003 | 162:227 | NORMAL_TEXT]
Renato Naville Watanabe, Rebeka Lorena Batichotti, Marcos Duarte

[P00004 | 227:228 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00005 | 228:328 | NORMAL_TEXT]
Biomedical Engineering Program, Federal University of ABC, São Bernardo do Campo, São Paulo, Brazil

[P00006 | 328:329 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00007 | 329:351 | NORMAL_TEXT]
Corresponding author:

[P00008 | 351:375 | NORMAL_TEXT]
Renato Naville Watanabe

[P00009 | 375:413 | NORMAL_TEXT]
E-mail: renato.watanabe@ufabc.edu.br

[P00010 | 413:422 | HEADING_1]
Abstract

[P00011 | 422:2052 | NORMAL_TEXT]
Decomposition-based EMG studies have reported lower motor-unit (MU) discharge rates in diabetic peripheral neuropathy (DPN) than in controls at matched relative contraction intensities. Whether this reflects physiology or selective representation of active MUs remains unclear. We used a neuromuscular force-control model to simulate 50 paired subjects under Normal and DPN conditions. For each subject, we compared mean MU discharge rates from three representations: an HD-sEMG-like sample comprising the 10 lowest-rate MUs with discharge rates of 5–15 pps and an interspike-interval coefficient of variation of 0.3 or less; an unrestricted random sample of 10 active MUs; and the complete active-MU population. At 20% MVC, HD-sEMG-like selection yielded a lower rate in DPN (mean paired difference, DPN minus Normal: −1.10 pps; 95% BCa CI [−1.28, −0.92]; p < 0.001). Conversely, random sampling yielded a higher rate in DPN (1.01 pps; 95% BCa CI [0.27, 1.76]; p = 0.024), as did the complete population (1.03 pps; 95% BCa CI [0.93, 1.13]; p < 0.001). Uniform sampling from the eligible subset also yielded a lower DPN rate, but with a smaller difference, showing that eligibility reversed the direction and lower-rate prioritization amplified it. The higher full-population rate in DPN was consistent with compensation for reduced MU force-generating capacity at the prescribed relative force level. These simulations show that MU selection can reverse between-condition discharge-rate differences; therefore, lower rates in HD-sEMG-like samples do not necessarily indicate lower rates across the complete active-MU population.

[P00012 | 2052:2053 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00013 | 2053:2189 | NORMAL_TEXT]
Keywords: Diabetic peripheral neuropathy, High-density surface electromyography, Motor unit, Computational modeling, EMG decomposition

[P00014 | 2189:2204 | HEADING_1]
1 Introduction

[P00015 | 2204:3059 | NORMAL_TEXT]
Motor-unit (MU) discharge behavior is a fundamental component of neuromuscular control because MU recruitment and rate coding shape muscle force generation and movement (Enoka and Farina 2021). High-density surface electromyography (HD-sEMG) is widely used to study this behavior non-invasively. By recording muscle electrical activity with a grid of closely spaced surface electrodes, HD-sEMG provides spatially distributed signals from which the discharge times of individual MUs can be estimated (Li et al. 2015). Signal decomposition separates the interference EMG signal into its constituent MU action-potential trains, enabling the estimation of recruitment and derecruitment thresholds, discharge rates, discharge variability, MU action-potential properties, and conduction velocity (Farina and Holobar 2016; Negro et al. 2016; Valli et al. 2024).

[P00016 | 3059:4094 | NORMAL_TEXT]
HD-sEMG and related decomposition-based methods have been used to investigate MU behavior in diabetes, but the available studies encompass different clinical phenotypes, muscles, contraction intensities, and outcomes. In individuals with confirmed DPN, lower mean MU discharge rates have been reported using intramuscular quantitative EMG and, in severe DPN, using HD-sEMG during contractions performed at matched relative intensities (Allen, Kimpinski, et al. 2014; Favretto et al. 2023). Studies in other diabetes populations have instead emphasized attenuated firing-rate modulation or greater discharge variability (K. Watanabe et al. 2013; Senefeld et al. 2020). More recently, lower MU discharge rates have also been reported in young individuals with uncomplicated type 1 diabetes (Valli et al. 2025). Collectively, these findings indicate altered MU discharge behavior across diabetes populations, but they do not establish that a lower mean discharge rate is a uniform property of DPN or of the complete active-MU population.

[P00017 | 4094:5082 | NORMAL_TEXT]
Interpreting a lower mean discharge rate in the identified MUs is particularly challenging because DPN is associated with motor-axon and MU loss, collateral reinnervation, slowed nerve conduction, altered MU contractile properties, and reduced muscle force-generating capacity (Allen, Kimpinski, et al. 2014; Allen, Major, et al. 2014; Favretto et al. 2023). These changes could alter afferent input, motoneuron excitability, MU force production, and the neural strategy used to maintain a target force; they therefore remain plausible physiological contributors to the reported discharge behavior. Reduced MU force-generating capacity may also require compensatory recruitment or greater discharge rates among other active MUs. At the same time, the mean obtained from a decomposed sample depends on which MUs are identified and retained. Consequently, an observed reduction may reflect altered physiology, selective representation of the active-MU population, or a combination of both.

[P00018 | 5082:6341 | NORMAL_TEXT]
HD-sEMG acquisition, decomposition, and subsequent analysis contain several potential selection mechanisms. Surface detection may favor MUs whose action potentials have larger amplitudes at the skin, while temporal superposition can make rapidly discharging MU action-potential trains more difficult to separate (Caillet et al. 2022; Negro et al. 2016). Decomposition-quality and analytical inclusion criteria may further restrict the accepted range of discharge rates or exclude MUs with high interspike-interval variability (Allen et al. 2015; Valli et al. 2024; Holobar and Zazula 2007). These mechanisms arise at different stages and need not produce the same effects. The present study did not simulate raw EMG signals, electrode geometry, MU action-potential amplitude, or the decomposition process itself. Instead, it isolated the consequences of an operational HD-sEMG-like selection procedure based on firing-rate eligibility, an interspike-interval coefficient-of-variation threshold, and preferential selection of the lower-rate eligible MUs. If the MU populations in Normal and DPN conditions have different firing-rate or variability distributions, applying the same procedure could sample systematically different portions of those populations.

[P00019 | 6341:7446 | NORMAL_TEXT]
To examine this possibility, we used a proof-of-concept computational model of neuromuscular force control to simulate paired Normal and DPN conditions during constant isometric contractions. Unlike experimental recordings, the simulations provided access to every active MU. We could therefore compare HD-sEMG-like samples of 10 MUs with unrestricted random samples of the same size and with the complete active-MU population of each simulated subject. We hypothesized that applying an HD-sEMG-like MU-selection procedure would reproduce the lower mean discharge rates reported in DPN, whereas this apparent decrease would not be observed when MUs were sampled without these restrictions or when the complete active-MU populations were compared. The prespecified primary comparison was performed at 20% MVC, with additional simulations at 10% and 50% MVC used to evaluate the influence of contraction intensity. This design allowed us to determine whether an apparent between-condition decrease produced by MU selection accurately represented the direction of the underlying population-level difference.

[P00020 | 7446:7447 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00021 | 7447:7457 | HEADING_1]
2 Methods

[P00022 | 7457:7481 | HEADING_2]
The computational model

[P00023 | 7481:8404 | NORMAL_TEXT]
We developed a computational model to simulate relevant human neurophysiological characteristics for producing a constant isometric muscle force, replicating the conditions of the experimental studies mentioned earlier. The model comprises four components designed to simulate relevant behaviors: 1) a pool of 400 neurons to generate descending commands; 2) a pool of 250 motoneurons, each modeled as a two-compartment neuron (soma and dendrite) with calcium dynamics whose firing behavior follows a gamma-point process; 3) corresponding “muscle fibers” whose force was modeled as a second-order system driven by the motoneurons (muscle-tendon dynamics were excluded as we focused on constant isometric muscle force at low levels); and 4) a controller consisting of a proportional-integral feedback loop representing visual feedback to maintain a target force level by modulating the firing rate of the descending command.

[P00024 | 8404:8882 | NORMAL_TEXT]
A schematic diagram of the model is depicted in Figure 1, and its mathematical formulation is detailed in the Appendix. This model is based on one previously developed by our group (Watanabe et al., 2013). The computational model was implemented in Python using the NEURON (M. L. Hines, Davison, and Muller 2009; M. Hines 1993) and PyNN (Davison et al. 2008) libraries. The computational code developed for this work is freely available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00025 | 8882:8883 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00026 | 8883:8885 | NORMAL_TEXT]
[INLINE_OBJECT i.0]

[P00027 | 8885:9361 | NORMAL_TEXT]
Figure 1. Schematic diagram representing force generation (F) by motor units recruited by descending commands with firing rate frequency distributed across a range. Each command activates a subset of motoneurons, leading to calcium influx (Ca²⁺) and muscle contraction through a calcium dynamics model. The total force (F) is the sum of the individual forces of the motor units. A feedback loop with a delay modulates the intervals between peaks based on the force generated.

[P00028 | 9361:9362 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00029 | 9362:9384 | HEADING_2]
Simulation conditions

[P00030 | 9384:9664 | NORMAL_TEXT]
To investigate the potential effects of DPN on motoneuron firing characteristics, simulations were conducted under two conditions with varied parameters: the normal condition represented a group of healthy subjects, and the DPN condition represented a group of patients with DPN.

[P00031 | 9664:10819 | NORMAL_TEXT]
Motor unit parameters were systematically adjusted across the two simulated conditions (see Table 1). For the DPN group, to represent the neuromuscular changes observed in diabetic neuropathy, the minimum and maximum motor unit twitch forces ([EQUATION], [EQUATION]) were reduced by a factor of 1.4, while the minimum and maximum motor unit time of contraction ([EQUATION], [EQUATION]) were concurrently increased by the same factor. To represent the conduction velocity of the nerves in diabetic neuropathy, conduction velocities of the motor nerve ([EQUATION]) were decreased by a factor of 0.85. To represent the decreased volume of the corticospinal tract in diabetic neuropathy, the number of neurons of corticospinal tract ([EQUATION]) was also reduced from 400 to 200. Importantly, the number of motoneurons, force feedback delay, and gamma order of the independent processes of the descending command remained constant across the two scenarios. All the other parameters were kept the same as used previously [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9). The parameter values that changed to represent normal and altered states are shown in Table 1. 

[P00032 | 10819:10820 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00033 | 10820:11201 | NORMAL_TEXT]
Table 1. Parameters adjusted in the two simulated conditions to represent diabetic neuropathy. Contraction force values ([EQUATION], [EQUATION]), contraction time ([EQUATION], [EQUATION]), motor conduction velocity ([EQUATION]) and number of neurons in the corticospinal tract ([EQUATION]) were modified to simulate normal and diabetic peripheral neuropathy (DPN) conditions.

[P00034 | 11201:11202 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00035 | 11205:11215 | NORMAL_TEXT | TABLE row=0 col=0]
Parameter

[P00036 | 11216:11223 | NORMAL_TEXT | TABLE row=0 col=1]
Normal

[P00037 | 11224:11228 | NORMAL_TEXT | TABLE row=0 col=2]
DPN

[P00038 | 11230:11244 | NORMAL_TEXT | TABLE row=1 col=0]
[EQUATION] (N)

[P00039 | 11245:11250 | NORMAL_TEXT | TABLE row=1 col=1]
0.04

[P00040 | 11251:11258 | NORMAL_TEXT | TABLE row=1 col=2]
0.0286

[P00041 | 11260:11274 | NORMAL_TEXT | TABLE row=2 col=0]
[EQUATION] (N)

[P00042 | 11275:11277 | NORMAL_TEXT | TABLE row=2 col=1]
4

[P00043 | 11278:11283 | NORMAL_TEXT | TABLE row=2 col=2]
2.86

[P00044 | 11285:11304 | NORMAL_TEXT | TABLE row=3 col=0]
[EQUATION] (ms)

[P00045 | 11305:11309 | NORMAL_TEXT | TABLE row=3 col=1]
110

[P00046 | 11310:11314 | NORMAL_TEXT | TABLE row=3 col=2]
154

[P00047 | 11316:11334 | NORMAL_TEXT | TABLE row=4 col=0]
[EQUATION](ms)

[P00048 | 11335:11338 | NORMAL_TEXT | TABLE row=4 col=1]
25

[P00049 | 11339:11342 | NORMAL_TEXT | TABLE row=4 col=2]
35

[P00050 | 11344:11359 | NORMAL_TEXT | TABLE row=5 col=0]
[EQUATION](m/s)

[P00051 | 11360:11363 | NORMAL_TEXT | TABLE row=5 col=1]
44

[P00052 | 11364:11369 | NORMAL_TEXT | TABLE row=5 col=2]
37.4

[P00053 | 11371:11386 | NORMAL_TEXT | TABLE row=6 col=0]
[EQUATION](m/s)

[P00054 | 11387:11390 | NORMAL_TEXT | TABLE row=6 col=1]
53

[P00055 | 11391:11397 | NORMAL_TEXT | TABLE row=6 col=2]
45.05

[P00056 | 11399:11403 | NORMAL_TEXT | TABLE row=7 col=0]
[EQUATION]

[P00057 | 11404:11408 | NORMAL_TEXT | TABLE row=7 col=1]
400

[P00058 | 11409:11413 | NORMAL_TEXT | TABLE row=7 col=2]
200

[P00059 | 11414:11415 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00060 | 11415:12031 | NORMAL_TEXT]
To introduce variability and account for biological fluctuations inherent in physiological systems, each parameter value for every simulation trial was subjected to perturbation. A random deviation from the default value was generated following a zero-mean normal distribution with a 5% coefficient of variation, thereby ensuring a degree of stochasticity while maintaining overall parameter ranges within physiologically plausible bounds. Although no formal sensitivity analysis was performed, this requirement was partially addressed by incorporating parameter variability to represent physiological fluctuations.

[P00061 | 12031:12778 | NORMAL_TEXT]
For each simulation condition, 50 trials of a 10-s isometric contraction at 20% of the maximum voluntary contraction (MVC) were conducted. The model's MVC was determined in a separate simulation trial in which all motoneurons were recruited at the maximum rate for 10 seconds; the MVC was estimated as the average force over the last 6 seconds of the simulation. To evaluate the potential influence of contraction intensity on the observed selection bias, we performed additional simulations at 10% and 50% of the maximum voluntary contraction (MVC). For each of these levels, 10 trials per condition (Normal and DPN) were conducted following the same computational protocols and parameter variability described for the primary 20% MVC condition.

[P00062 | 12778:13079 | NORMAL_TEXT]
The simulations were numerically integrated using the implicit Euler method, with derivatives estimated by Newton’s method. The numerical integration time step was 0.05 ms. These are typical values previously employed in published studies on neural computational simulation (Watanabe and Kohn, 2015).

[P00063 | 13079:13080 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00064 | 13080:13089 | HEADING_2]
Analysis

[P00065 | 13089:14488 | NORMAL_TEXT]
Motoneuron activity was analyzed over the steady-state interval from 4 to 10 s; the first 4 s were discarded to avoid transient effects. Two sampling modes were defined. In the HD-sEMG mode, active motor units were eligible when their mean firing rate was greater than 5 and less than 15 pulses per second (pps) and their interspike interval coefficient of variation (ISI-CoV) was less than or equal to 0.3. These criteria reflect the firing behavior and reliability restrictions used in studies of motor units amenable to HD-sEMG decomposition (Negro et al. 2016; Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Almeida, Riddell, and Cafarelli 2008; K. Watanabe et al. 2013; Valli et al. 2025). When more than 10 motor units met these criteria, the 10 eligible units with the lowest mean firing rates were selected, approximating the number of identified motor units commonly reported in experimental studies. Although surface recordings may preferentially detect larger, higher-threshold motor units (Caillet et al. 2022), the present operational mode modeled discharge-based selection only and did not include an explicit amplitude- or motor-unit-size-dependent detection stage. In the Random mode, 10 unique motor units were sampled without replacement from the complete pool active during the steady-state interval, without applying the HD-sEMG eligibility criteria.

[P00066 | 14488:15148 | NORMAL_TEXT]
For each motor unit, mean firing rate was calculated as the number of discharges during the 6-s steady-state interval divided by the interval duration. Interspike intervals were calculated as the temporal differences between successive discharges, and ISI-CoV was calculated as the sample standard deviation divided by the mean of those intervals. Reliable estimation required more than three interspike intervals; units with three or fewer intervals were assigned an ISI-CoV of 1.0 and therefore did not satisfy the HD-sEMG eligibility criterion. Mean firing rate and ISI-CoV were subsequently averaged across the selected motor units within each simulation.

[P00067 | 15148:15964 | NORMAL_TEXT]
For each simulated subject and condition, the mean firing rate across the complete population of motor units active during the steady-state interval was defined as the simulation truth. Because all active motor units were accessible in the simulation, this trial-specific full-population value was known exactly and served as the reference against which the HD-sEMG and Random sampling modes were evaluated. As a sensitivity analysis, 10 motor units were also sampled without replacement from the subset meeting the same firing-rate and ISI-CoV eligibility criteria, but without preferentially selecting the units with the lowest firing rates. This eligibility-restricted random analysis was used to distinguish the effect of the eligibility criteria from the additional effect of lowest-firing-rate prioritization.

[P00068 | 15964:16884 | NORMAL_TEXT]
Additional motor-unit-level analyses were descriptive and were not used for group-level inference. For Figure 3, 100 active motor units were uniformly sampled without replacement from each simulated subject and condition at 20% MVC, without applying the HD-sEMG eligibility criteria, and their mean firing rate and ISI-CoV were plotted. For Figure 4, discharge rasters were plotted for paired simulated subject 30; across all 50 paired subjects, the minimum and maximum identifiers of the selected motor units and their within-subject span, defined as the maximum minus the minimum identifier, were summarized descriptively. For Figure 5, ISI-CoV values from all recorded motor units were pooled across the 50 simulated subjects within each condition to visualize their distributions and the proportion satisfying the ISI-CoV threshold. These pooled motor-unit observations were used only for descriptive visualization.

[P00069 | 16884:17234 | NORMAL_TEXT]
At 10% and 50% MVC, the same steady-state definitions and HD-sEMG, Random, and simulation-truth analyses were applied to 10 paired simulated subjects at each force level. These additional-force analyses were treated as secondary, exploratory evaluations of whether the direction of the selection effect was maintained across contraction intensities.

[P00070 | 17234:17881 | NORMAL_TEXT]
Each trial identifier represented one simulated subject evaluated under both the Normal and DPN conditions, and observations with the same trial identifier constituted a pair. Mean firing rate was the primary outcome, and simulation-level mean ISI-CoV was a secondary outcome. Within each sampling mode or full-population reference, one mean value per simulated subject and condition was used as the unit of statistical inference. Reported values are mean ± sample SD across simulated subjects. For the simulation-truth series, the SD represents between-subject variation in the trial-specific true values rather than uncertainty in those values.

[P00071 | 17881:18993 | NORMAL_TEXT]
The primary inferential comparison was specified a priori as the paired Normal–DPN difference in mean firing rate under the HD-sEMG mode at 20% MVC. The Random, eligibility-restricted random, simulation-truth, ISI-CoV, and additional-force comparisons were secondary or exploratory; their p-values were nominal and were not adjusted for multiple comparisons. For each condition, the group mean and its bias-corrected and accelerated (BCa) 95% bootstrap confidence interval were calculated. The mean paired difference between conditions (DPN minus Normal) and its BCa 95% bootstrap confidence interval were also estimated. Confidence intervals were based on 100,000 bootstrap resamples of the simulations, sampled with replacement; paired resampling was used for the between-condition difference to preserve the Normal–DPN correspondence within each simulated subject. Two-sided Wilcoxon signed-rank tests were selected a priori for paired comparisons. The primary comparison used a significance level of 0.05. Analyses were performed in Python, and all code is available at [https://github.com/BMClab/HDsEMGbias](https://github.com/BMClab/HDsEMGbias).

[P00072 | 18993:18994 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00073 | 18994:19004 | HEADING_1]
3 Results

[P00074 | 19004:19608 | NORMAL_TEXT]
Figure 2 shows the mean motor-unit (MU) firing rates obtained from 50 paired simulated subjects under the Normal and DPN conditions. For each subject and condition, 10 active MUs were selected using two sampling strategies. In the HD-sEMG mode, the 10 MUs with the lowest firing rates were selected from those meeting the HD-sEMG-like eligibility criteria: firing rates between 5 and 15 pps and an interspike interval coefficient of variation (ISI-CoV) of 0.3 or less. In the Random mode, 10 active MUs were uniformly sampled from the complete active-MU pool without applying these eligibility criteria.

[P00075 | 19608:20576 | NORMAL_TEXT]
In the HD-sEMG mode, mean firing rate was significantly lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 9.14 ± 0.45 pps, 95% BCa CI [9.02, 9.27]; DPN, 8.04 ± 0.62 pps, 95% BCa CI [7.89, 8.23]). The mean paired difference (DPN minus Normal) was −1.10 pps (95% BCa CI [−1.28, −0.92]; Wilcoxon signed-rank W = 12.0, p < 0.001). In the Random mode, the difference was in the opposite direction: mean firing rate was significantly higher in the DPN condition (Normal, 13.05 ± 1.99 pps, 95% BCa CI [12.51, 13.61]; DPN, 14.06 ± 1.83 pps, 95% BCa CI [13.53, 14.54]). The mean paired difference was 1.01 pps (95% BCa CI [0.27, 1.76]; W = 404.0, p = 0.024). The full-population simulation truth likewise showed a higher mean firing rate in the DPN condition (Normal, 13.00 ± 0.27 pps, 95% BCa CI [12.93, 13.08]; DPN, 14.04 ± 0.40 pps, 95% BCa CI [13.93, 14.14]). The mean paired difference was 1.03 pps (95% BCa CI [0.93, 1.13]; W = 0.0, p < 0.001).

[P00076 | 20576:20577 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00077 | 20577:20579 | NORMAL_TEXT]
[INLINE_OBJECT i.1]

[P00078 | 20579:21195 | NORMAL_TEXT]
Figure 2. Mean motor-unit (MU) firing rate in the Normal and diabetic peripheral neuropathy (DPN) conditions under HD-sEMG-like (left) and Random (right) sampling. Each blue point represents the mean firing rate of 10 sampled MUs from one simulated subject (n = 50 per condition). Black plus signs and error bars indicate the across-subject mean and 95% BCa confidence interval. Red horizontal lines indicate the across-subject mean of the subject-specific simulation truths calculated using all active MUs; the same reference values are shown in both panels. Paired Normal–DPN comparisons: *p < 0.05; ***p < 0.001.

[P00079 | 21195:21196 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00080 | 21196:22150 | NORMAL_TEXT]
As a sensitivity analysis, 10 MUs were uniformly sampled from the subset meeting the same firing-rate and ISI-CoV eligibility criteria used in the HD-sEMG mode, but without preferentially selecting the MUs with the lowest firing rates. Under this eligibility-restricted random sampling, mean firing rate remained significantly lower in the DPN condition (mean ± SD: Normal, 12.20 ± 0.50 pps, 95% BCa CI [12.06, 12.33]; DPN, 11.71 ± 0.72 pps, 95% BCa CI [11.51, 11.91]). The mean paired difference (DPN minus Normal) was −0.48 pps (95% BCa CI [−0.73, −0.24]; Wilcoxon signed-rank W = 261.0, p < 0.001). This difference was smaller than that observed in the HD-sEMG mode (−1.10 pps), indicating that the eligibility criteria alone were sufficient to reverse the direction observed with unrestricted Random sampling and in the simulation truth, whereas preferential selection of the lowest-firing-rate MUs further increased the magnitude of the difference.

[P00081 | 22150:22642 | NORMAL_TEXT]
In the HD-sEMG mode, mean ISI-CoV was significantly lower in the DPN condition than in the Normal condition (mean ± SD: Normal, 0.245 ± 0.015, 95% BCa CI [0.241, 0.250]; DPN, 0.225 ± 0.021, 95% BCa CI [0.218, 0.230]). The mean paired difference (DPN minus Normal) was −0.021 (95% BCa CI [−0.027, −0.014]; Wilcoxon signed-rank W = 142.0, p < 0.001). Figure 3 separately provides a descriptive MU-level view of the relationship between firing rate and ISI-CoV across the 50 simulated subjects.

[P00082 | 22642:22643 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00083 | 22643:22645 | NORMAL_TEXT]
[INLINE_OBJECT i.2]

[P00084 | 22645:23412 | NORMAL_TEXT]
Figure 3. Relationship between mean firing rate and the interspike interval coefficient of variation (ISI-CoV) in the Normal and DPN conditions. For each simulated subject and condition, 100 active MUs were uniformly sampled without applying the HD-sEMG-like eligibility criteria, yielding 5,000 MU observations per condition across 50 subjects. Each point represents one MU and is shown descriptively rather than as an independent unit of group-level inference. Blue and orange indicate the Normal and DPN conditions, respectively. Within each condition, lighter, intermediate, and darker shades indicate earlier-recruited, intermediate, and later-recruited MUs, respectively. The inset enlarges the region containing MUs with lower ISI-CoV and higher firing rates.

[P00085 | 23412:23413 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00086 | 23413:24057 | NORMAL_TEXT]
Figure 4 shows MU discharge rasters for one paired simulated subject (simulation 30), illustrating the distribution of MUs selected by the HD-sEMG mode within the active pool. In this example, the selected MU identifiers spanned 88–146 in the Normal condition and 88–193 in the DPN condition. Across the 50 paired simulated subjects, the within-subject span of selected MU identifiers was larger on average in DPN (mean ± SD: Normal, 90.6 ± 24.3; DPN, 117.2 ± 29.5), with a larger DPN span in 37 of the 50 pairs. Across all subjects, selected MU identifiers ranged from 27 to 207 in the Normal condition and from 6 to 247 in the DPN condition.

[P00087 | 24057:24058 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00088 | 24058:24060 | NORMAL_TEXT]
[INLINE_OBJECT i.3]

[P00089 | 24060:24549 | NORMAL_TEXT]
Figure 4. Motor-unit (MU) discharge rasters for simulated subject 30 under the Normal (top) and DPN (bottom) conditions. Each point represents one MU discharge, with MUs ordered by identifier on the vertical axis. Red points show discharges from the 10 MUs selected by the HD-sEMG-like mode, while gray points show discharges from the remaining simulated MUs. The blue dashed line at 4,000 ms marks the beginning of the steady-state interval used for the firing-rate and ISI-CoV analyses.

[P00090 | 24549:24550 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00091 | 24550:24975 | NORMAL_TEXT]
Figure 5 presents a histogram of the interspike interval coefficient of variation (ISI-CoV) across all motor units for each experimental condition. Across all motor units, the average coefficient of variation (CoV) was found to be lower in the DPN condition than in the Normal condition. The proportion of motor units with an ISI-CoV of less than 0.3 increased from the Normal condition (76.9%) to the DPN condition (85.4%).

[P00092 | 24975:24976 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00093 | 24976:24978 | NORMAL_TEXT]
[INLINE_OBJECT kix.pdzorptanl8e]

[P00094 | 24978:25846 | NORMAL_TEXT]
Figure 5. Pooled distributions of the interspike interval coefficient of variation (ISI-CoV) for individual motor units (MUs) under the Normal (left) and DPN (right) conditions across 50 simulated subjects. Red dashed lines mark the HD-sEMG-like eligibility threshold of ISI-CoV = 0.3, and shaded regions indicate values below this threshold. Panel annotations show the number of MUs below the threshold and the total number included in each condition. The terminal bin includes MUs assigned an ISI-CoV of 1.0 because three or fewer interspike intervals were available during the steady-state analysis window, preventing reliable estimation; these MUs therefore did not satisfy the eligibility criterion. The x-axis is limited to 1.0 to emphasize values relevant to MU selection; ISI-CoV values above 1.0 are not displayed but remain included in the annotated totals.

[P00095 | 25846:25847 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00096 | 25847:26584 | NORMAL_TEXT]
Additional simulations at 10% and 50% MVC included 10 paired simulated subjects at each force level. At 10% MVC, the HD-sEMG mode yielded a lower mean firing rate in DPN (mean ± SD: Normal, 9.31 ± 0.39 pps; DPN, 8.21 ± 0.46 pps), with a mean paired difference of −1.10 pps (95% BCa CI [−1.38, −0.63]; W = 1.0, p = 0.004). Random sampling yielded Normal and DPN means of 10.32 ± 2.06 and 11.39 ± 2.32 pps, respectively, but the paired difference was not statistically significant (1.07 pps, 95% BCa CI [−0.70, 3.80]; W = 23.0, p = 0.695). In contrast, the simulation truth showed a higher mean firing rate in DPN (Normal, 10.09 ± 0.47 pps; DPN, 11.53 ± 0.40 pps; paired difference, 1.44 pps, 95% BCa CI [0.92, 1.83]; W = 0.0, p = 0.002).

[P00097 | 26584:27481 | NORMAL_TEXT]
At 50% MVC, the HD-sEMG mode again yielded a lower mean firing rate in DPN, although the difference was not statistically significant (Normal, 8.62 ± 0.66 pps; DPN, 8.28 ± 0.83 pps; paired difference, −0.34 pps, 95% BCa CI [−0.80, 0.22]; W = 15.0, p = 0.232). Random sampling also showed no significant difference (Normal, 17.65 ± 2.01 pps; DPN, 17.11 ± 2.06 pps; paired difference, −0.55 pps, 95% BCa CI [−2.01, 1.76]; W = 18.0, p = 0.375). The simulation truth nevertheless showed a higher mean firing rate in DPN (Normal, 16.86 ± 0.20 pps; DPN, 17.41 ± 0.37 pps; paired difference, 0.55 pps, 95% BCa CI [0.37, 0.80]; W = 0.0, p = 0.002). Thus, the direction of the HD-sEMG-mode difference was reproduced at both additional force levels, whereas the simulation truth showed the opposite direction; however, evidence for the HD-sEMG-mode difference was statistically significant only at 10% MVC.

[P00098 | 27481:27482 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00099 | 27482:27495 | HEADING_1]
4 Discussion

[P00100 | 27495:28855 | NORMAL_TEXT]
We investigated whether the lower motor-unit (MU) discharge rates previously reported in patients with diabetic peripheral neuropathy (DPN) during matched relative-force contractions could arise from selection biases associated with high-density surface electromyography (HD-sEMG) decomposition. The prespecified primary comparison at 20% MVC supported this possibility. Under HD-sEMG-like selection, mean MU firing rate was lower in the DPN condition than in the Normal condition (8.04 ± 0.62 vs. 9.14 ± 0.45 pps; paired difference, −1.10 pps; p < 0.001), consistent with previous experimental reports (Favretto et al. 2023; Allen, Kimpinski, et al. 2014; Senefeld et al. 2020; Valli et al. 2025). By contrast, unrestricted random sampling of 10 active MUs yielded a higher mean firing rate in DPN (14.06 ± 1.83 vs. 13.05 ± 1.99 pps; paired difference, 1.01 pps; p = 0.024). The full-population simulation truth was likewise higher in DPN (14.04 ± 0.40 vs. 13.00 ± 0.27 pps; paired difference, 1.03 pps; p < 0.001). The results therefore supported the selection-bias component of our hypothesis, but not the specific prediction that removing the selection criteria would eliminate the between-condition difference. Instead, the HD-sEMG-like selection procedure reversed, rather than merely attenuated, the direction of the underlying difference in the model.

[P00101 | 28855:30119 | NORMAL_TEXT]
Discharge regularity has been central to MU identification since the development of surface-EMG decomposition methods (Holobar and Zazula 2007). Criteria intended to ensure reliable decomposition cannot simply be removed from experimental analyses, because doing so may compromise identification accuracy. Surface recordings may also favor MUs that generate larger detectable potentials, while superimposition can impede identification of MUs discharging at higher rates (Caillet et al. 2022; Negro et al. 2016). Although recent algorithms seek to identify a broader range of MUs (Grison et al. 2025; Jiang et al. 2025), the representativeness of the identified sample remains important when groups differ in MU discharge behavior. The present model did not generate raw surface EMG or apply a decomposition algorithm. Instead, it operationalized selected features of HD-sEMG identification by restricting eligible MUs to firing rates between 5 and 15 pps and an interspike interval coefficient of variation (ISI-CoV) of 0.3 or less, followed by selection of the 10 eligible MUs with the lowest firing rates. The findings therefore concern the consequences of this HD-sEMG-like selection rule rather than the performance of any particular decomposition algorithm.

[P00102 | 30119:31246 | NORMAL_TEXT]
The eligibility-restricted random-sampling analysis clarified how the modeled selection procedure produced the primary result. When 10 MUs were sampled randomly from the eligible subset, without preferentially selecting those with the lowest firing rates, mean firing rate remained lower in DPN (11.71 ± 0.72 vs. 12.20 ± 0.50 pps; paired difference, −0.48 pps; p < 0.001). The joint firing-rate and ISI-CoV eligibility criteria were therefore sufficient to reverse the direction observed under unrestricted random sampling and in the full-population reference, whereas preferential selection of the lowest-firing eligible MUs increased the magnitude of the difference to −1.10 pps. Because the eligibility-restricted analysis retained both the firing-rate bounds and the ISI-CoV threshold, it does not isolate the contribution of either criterion. Similarly, because the model did not include a spatial or motor-unit-action-potential-amplitude detection stage, the findings show that explicit size-based detection was not required to reproduce the apparent reduction; they do not establish that motor-unit size is unimportant.

[P00103 | 31246:32255 | NORMAL_TEXT]
The ISI-CoV findings provide additional context for this selection mechanism. Within the HD-sEMG-like samples, the simulation-level mean ISI-CoV was modestly but significantly lower in DPN than in the Normal condition (0.225 ± 0.021 vs. 0.245 ± 0.015; p < 0.001). At the descriptive MU level, Figure 3 shows the joint distribution of firing rate and ISI-CoV, while Figure 5 shows that the pooled proportion of MUs below the ISI-CoV eligibility threshold was greater in DPN than in the Normal condition (85.4% vs. 76.9%). Together, these descriptive distributions indicate that the same eligibility rule operated on differently shaped MU populations in the two simulated conditions, thereby admitting different subsets of MUs. However, because the MU-level observations in Figures 3 and 5 were pooled for descriptive purposes, these figures do not provide independent subject-level evidence that DPN reduces ISI-CoV at a given firing rate, nor do they isolate ISI-CoV as the cause of the firing-rate reversal.

[P00104 | 32255:33166 | NORMAL_TEXT]
The higher full-population firing rate in DPN is physiologically plausible within the model and, in our view, most likely reflects compensation for the reduced force-generating capacity assigned to DPN MUs. Their twitch-force parameters were reduced by a factor of 1.4, while the feedback controller was required to maintain the same target force. A compensatory increase in MU discharge rate is therefore the most direct explanation for the higher full-population means in DPN. Other DPN-related parameters were altered concurrently, and no parameter-ablation analysis was performed; consequently, the precise contribution of reduced MU force capacity cannot be isolated from the other modeled alterations. Nevertheless, the direct relationship between reduced force per MU and the neural drive required to sustain the target force makes this the most likely causal explanation for the full-population result.

[P00105 | 33166:33954 | NORMAL_TEXT]
The supplementary analyses extended the comparison to 10% and 50% MVC. The HD-sEMG-like estimate remained lower in DPN at both force levels, whereas the full-population reference remained higher in DPN. At 10% MVC, the HD-sEMG-like difference was statistically significant (−1.10 pps; p = 0.004); at 50% MVC, the estimated difference was smaller and not statistically significant (−0.34 pps; 95% CI [−0.80, 0.22]; p = 0.232). Moreover, unrestricted random sampling did not yield a statistically significant between-condition difference at either supplementary force level. These exploratory analyses therefore demonstrate qualitative consistency in the direction of the HD-sEMG-like estimates but do not establish that the magnitude of the selection effect is independent of force level.

[P00106 | 33954:35265 | NORMAL_TEXT]
Computational models cannot reproduce the full biological and measurement complexity of the human neuromuscular system, but they provide a platform for testing hypotheses that are difficult to isolate experimentally (Farina and Negro 2015; R. N. Watanabe and Kohn 2015). The present findings do not constitute direct empirical evidence that the complete MU population in patients with DPN has normal or increased firing rates. We did not collect patient data, generate raw EMG, or process signals with an actual decomposition algorithm. The model also lacked a volume conductor, electrode geometry, MU action-potential amplitudes, and an explicit spatial detection stage. Muscle–tendon dynamics and afferent feedback from muscle spindles and Golgi tendon organs were not included, and some pathological parameter changes were estimated because precise quantitative human data were unavailable. In addition, several DPN-related parameters were varied together, preventing attribution of the results to any single alteration. Future work should incorporate spatially realistic EMG generation and decomposition, evaluate the selection rule against experimental data, and use parameter-ablation analyses to determine which physiological and measurement factors contribute most strongly to the observed differences.

[P00107 | 35265:36169 | NORMAL_TEXT]
In summary, applying an HD-sEMG-like selection rule to the simulated MU populations produced a lower mean firing rate in DPN even though unrestricted sampling and the full-population reference showed the opposite direction at the primary force level. This proof-of-concept does not demonstrate that previously reported reductions in DPN are entirely methodological artifacts. It shows, however, that a lower firing rate in an HD-sEMG-decomposed sample need not represent a reduction across the complete active-MU population. Comparisons between Normal and DPN groups should therefore consider whether pathological changes in MU discharge distributions alter which units satisfy identification and reliability criteria. Experimental validation and decomposition methods that are less sensitive to such distributional differences will be necessary to determine the extent of this bias in human recordings.

[P00108 | 36169:36170 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00109 | 36170:36179 | HEADING_1]
Appendix

[P00110 | 36179:36203 | HEADING_2]
The computational model

[P00111 | 36203:36618 | NORMAL_TEXT]
The model consists of a pool of 250 motoneurons, each modeled as a two-compartment neuron with a soma and a dendrite. The parameters of the neurons are based on data of a previous model [(R. N. Watanabe et al. 2013; R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/0RVK+zbS9) and vary exponentially between the minimal and maximal values along the motoneuron population. Here is a list of all the parameters used in model relevant to this study:

[P00112 | 36618:36619 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00113 | 36619:36670 | NORMAL_TEXT]
Table 2. List of relevant parameters of the model.

[P00114 | 36670:36671 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00115 | 36674:36684 | NORMAL_TEXT | TABLE row=0 col=0]
Parameter

[P00116 | 36685:36697 | NORMAL_TEXT | TABLE row=0 col=1]
Description

[P00117 | 36698:36703 | NORMAL_TEXT | TABLE row=0 col=2]
Unit

[P00118 | 36704:36717 | NORMAL_TEXT | TABLE row=0 col=3]
Values Range

[P00119 | 36719:36727 | NORMAL_TEXT | TABLE row=1 col=0]
[EQUATION]

[P00120 | 36728:36749 | NORMAL_TEXT | TABLE row=1 col=1]
Membrane capacitance

[P00121 | 36750:36761 | NORMAL_TEXT | TABLE row=1 col=2]
[EQUATION]

[P00122 | 36762:36764 | NORMAL_TEXT | TABLE row=1 col=3]
1

[P00123 | 36766:36774 | NORMAL_TEXT | TABLE row=2 col=0]
[EQUATION]

[P00124 | 36775:36792 | NORMAL_TEXT | TABLE row=2 col=1]
Axial resistance

[P00125 | 36793:36800 | NORMAL_TEXT | TABLE row=2 col=2]
[EQUATION]

[P00126 | 36801:36806 | NORMAL_TEXT | TABLE row=2 col=3]
0.07

[P00127 | 36808:36812 | NORMAL_TEXT | TABLE row=3 col=0]
[EQUATION]

[P00128 | 36813:36843 | NORMAL_TEXT | TABLE row=3 col=1]
Number of descending commands

[P00129 | 36844:36846 | NORMAL_TEXT | TABLE row=3 col=2]
-

[P00130 | 36847:36851 | NORMAL_TEXT | TABLE row=3 col=3]
400

[P00131 | 36853:36857 | NORMAL_TEXT | TABLE row=4 col=0]
[EQUATION]

[P00132 | 36858:36880 | NORMAL_TEXT | TABLE row=4 col=1]
Number of motor units

[P00133 | 36881:36883 | NORMAL_TEXT | TABLE row=4 col=2]
-

[P00134 | 36884:36888 | NORMAL_TEXT | TABLE row=4 col=3]
250

[P00135 | 36890:36894 | NORMAL_TEXT | TABLE row=5 col=0]
[EQUATION]

[P00136 | 36895:36923 | NORMAL_TEXT | TABLE row=5 col=1]
Motor unit twitch amplitude

[P00137 | 36924:36926 | NORMAL_TEXT | TABLE row=5 col=2]
N

[P00138 | 36927:36936 | NORMAL_TEXT | TABLE row=5 col=3]
0.04 - 4

[P00139 | 36938:36946 | NORMAL_TEXT | TABLE row=6 col=0]
[EQUATION]

[P00140 | 36947:36978 | NORMAL_TEXT | TABLE row=6 col=1]
Motor unit twitch time to peak

[P00141 | 36979:36982 | NORMAL_TEXT | TABLE row=6 col=2]
ms

[P00142 | 36983:36992 | NORMAL_TEXT | TABLE row=6 col=3]
110 - 25

[P00143 | 36994:37003 | NORMAL_TEXT | TABLE row=7 col=0]
[EQUATION]

[P00144 | 37004:37030 | NORMAL_TEXT | TABLE row=7 col=1]
Sodium reversal potential

[P00145 | 37031:37034 | NORMAL_TEXT | TABLE row=7 col=2]
mV

[P00146 | 37035:37038 | NORMAL_TEXT | TABLE row=7 col=3]
50

[P00147 | 37040:37049 | NORMAL_TEXT | TABLE row=8 col=0]
[EQUATION]

[P00148 | 37050:37084 | NORMAL_TEXT | TABLE row=8 col=1]
Slow potassium reversal potential

[P00149 | 37085:37088 | NORMAL_TEXT | TABLE row=8 col=2]
mV

[P00150 | 37089:37093 | NORMAL_TEXT | TABLE row=8 col=3]
-80

[P00151 | 37095:37104 | NORMAL_TEXT | TABLE row=9 col=0]
[EQUATION]

[P00152 | 37105:37139 | NORMAL_TEXT | TABLE row=9 col=1]
Fast potassium reversal potential

[P00153 | 37140:37143 | NORMAL_TEXT | TABLE row=9 col=2]
mV

[P00154 | 37144:37148 | NORMAL_TEXT | TABLE row=9 col=3]
-80

[P00155 | 37150:37158 | NORMAL_TEXT | TABLE row=10 col=0]
[EQUATION]

[P00156 | 37159:37196 | NORMAL_TEXT | TABLE row=10 col=1]
Proportional constant of the control

[P00157 | 37197:37203 | NORMAL_TEXT | TABLE row=10 col=2]
pps/N

[P00158 | 37204:37209 | NORMAL_TEXT | TABLE row=10 col=3]
0.05

[P00159 | 37211:37219 | NORMAL_TEXT | TABLE row=11 col=0]
[EQUATION]

[P00160 | 37220:37253 | NORMAL_TEXT | TABLE row=11 col=1]
Integral constant of the control

[P00161 | 37254:37261 | NORMAL_TEXT | TABLE row=11 col=2]
pps/Ns

[P00162 | 37262:37268 | NORMAL_TEXT | TABLE row=11 col=3]
0.005

[P00163 | 37270:37276 | NORMAL_TEXT | TABLE row=12 col=0]
[EQUATION]

[P00164 | 37277:37300 | NORMAL_TEXT | TABLE row=12 col=1]
Calcium-bound troponin

[P00165 | 37301:37305 | NORMAL_TEXT | TABLE row=12 col=2]
mol

[P00166 | 37306:37308 | NORMAL_TEXT | TABLE row=12 col=3]
-

[P00167 | 37310:37314 | NORMAL_TEXT | TABLE row=13 col=0]
[EQUATION]

[P00168 | 37315:37347 | NORMAL_TEXT | TABLE row=13 col=1]
Force produced by a muscle unit

[P00169 | 37348:37350 | NORMAL_TEXT | TABLE row=13 col=2]
N

[P00170 | 37351:37353 | NORMAL_TEXT | TABLE row=13 col=3]
-

[P00171 | 37355:37359 | NORMAL_TEXT | TABLE row=14 col=0]
[EQUATION]

[P00172 | 37360:37386 | NORMAL_TEXT | TABLE row=14 col=1]
Nerve conduction velocity

[P00173 | 37387:37391 | NORMAL_TEXT | TABLE row=14 col=2]
m/s

[P00174 | 37392:37398 | NORMAL_TEXT | TABLE row=14 col=3]
44-53

[P00175 | 37400:37404 | NORMAL_TEXT | TABLE row=15 col=0]
[EQUATION]

[P00176 | 37405:37441 | NORMAL_TEXT | TABLE row=15 col=1]
State of the fast potassium channel

[P00177 | 37442:37444 | NORMAL_TEXT | TABLE row=15 col=2]
-

[P00178 | 37445:37447 | NORMAL_TEXT | TABLE row=15 col=3]
-

[P00179 | 37449:37453 | NORMAL_TEXT | TABLE row=16 col=0]
[EQUATION]

[P00180 | 37454:37493 | NORMAL_TEXT | TABLE row=16 col=1]
Activation state of the sodium channel

[P00181 | 37494:37496 | NORMAL_TEXT | TABLE row=16 col=2]
-

[P00182 | 37497:37499 | NORMAL_TEXT | TABLE row=16 col=3]
-

[P00183 | 37501:37505 | NORMAL_TEXT | TABLE row=17 col=0]
[EQUATION]

[P00184 | 37506:37547 | NORMAL_TEXT | TABLE row=17 col=1]
Inactivation state of the sodium channel

[P00185 | 37548:37550 | NORMAL_TEXT | TABLE row=17 col=2]
-

[P00186 | 37551:37553 | NORMAL_TEXT | TABLE row=17 col=3]
-

[P00187 | 37555:37559 | NORMAL_TEXT | TABLE row=18 col=0]
[EQUATION]

[P00188 | 37560:37596 | NORMAL_TEXT | TABLE row=18 col=1]
State of the slow potassium channel

[P00189 | 37597:37599 | NORMAL_TEXT | TABLE row=18 col=2]
-

[P00190 | 37600:37602 | NORMAL_TEXT | TABLE row=18 col=3]
-

[P00191 | 37604:37612 | NORMAL_TEXT | TABLE row=19 col=0]
[EQUATION]

[P00192 | 37613:37637 | NORMAL_TEXT | TABLE row=19 col=1]
Soma membrane potential

[P00193 | 37638:37641 | NORMAL_TEXT | TABLE row=19 col=2]
mV

[P00194 | 37642:37644 | NORMAL_TEXT | TABLE row=19 col=3]
-

[P00195 | 37646:37654 | NORMAL_TEXT | TABLE row=20 col=0]
[EQUATION]

[P00196 | 37655:37683 | NORMAL_TEXT | TABLE row=20 col=1]
Dendrite membrane potential

[P00197 | 37684:37687 | NORMAL_TEXT | TABLE row=20 col=2]
mV

[P00198 | 37688:37690 | NORMAL_TEXT | TABLE row=20 col=3]
-

[P00199 | 37692:37700 | NORMAL_TEXT | TABLE row=21 col=0]
[EQUATION]

[P00200 | 37701:37727 | NORMAL_TEXT | TABLE row=21 col=1]
Soma membrane capacitance

[P00201 | 37728:37733 | NORMAL_TEXT | TABLE row=21 col=2]
[EQUATION]

[P00202 | 37734:37736 | NORMAL_TEXT | TABLE row=21 col=3]
-

[P00203 | 37738:37746 | NORMAL_TEXT | TABLE row=22 col=0]
[EQUATION]

[P00204 | 37747:37777 | NORMAL_TEXT | TABLE row=22 col=1]
Dendrite membrane capacitance

[P00205 | 37778:37783 | NORMAL_TEXT | TABLE row=22 col=2]
[EQUATION]

[P00206 | 37784:37786 | NORMAL_TEXT | TABLE row=22 col=3]
-

[P00207 | 37788:37798 | NORMAL_TEXT | TABLE row=23 col=0]
[EQUATION]

[P00208 | 37799:37832 | NORMAL_TEXT | TABLE row=23 col=1]
conductance of the soma membrane

[P00209 | 37833:37836 | NORMAL_TEXT | TABLE row=23 col=2]
mS

[P00210 | 37837:37839 | NORMAL_TEXT | TABLE row=23 col=3]
-

[P00211 | 37841:37851 | NORMAL_TEXT | TABLE row=24 col=0]
[EQUATION]

[P00212 | 37852:37889 | NORMAL_TEXT | TABLE row=24 col=1]
conductance of the dendrite membrane

[P00213 | 37890:37893 | NORMAL_TEXT | TABLE row=24 col=2]
mS

[P00214 | 37894:37895 | NORMAL_TEXT | TABLE row=24 col=3]
⟦EMPTY PARAGRAPH⟧

[P00215 | 37897:37909 | NORMAL_TEXT | TABLE row=25 col=0]
[EQUATION]

[P00216 | 37910:37930 | NORMAL_TEXT | TABLE row=25 col=1]
Sodium conductance 

[P00217 | 37931:37934 | NORMAL_TEXT | TABLE row=25 col=2]
mS

[P00218 | 37935:37944 | NORMAL_TEXT | TABLE row=25 col=3]
[EQUATION]

[P00219 | 37946:37958 | NORMAL_TEXT | TABLE row=26 col=0]
[EQUATION]

[P00220 | 37959:37987 | NORMAL_TEXT | TABLE row=26 col=1]
Fast potassium conductance 

[P00221 | 37988:37991 | NORMAL_TEXT | TABLE row=26 col=2]
mS

[P00222 | 37992:37997 | NORMAL_TEXT | TABLE row=26 col=3]
2.25

[P00223 | 37999:38011 | NORMAL_TEXT | TABLE row=27 col=0]
[EQUATION]

[P00224 | 38012:38040 | NORMAL_TEXT | TABLE row=27 col=1]
Slow potassium conductance 

[P00225 | 38041:38044 | NORMAL_TEXT | TABLE row=27 col=2]
mS

[P00226 | 38045:38049 | NORMAL_TEXT | TABLE row=27 col=3]
0.1

[P00227 | 38050:38051 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00228 | 38051:38444 | NORMAL_TEXT]
The somatic compartment of each motor neuron includes sodium, slow potassium, and fast potassium channels, modeled using the structure of the Hodgkin-Huxley model [(Hodgkin and Huxley 1952)](https://paperpile.com/c/ku2MlM/nbxX) and is described elsewhere [(Destexhe and Paré 1999; Cisi and Kohn 2008)](https://paperpile.com/c/ku2MlM/ap2G+8qUP). The differential equations that describe the membrane potentials of the soma (Vs) and dendrite (Vd) models of each motoneuron are:

[P00229 | 38444:38532 | NORMAL_TEXT]
[EQUATION]

[P00230 | 38532:38620 | NORMAL_TEXT]
[EQUATION]

[P00231 | 38620:39049 | NORMAL_TEXT]
The values of [EQUATION]and [EQUATION] (capacitance of the soma membrane, capacitance of the dendrite membrane, conductance of the soma membrane, conductance of the dendrite membrane and conductance between soma and dendrite, respectively) are the same used by [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9). The ionic current of the soma is the sum of the currents of the sodium, fast potassium and slow potassium channels:

[P00232 | 39049:39175 | NORMAL_TEXT]
[EQUATION]

[P00233 | 39175:39283 | NORMAL_TEXT]
The differential equation of the [EQUATION], [EQUATION] and  [EQUATION] state variables are as used in [(Destexhe and Paré 1999)](https://paperpile.com/c/ku2MlM/ap2G):

[P00234 | 39283:39326 | NORMAL_TEXT]
[EQUATION]

[P00235 | 39326:39434 | NORMAL_TEXT]
with [EQUATION] being the state variables [EQUATION], [EQUATION] or [EQUATION]. The constants [EQUATION] and [EQUATION] for each state variable are: 

[P00236 | 39434:39575 | NORMAL_TEXT]
[EQUATION] and [EQUATION]

[P00237 | 39575:39677 | NORMAL_TEXT]
[EQUATION] and [EQUATION]

[P00238 | 39677:39790 | NORMAL_TEXT]
[EQUATION]and [EQUATION]

[P00239 | 39790:39874 | NORMAL_TEXT]
The differential equation of the [EQUATION] state is as used in [(Nussbaumer et al. 2002)](https://paperpile.com/c/ku2MlM/JGxw): 

[P00240 | 39874:39910 | NORMAL_TEXT]
[EQUATION]

[P00241 | 39910:39915 | NORMAL_TEXT]
with

[P00242 | 39915:40018 | NORMAL_TEXT]
[EQUATION]and [EQUATION]

[P00243 | 40018:40191 | NORMAL_TEXT]
The values of [EQUATION]are the motoneuron threshold for firing and are the same used in [(R. N. Watanabe and Kohn 2015)](https://paperpile.com/c/ku2MlM/zbS9) and [EQUATION] is the membrane potential of the soma. 

[P00244 | 40191:40880 | NORMAL_TEXT]
The calcium dynamics of each motor unit follows the model developed previously by [(Kim and Heckman 2023)](https://paperpile.com/c/ku2MlM/ueNw). This model accounts for several key processes, including the concentration of sarcoplasmic calcium, the reaction of calcium and calsequestrin within the sarcoplasmic reticulum, calcium release and uptake through the sarcoplasmic reticulum membrane, calcium buffering, calcium-troponin binding, and the resulting muscle unit activation level. Muscle force is generated from the activation of the calcium dynamics model using a second-order linear model [(Cisi and Kohn 2008; Fuglevand, Winter, and Patla 1993)](https://paperpile.com/c/ku2MlM/8qUP+tjpv). The differential equation of the force generation for each motor unit is:

[P00245 | 40880:40990 | NORMAL_TEXT]
[EQUATION]

[P00246 | 40990:41311 | NORMAL_TEXT]
In the equation above [EQUATION]is force the motor unit [EQUATION] produces through time, [EQUATION] is the contraction time of the motor unit [EQUATION], [EQUATION] is the maximum twitch force of the motor unit [EQUATION] has and [EQUATION] is the muscle unit calcium-troponin binding through time obtained from the calcium dynamics model.

[P00247 | 41311:41641 | NORMAL_TEXT]
The descending command consists of [EQUATION] independent neurons (see Figure 1) (R. N. Watanabe et al. 2013). Each descending command connects to approximately 10% of the motoneurons, randomly. For this work, only excitatory synapses were used. Each synapse from the descending command generates a current following the equation below:

[P00248 | 41641:41670 | NORMAL_TEXT]
[EQUATION]

[P00249 | 41670:41867 | NORMAL_TEXT]
The dynamics of [EQUATION] follows a first-order dynamics with time constant [EQUATION] ms with each incoming spike adding a conductance of [EQUATION] nS. The synaptic delay is 0.2 ms.

[P00250 | 41867:42413 | NORMAL_TEXT]
The mean discharge rate of the gamma distribution of each descending command is modulated by the level of force produced, following a proportional-integral controller, with a force level specified at the beginning of the simulation as a reference, with the proportional constant [EQUATION] and the integral constant [EQUATION] (see Figure 1). A 60 ms temporal delay was incorporated into the force feedback loop to simulate the visual feedback, typically provided to participants during isometric contraction paradigms.

[P00251 | 42413:42414 | NORMAL_TEXT]
⟦EMPTY PARAGRAPH⟧

[P00252 | 42414:42427 | HEADING_1]
6 References

[P00253 | 42427:42735 | NORMAL_TEXT]
[Allen, Matti D., Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Length Dependent Loss of Motor Axons and Altered Motor Unit Properties in Human Diabetic Polyneuropathy.”](http://paperpile.com/b/ku2MlM/PRcA)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/PRcA)[125 (4): 836–43.](http://paperpile.com/b/ku2MlM/PRcA)

[P00254 | 42735:43012 | NORMAL_TEXT]
[Allen, Matti D., Brendan Major, Kurt Kimpinski, Timothy J. Doherty, and Charles L. Rice. 2014. “Skeletal Muscle Morphology and Contractile Function in Relation to Muscle Denervation in Diabetic Neuropathy.”](http://paperpile.com/b/ku2MlM/jR7N)[Journal of Applied Physiology (Bethesda, Md. : 1985)](http://paperpile.com/b/ku2MlM/jR7N)[116 (5): 545–52.](http://paperpile.com/b/ku2MlM/jR7N)

[P00255 | 43012:43426 | NORMAL_TEXT]
[Allen, Matti D., Daniel W. Stashuk, Kurt Kimpinski, Timothy J. Doherty, Maddison L. Hourigan, and Charles L. Rice. 2015. “Increased Neuromuscular Transmission Instability and Motor Unit Remodelling with Diabetic Neuropathy as Assessed Using Novel near Fibre Motor Unit Potential Parameters.”](http://paperpile.com/b/ku2MlM/LtlU)[Clinical Neurophysiology : Official Journal of the International Federation of Clinical Neurophysiology](http://paperpile.com/b/ku2MlM/LtlU)[126 (4): 794–802.](http://paperpile.com/b/ku2MlM/LtlU)

[P00256 | 43426:43663 | NORMAL_TEXT]
[Almeida, S., M. C. Riddell, and E. Cafarelli. 2008. “Slower Conduction Velocity and Motor Unit Discharge Frequency Are Associated with Muscle Fatigue during Isometric Exercise in Type 1 Diabetes Mellitus.”](http://paperpile.com/b/ku2MlM/V9si)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/V9si)[37 (2): 231–40.](http://paperpile.com/b/ku2MlM/V9si)

[P00257 | 43663:43985 | NORMAL_TEXT]
[Aye, Tandy, Naama Barnea-Goraly, Christian Ambler, Sherry Hoang, Kristin Schleifer, Yaena Park, Jessica Drobny, Darrell M. Wilson, Allan L. Reiss, and Bruce A. Buckingham. 2012. “White Matter Structural Differences in Young Children with Type 1 Diabetes: A Diffusion Tensor Imaging Study.”](http://paperpile.com/b/ku2MlM/1pPD)[Diabetes Care](http://paperpile.com/b/ku2MlM/1pPD)[35 (11): 2167–73.](http://paperpile.com/b/ku2MlM/1pPD)

[P00258 | 43985:44267 | NORMAL_TEXT]
[Caillet, Arnault H., Andrew T. M. Phillips, Dario Farina, and Luca Modenese. 2022. “Estimation of the Firing Behaviour of a Complete Motoneuron Pool by Combining Electromyography Signal Decomposition and Realistic Motoneuron Modelling.”](http://paperpile.com/b/ku2MlM/p4VN)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/p4VN)[18 (9): e1010556.](http://paperpile.com/b/ku2MlM/p4VN)

[P00259 | 44267:44561 | NORMAL_TEXT]
[Cardoso de Oliveira, Marina, Renato Naville Watanabe, and André Fabio Kohn. 2022. “Electrophysiological and Functional Signs of Guillain-Barré Syndrome Predicted by a Multiscale Neuromuscular Computational Model.”](http://paperpile.com/b/ku2MlM/GVkn)[Journal of Neural Engineering](http://paperpile.com/b/ku2MlM/GVkn)[19 (5). https://doi.org/](http://paperpile.com/b/ku2MlM/GVkn)[10.1088/1741-2552/ac91f8](http://dx.doi.org/10.1088/1741-2552/ac91f8)[.](http://paperpile.com/b/ku2MlM/GVkn)

[P00260 | 44561:44773 | NORMAL_TEXT]
[Cisi, Rogerio R. L., and André F. Kohn. 2008. “Simulation System of Spinal Cord Motor Nuclei and Associated Nerves and Muscles, in a Web-Based Architecture.”](http://paperpile.com/b/ku2MlM/8qUP)[Journal of Computational Neuroscience](http://paperpile.com/b/ku2MlM/8qUP)[25 (3): 520–42.](http://paperpile.com/b/ku2MlM/8qUP)

[P00261 | 44773:45006 | NORMAL_TEXT]
[Davison, Andrew P., Daniel Brüderle, Jochen Eppler, Jens Kremkow, Eilif Muller, Dejan Pecevski, Laurent Perrinet, and Pierre Yger. 2008. “PyNN: A Common Interface for Neuronal Network Simulators.”](http://paperpile.com/b/ku2MlM/9z19)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/9z19)[2:11.](http://paperpile.com/b/ku2MlM/9z19)

[P00262 | 45006:45184 | NORMAL_TEXT]
[Destexhe, A., and D. Paré. 1999. “Impact of Network Activity on the Integrative Properties of Neocortical Pyramidal Neurons in Vivo.”](http://paperpile.com/b/ku2MlM/ap2G)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/ap2G)[81 (4): 1531–47.](http://paperpile.com/b/ku2MlM/ap2G)

[P00263 | 45184:45327 | NORMAL_TEXT]
[Enoka, Roger M., and Dario Farina. 2021. “Force Steadiness: From Motor Units to Voluntary Actions.”](http://paperpile.com/b/ku2MlM/GtoK)[Physiology (Bethesda, Md.)](http://paperpile.com/b/ku2MlM/GtoK)[36 (2): 114–30.](http://paperpile.com/b/ku2MlM/GtoK)

[P00264 | 45327:45470 | NORMAL_TEXT]
[Eshima, Hiroaki, David C. Poole, and Yutaka Kano. 2014. “In Vivo Calcium Regulation in Diabetic Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/zhBj)[Cell Calcium](http://paperpile.com/b/ku2MlM/zhBj)[56 (5): 381–89.](http://paperpile.com/b/ku2MlM/zhBj)

[P00265 | 45470:45673 | NORMAL_TEXT]
[Farina, Dario, and Ales Holobar. 2016. “Characterization of Human Motor Units from Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/jbAP)[Proceedings of the IEEE. Institute of Electrical and Electronics Engineers](http://paperpile.com/b/ku2MlM/jbAP)[104 (2): 353–73.](http://paperpile.com/b/ku2MlM/jbAP)

[P00266 | 45673:45855 | NORMAL_TEXT]
[Farina, Dario, and Francesco Negro. 2015. “Common Synaptic Input to Motor Neurons, Motor Unit Synchronization, and Force Control.”](http://paperpile.com/b/ku2MlM/4xcD)[Exercise and Sport Sciences Reviews](http://paperpile.com/b/ku2MlM/4xcD)[43 (1): 23–33.](http://paperpile.com/b/ku2MlM/4xcD)

[P00267 | 45855:46295 | NORMAL_TEXT]
[Favretto, Mateus André, Felipe Rettore Andreis, Sandra Cossul, Francesco Negro, Anderson Souza Oliveira, and Jefferson Luiz Brum Marques. 2023. “Differences in Motor Unit Behavior during Isometric Contractions in Patients with Diabetic Peripheral Neuropathy at Various Disease Severities.”](http://paperpile.com/b/ku2MlM/5qJ6)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/5qJ6)[68 (February):102725.](http://paperpile.com/b/ku2MlM/5qJ6)

[P00268 | 46295:46468 | NORMAL_TEXT]
[Fuglevand, A. J., D. A. Winter, and A. E. Patla. 1993. “Models of Recruitment and Rate Coding Organization in Motor-Unit Pools.”](http://paperpile.com/b/ku2MlM/tjpv)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/tjpv)[70 (6): 2470–88.](http://paperpile.com/b/ku2MlM/tjpv)

[P00269 | 46468:46746 | NORMAL_TEXT]
[Grison, Agnese, Irene Mendez Guerra, Alexander Kenneth Clarke, Silvia Muceli, Jaime Ibáñez, and Dario Farina. 2025. “Unlocking the Full Potential of High-Density Surface EMG: Novel Non-Invasive High-Yield Motor Unit Decomposition.”](http://paperpile.com/b/ku2MlM/QyGL)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/QyGL)[603 (8): 2281–2300.](http://paperpile.com/b/ku2MlM/QyGL)

[P00270 | 46746:46942 | NORMAL_TEXT]
[Harris, Charles R., K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, et al. 2020. “Array Programming with NumPy.”](http://paperpile.com/b/ku2MlM/HVd0)[Nature](http://paperpile.com/b/ku2MlM/HVd0)[585 (7825): 357–62.](http://paperpile.com/b/ku2MlM/HVd0)

[P00271 | 46942:47039 | NORMAL_TEXT]
[Heckman, C. J., and Roger M. Enoka. 2012. “Motor Unit.”](http://paperpile.com/b/ku2MlM/mzRP)[Comprehensive Physiology](http://paperpile.com/b/ku2MlM/mzRP)[2 (4): 2629–82.](http://paperpile.com/b/ku2MlM/mzRP)

[P00272 | 47039:47192 | NORMAL_TEXT]
[Hines, Michael. 1993. “NEURON — A Program for Simulation of Nerve Equations.” In](http://paperpile.com/b/ku2MlM/Vcj2)[Neural Systems: Analysis and Modeling](http://paperpile.com/b/ku2MlM/Vcj2)[, 127–36. Boston, MA: Springer US.](http://paperpile.com/b/ku2MlM/Vcj2)

[P00273 | 47192:47320 | NORMAL_TEXT]
[Hines, Michael L., Andrew P. Davison, and Eilif Muller. 2009. “NEURON and Python.”](http://paperpile.com/b/ku2MlM/jjzD)[Frontiers in Neuroinformatics](http://paperpile.com/b/ku2MlM/jjzD)[3 (January):1.](http://paperpile.com/b/ku2MlM/jjzD)

[P00274 | 47320:47512 | NORMAL_TEXT]
[Hodgkin, A. L., and A. F. Huxley. 1952. “A Quantitative Description of Membrane Current and Its Application to Conduction and Excitation in Nerve.”](http://paperpile.com/b/ku2MlM/nbxX)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/nbxX)[117 (4): 500–544.](http://paperpile.com/b/ku2MlM/nbxX)

[P00275 | 47512:47744 | NORMAL_TEXT]
[Holobar, Aleš, and Damjan Zazula. 2007. “Gradient Convolution Kernel Compensation Applied to Surface Electromyograms.” In](http://paperpile.com/b/ku2MlM/C6Et)[Independent Component Analysis and Signal Separation](http://paperpile.com/b/ku2MlM/C6Et)[, 617–24. Berlin, Heidelberg: Springer Berlin Heidelberg.](http://paperpile.com/b/ku2MlM/C6Et)

[P00276 | 47744:47971 | NORMAL_TEXT]
[Holobar, Ales, and Damjan Zazula. 2007. “Multichannel Blind Source Separation Using Convolution Kernel Compensation.”](http://paperpile.com/b/ku2MlM/nHk7)[IEEE Transactions on Signal Processing: A Publication of the IEEE Signal Processing Society](http://paperpile.com/b/ku2MlM/nHk7)[55 (9): 4487–96.](http://paperpile.com/b/ku2MlM/nHk7)

[P00277 | 47971:48083 | NORMAL_TEXT]
[Hunter, John D. 2007. “Matplotlib: A 2D Graphics Environment.”](http://paperpile.com/b/ku2MlM/SRer)[Computing in Science & Engineering](http://paperpile.com/b/ku2MlM/SRer)[9 (3): 90–95.](http://paperpile.com/b/ku2MlM/SRer)

[P00278 | 48083:48313 | NORMAL_TEXT]
[Jiang, Xi, Weiyu Guo, Ziwei Cui, Chuang Lin, and Jingyong Su. 2025. “Decomposition of High-Density sEMG Signals: Extracting Multiple Spikes from Single Time Windows.”](http://paperpile.com/b/ku2MlM/K78i)[Biomedical Signal Processing and Control](http://paperpile.com/b/ku2MlM/K78i)[107 (107771): 107771.](http://paperpile.com/b/ku2MlM/K78i)

[P00279 | 48313:48700 | NORMAL_TEXT]
[Junquera-Godoy, I., J. L. Martinez-De-Juan, G. González Lorente, J. M. Carot-Sierra, J. Gomis-Tena, J. Saiz, R. López Mateu, et al. 2025. “Surface Electromyography for Characterizing Neuromuscular Changes in Diabetic Peripheral Neuropathy.”](http://paperpile.com/b/ku2MlM/wc3t)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/wc3t)[82 (June):102991.](http://paperpile.com/b/ku2MlM/wc3t)

[P00280 | 48700:48876 | NORMAL_TEXT]
[Kim, Hojeong, and Charles J. Heckman. 2023. “A Dynamic Calcium-Force Relationship Model for Sag Behavior in Fast Skeletal Muscle.”](http://paperpile.com/b/ku2MlM/ueNw)[PLoS Computational Biology](http://paperpile.com/b/ku2MlM/ueNw)[19 (6): e1011178.](http://paperpile.com/b/ku2MlM/ueNw)

[P00281 | 48876:49139 | NORMAL_TEXT]
[Klein Horsman, M. D., H. F. J. M. Koopman, F. C. T. van der Helm, L. Poliacu Prosé, and H. E. J. Veeger. 2007. “Morphological Muscle and Joint Parameters for Musculoskeletal Modelling of the Lower Extremity.”](http://paperpile.com/b/ku2MlM/HeGb)[Clinical Biomechanics (Bristol, Avon)](http://paperpile.com/b/ku2MlM/HeGb)[22 (2): 239–47.](http://paperpile.com/b/ku2MlM/HeGb)

[P00282 | 49139:49334 | NORMAL_TEXT]
[Klueber, K. M., and J. D. Feczko. 1994. “Ultrastructural, Histochemical, and Morphometric Analysis of Skeletal Muscle in a Murine Model of Type I Diabetes.”](http://paperpile.com/b/ku2MlM/2p6W)[The Anatomical Record](http://paperpile.com/b/ku2MlM/2p6W)[239 (1): 18–34.](http://paperpile.com/b/ku2MlM/2p6W)

[P00283 | 49334:49678 | NORMAL_TEXT]
[Lecce, Edoardo, Alessio Bellini, Giuseppe Greco, Fiorella Martire, Alessandro Scotto di Palumbo, Massimo Sacchetti, and Ilenia Bazzucchi. 2025. “Physiological Mechanisms of Neuromuscular Impairment in Diabetes-Related Complications: Can Physical Exercise Help Prevent It?”](http://paperpile.com/b/ku2MlM/cyvg)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/cyvg)[, February. https://doi.org/](http://paperpile.com/b/ku2MlM/cyvg)[10.1113/JP287589](http://dx.doi.org/10.1113/JP287589)[.](http://paperpile.com/b/ku2MlM/cyvg)

[P00284 | 49678:50052 | NORMAL_TEXT]
[Liang, Lucy, Arianna Damiani, Matteo Del Brocco, Evan R. Rogers, Maria K. Jantz, Lee E. Fisher, Robert A. Gaunt, Marco Capogrosso, Scott F. Lempka, and Elvira Pirondini. 2023. “A Systematic Review of Computational Models for the Design of Spinal Cord Stimulation Therapies: From Neural Circuits to Patient-Specific Simulations.”](http://paperpile.com/b/ku2MlM/kXVU)[The Journal of Physiology](http://paperpile.com/b/ku2MlM/kXVU)[601 (15): 3103–21.](http://paperpile.com/b/ku2MlM/kXVU)

[P00285 | 50052:50329 | NORMAL_TEXT]
[Li, Xiaoyan, Ales Holobar, Marco Gazzoni, Roberto Merletti, William Zev Rymer, and Ping Zhou. 2015. “Examination of Poststroke Alteration in Motor Unit Firing Behavior Using High-Density Surface EMG Decomposition.”](http://paperpile.com/b/ku2MlM/py9H)[IEEE Transactions on Bio-Medical Engineering](http://paperpile.com/b/ku2MlM/py9H)[62 (5): 1242–52.](http://paperpile.com/b/ku2MlM/py9H)

[P00286 | 50329:50574 | NORMAL_TEXT]
[Negro, Francesco, Silvia Muceli, Anna Margherita Castronovo, Ales Holobar, and Dario Farina. 2016. “Multi-Channel Intramuscular and Surface EMG Decomposition by Convolutive Blind Source Separation.”](http://paperpile.com/b/ku2MlM/N3dD)[Journal of Neural Engineering](http://paperpile.com/b/ku2MlM/N3dD)[13 (2): 026027.](http://paperpile.com/b/ku2MlM/N3dD)

[P00287 | 50574:50780 | NORMAL_TEXT]
[Nussbaumer, R. M., D. G. Ruegg, L. M. Studer, and J-P Gabriel. 2002. “Computer Simulation of the Motoneuron Pool-Muscle Complex. I. Input System and Motoneuron Pool.”](http://paperpile.com/b/ku2MlM/JGxw)[Biological Cybernetics](http://paperpile.com/b/ku2MlM/JGxw)[86 (4): 317–33.](http://paperpile.com/b/ku2MlM/JGxw)

[P00288 | 50780:51085 | NORMAL_TEXT]
[Perantie, Dana C., Jenny Wu, Jonathan M. Koller, Audrey Lim, Stacie L. Warren, Kevin J. Black, Michelle Sadler, Neil H. White, and Tamara Hershey. 2007. “Regional Brain Volume Differences Associated with Hyperglycemia and Severe Hypoglycemia in Youth with Type 1 Diabetes.”](http://paperpile.com/b/ku2MlM/IDFc)[Diabetes Care](http://paperpile.com/b/ku2MlM/IDFc)[30 (9): 2331–37.](http://paperpile.com/b/ku2MlM/IDFc)

[P00289 | 51085:51168 | NORMAL_TEXT]
[Perkel, Jeffrey M. 2015. “Programming: Pick up Python.”](http://paperpile.com/b/ku2MlM/xpwa)[Nature](http://paperpile.com/b/ku2MlM/xpwa)[518 (7537): 125–26.](http://paperpile.com/b/ku2MlM/xpwa)

[P00290 | 51168:51411 | NORMAL_TEXT]
[Senefeld, Jonathon W., Kevin G. Keenan, Kevin S. Ryan, Sarah E. D’Astice, Francesco Negro, and Sandra K. Hunter. 2020. “Greater Fatigability and Motor Unit Discharge Variability in Human Type 2 Diabetes.”](http://paperpile.com/b/ku2MlM/TuGo)[Physiological Reports](http://paperpile.com/b/ku2MlM/TuGo)[8 (13): e14503.](http://paperpile.com/b/ku2MlM/TuGo)

[P00291 | 51411:51697 | NORMAL_TEXT]
[Singh-Peters, Lynette A., Gareth R. Jones, Kenji A. Kenno, and Jennifer M. Jakobi. 2007. “Strength and Contractile Properties Are Similar between Persons with Type 2 Diabetes and Age-,weight-, Gender- and Physical Activitymatched Controls.”](http://paperpile.com/b/ku2MlM/FCjz)[Canadian Journal of Diabetes](http://paperpile.com/b/ku2MlM/FCjz)[31 (4): 357–64.](http://paperpile.com/b/ku2MlM/FCjz)

[P00292 | 51697:51860 | NORMAL_TEXT]
[Tomar, Rimjhim, and Lubomir Kostal. 2021. “Variability and Randomness of the Instantaneous Firing Rate.”](http://paperpile.com/b/ku2MlM/Gmym)[Frontiers in Computational Neuroscience](http://paperpile.com/b/ku2MlM/Gmym)[15 (June):620410.](http://paperpile.com/b/ku2MlM/Gmym)

[P00293 | 51860:52234 | NORMAL_TEXT]
[Valli, Giacomo, Paul Ritsche, Andrea Casolo, Francesco Negro, and Giuseppe De Vito. 2024. “Tutorial: Analysis of Central and Peripheral Motor Unit Properties from Decomposed High-Density Surface EMG Signals with Openhdemg.”](http://paperpile.com/b/ku2MlM/o27l)[Journal of Electromyography and Kinesiology : Official Journal of the International Society of Electrophysiological Kinesiology](http://paperpile.com/b/ku2MlM/o27l)[74 (February):102850.](http://paperpile.com/b/ku2MlM/o27l)

[P00294 | 52234:52600 | NORMAL_TEXT]
[Valli, Giacomo, Rui Wu, Dean Minnock, Giuseppe Sirago, Giosuè Annibalini, Andrea Casolo, Alessandro Del Vecchio, Luana Toniolo, Elena Barbieri, and Giuseppe De Vito. 2025. “Can Non-Invasive Motor Unit Analysis Reveal Distinct Neural Strategies of Force Production in Young with Uncomplicated Type 1 Diabetes?”](http://paperpile.com/b/ku2MlM/zcHs)[European Journal of Applied Physiology](http://paperpile.com/b/ku2MlM/zcHs)[125 (1): 247–59.](http://paperpile.com/b/ku2MlM/zcHs)

[P00295 | 52600:52831 | NORMAL_TEXT]
[Virtanen, Pauli, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, et al. 2020. “SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.”](http://paperpile.com/b/ku2MlM/f7C0)[Nature Methods](http://paperpile.com/b/ku2MlM/f7C0)[17 (3): 261–72.](http://paperpile.com/b/ku2MlM/f7C0)

[P00296 | 52831:53082 | NORMAL_TEXT]
[Watanabe, Kohei, Marco Gazzoni, Ales Holobar, Toshiaki Miyamoto, Kazuhito Fukuda, Roberto Merletti, and Toshio Moritani. 2013. “Motor Unit Firing Pattern of Vastus Lateralis Muscle in Type 2 Diabetes Mellitus Patients.”](http://paperpile.com/b/ku2MlM/7cHw)[Muscle & Nerve](http://paperpile.com/b/ku2MlM/7cHw)[48 (5): 806–13](http://paperpile.com/b/ku2MlM/7cHw)[.](http://paperpile.com/b/ku2MlM/7cHw)

[P00297 | 53082:53333 | NORMAL_TEXT]
[Watanabe, Renato N., and Andre F. Kohn. 2015. “Fast Oscillatory Commands from the Motor Cortex Can Be Decoded by the Spinal Cord for Force Control.”](http://paperpile.com/b/ku2MlM/zbS9)[The Journal of Neuroscience : The Official Journal of the Society for Neuroscience](http://paperpile.com/b/ku2MlM/zbS9)[35 (40): 13687–97.](http://paperpile.com/b/ku2MlM/zbS9)

[P00298 | 53333:53632 | NORMAL_TEXT]
[Watanabe, Renato N., Fernando H. Magalhães, Leonardo A. Elias, Vitor M. Chaud, Emanuele M. Mello, and André F. Kohn. 2013. “Influences of Premotoneuronal Command Statistics on the Scaling of Motor Output Variability during Isometric Plantar Flexion.”](http://paperpile.com/b/ku2MlM/0RVK)[Journal of Neurophysiology](http://paperpile.com/b/ku2MlM/0RVK)[110 (11): 2592–2606.](http://paperpile.com/b/ku2MlM/0RVK)

[P00299 | 53632:53794 | NORMAL_TEXT]
[Wolpert, Daniel M., Zoubin Ghahramani, and J. Randall Flanagan. 2001. “Perspectives and Problems in Motor Learning.”](http://paperpile.com/b/ku2MlM/6WoP)[Trends in Cognitive Sciences](http://paperpile.com/b/ku2MlM/6WoP)[5 (11): 487–94.](http://paperpile.com/b/ku2MlM/6WoP)

[P00300 | 53794:54102 | NORMAL_TEXT]
[Xiong, Y., Y. Sui, Z. Xu, Q. Zhang, M. M. Karaman, K. Cai, T. M. Anderson, W. Zhu, J. Wang, and X. J. Zhou. 2016. “A Diffusion Tensor Imaging Study on White Matter Abnormalities in Patients with Type 2 Diabetes Using Tract-Based Spatial Statistics.”](http://paperpile.com/b/ku2MlM/ypmV)[AJNR. American Journal of Neuroradiology](http://paperpile.com/b/ku2MlM/ypmV)[37 (8): 1462–69.](http://paperpile.com/b/ku2MlM/ypmV)

