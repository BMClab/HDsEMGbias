# Neuromuscular System Model Parameters

This table contains all parameters used in the diabetes neuropathy neuromuscular system model, including their units, descriptions, and default values.

## Model Parameters Table

| Parameter | Units | Description | Default Value | Parameter Type |
|-----------|-------|-------------|---------------|----------------|
| **Motoneuron Morphology Parameters** |
| `diameter_soma_min` | μm | Minimum diameter of motoneuron soma | 77.5 | Morphological |
| `diameter_soma_max` | μm | Maximum diameter of motoneuron soma | 82.5 | Morphological |
| `diameter_dend_min` | μm | Minimum diameter of dendrites | 41.5 | Morphological |
| `diameter_dend_max` | μm | Maximum diameter of dendrites | 62.5 | Morphological |
| `y_min` | μm | Minimum y-coordinate for neuron positioning | 18.0 | Morphological |
| `y_max` | μm | Maximum y-coordinate for neuron positioning | 36.0 | Morphological |
| `x_min` | μm | Minimum x-coordinate for dendrite positioning | -5500 | Morphological |
| `x_max` | μm | Maximum x-coordinate for dendrite positioning | -6789 | Morphological |
| **Motoneuron Electrical Properties** |
| `vt_min` | mV | Minimum voltage threshold for smallest motoneurons | 12.35 | Electrical |
| `vt_max` | mV | Maximum voltage threshold for largest motoneurons | 20.9 | Electrical |
| `kf_cond_min` | mS/cm² | Minimum fast potassium conductance density | 4 | Electrical |
| `kf_cond_max` | mS/cm² | Maximum fast potassium conductance density | 0.5 | Electrical |
| `cm_soma` | μF/cm² | Membrane capacitance (soma) | 1 | Electrical |
| `cm_dend` | μF/cm² | Membrane capacitance (dendrites) | 1 | Electrical |
| `Ra` | Ω·mm | Axial resistance | 0.070 | Electrical |
| **Ion Channel Parameters** |
| `ena` | mV | Sodium reversal potential | 50 | Electrical |
| `eks` | mV | Slow potassium reversal potential | -80 | Electrical |
| `ekf` | mV | Fast potassium reversal potential | -80 | Electrical |
| `el` | mV | Leak reversal potential | -70 | Electrical |
| `gna` | mS/cm² | Sodium conductance density | 30 | Electrical |
| `gks` | mS/cm² | Slow potassium conductance density | 0.1 | Electrical |
| `gl_soma` | mS/cm² | Leak conductance density (soma) | 7e-4 | Electrical |
| `gl_dend` | mS/cm² | Leak conductance density (dendrites) | 7e-4 | Electrical |
| **Sodium Channel Kinetics** |
| `alpha_m_coeff1` | - | Sodium m-gate activation coefficient 1 | -0.32 | Electrical |
| `alpha_m_offset1` | mV | Sodium m-gate activation voltage offset 1 | -13 | Electrical |
| `alpha_m_slope1` | mV | Sodium m-gate activation slope 1 | 4 | Electrical |
| `beta_m_coeff1` | - | Sodium m-gate inactivation coefficient 1 | 0.28 | Electrical |
| `beta_m_offset1` | mV | Sodium m-gate inactivation voltage offset 1 | -40 | Electrical |
| `beta_m_slope1` | mV | Sodium m-gate inactivation slope 1 | 5 | Electrical |
| `alpha_h_coeff` | ms⁻¹ | Sodium h-gate activation coefficient | 0.128 | Electrical |
| `alpha_h_offset` | mV | Sodium h-gate activation voltage offset | -17 | Electrical |
| `alpha_h_slope` | mV | Sodium h-gate activation slope | 18 | Electrical |
| `beta_h_coeff` | ms⁻¹ | Sodium h-gate inactivation coefficient | 4 | Electrical |
| `beta_h_offset` | mV | Sodium h-gate inactivation voltage offset | -40 | Electrical |
| `beta_h_slope` | mV | Sodium h-gate inactivation slope | 5 | Electrical |
| `h_rate_factor` | - | Sodium h-gate rate scaling factor | 0.04 | Electrical |
| **Fast Potassium Channel Kinetics** |
| `alpha_n_coeff` | - | Fast K+ n-gate activation coefficient | -0.032 | Electrical |
| `alpha_n_offset` | mV | Fast K+ n-gate activation voltage offset | -15 | Electrical |
| `alpha_n_slope` | mV | Fast K+ n-gate activation slope | 5 | Electrical |
| `beta_n_coeff` | ms⁻¹ | Fast K+ n-gate inactivation coefficient | 0.5 | Electrical |
| `beta_n_offset` | mV | Fast K+ n-gate inactivation voltage offset | -10 | Electrical |
| `beta_n_slope` | mV | Fast K+ n-gate inactivation slope | 40 | Electrical |
| `n_rate_factor` | - | Fast K+ n-gate rate scaling factor | 0.04 | Electrical |
| **Slow Potassium Channel Kinetics** |
| `ks_v_half` | mV | Slow K+ half-activation voltage | -35 | Electrical |
| `ks_v_slope` | mV | Slow K+ activation voltage slope | 10 | Electrical |
| `tau_max_p` | ms | Maximum slow K+ time constant | 4 | Electrical |
| `ks_tau_coeff1` | - | Slow K+ tau coefficient 1 | 3.3 | Electrical |
| `ks_tau_slope1` | mV | Slow K+ tau slope 1 | 20 | Electrical |
| `ks_tau_slope2` | mV | Slow K+ tau slope 2 | 20 | Electrical |
| **Ion Channel State Variables** |
| `m_initial` | - | Sodium m-gate initial value | 0 | Electrical |
| `h_initial` | - | Sodium h-gate initial value | 1 | Electrical |
| `n_initial` | - | Fast K+ n-gate initial value | 0 | Electrical |
| `p_initial` | - | Slow K+ p-gate initial value | pinf | Electrical |
| **Channel Exponents** |
| `na_m_exp` | - | Sodium channel m-gate exponent | 3 | Electrical |
| `na_h_exp` | - | Sodium channel h-gate exponent | 1 | Electrical |
| `kf_n_exp` | - | Fast K+ channel n-gate exponent | 4 | Electrical |
| `ks_p_exp` | - | Slow K+ channel p-gate exponent | 2 | Electrical |
| **Muscle Unit Parameters** |
| `Fmin` | N | Minimum force of smallest muscle unit | 0.04 | Mechanical |
| `Fmax` | N | Maximum force of largest muscle unit | 4 | Mechanical |
| `Tcmin` | ms | Minimum contraction time of fastest muscle unit | 110 | Mechanical |
| `Tcmax` | ms | Maximum contraction time of slowest muscle unit | 25 | Mechanical |
| `vel_min` | m/s | Minimum conduction velocity | 44 | Physiological |
| `vel_max` | m/s | Maximum conduction velocity | 53 | Physiological |
| `Umax` | M⁻¹·ms⁻¹ | Maximum calcium uptake rate | 2000 | Biochemical |
| **Calcium Dynamics Parameters** |
| `k1` | M⁻¹·ms⁻¹ | Calcium-calsequestrin binding rate constant | 3000 | Biochemical |
| `k2` | ms⁻¹ | Calcium-calsequestrin unbinding rate constant | 3 | Biochemical |
| `k3` | M⁻¹·ms⁻¹ | Calcium-buffer binding rate constant | 400 | Biochemical |
| `k4` | ms⁻¹ | Calcium-buffer unbinding rate constant | 1 | Biochemical |
| `k5i` | M⁻¹·ms⁻¹ | Calcium-troponin binding rate constant (initial) | 4e5 | Biochemical |
| `k6i` | ms⁻¹ | Calcium-troponin unbinding rate constant (initial) | 150 | Biochemical |
| `k` | M⁻¹ | Calcium uptake binding constant | 850 | Biochemical |
| `Rmax` | ms⁻¹ | Maximum calcium release rate | 10 | Biochemical |
| `tau1` | ms | Calcium release time constant 1 | 1 | Biochemical |
| `tau2` | ms | Calcium release time constant 2 | 13 | Biochemical |
| `phi1` | - | Calcium release probability factor 1 | 0.004 | Biochemical |
| `phi2` | - | Calcium release probability factor 2 | 0.98 | Biochemical |
| `phi3` | - | Calcium release probability factor 3 | 0.0002 | Biochemical |
| `phi4` | - | Calcium release probability factor 4 | 0.999 | Biochemical |
| `SF_AM` | - | Actomyosin scaling factor | 5 | Biochemical |
| `CS0` | M | Initial calsequestrin concentration | 0.03 | Biochemical |
| `B0` | M | Initial buffer concentration | 0.00043 | Biochemical |
| `T0` | M | Initial troponin concentration | 0.00007 | Biochemical |
| **Calcium State Variables (Initial Values)** |
| `CaSR_initial` | M | Initial sarcoplasmic reticulum calcium | 0.0025 | Biochemical |
| `CaSRCS_initial` | M | Initial calsequestrin-bound calcium | 0.0 | Biochemical |
| `Ca_initial` | M | Initial free calcium concentration | 1e-10 | Biochemical |
| `CaT_initial` | M | Initial troponin-bound calcium | 0.0 | Biochemical |
| `CaB_initial` | M | Initial buffer-bound calcium | 0.0 | Biochemical |
| `AM_initial` | - | Initial actomyosin fraction | 0.0 | Biochemical |
| **Muscle Activation Parameters** |
| `c1i` | - | Activation parameter c1 initial value | 0.154 | Biochemical |
| `c1n1` | - | Activation parameter c1 coefficient 1 | 0.01 | Biochemical |
| `c1n2` | - | Activation parameter c1 coefficient 2 | 0.15 | Biochemical |
| `c1n3` | - | Activation parameter c1 coefficient 3 | 0.01 | Biochemical |
| `tauc1` | ms | Activation time constant c1 | 85 | Biochemical |
| `c2i` | - | Activation parameter c2 initial value | 0.11 | Biochemical |
| `c2n1` | - | Activation parameter c2 coefficient 1 | -0.0315 | Biochemical |
| `c2n2` | - | Activation parameter c2 coefficient 2 | 0.27 | Biochemical |
| `c2n3` | - | Activation parameter c2 coefficient 3 | 0.015 | Biochemical |
| `tauc2` | ms | Activation time constant c2 | 70 | Biochemical |
| `c3` | - | Activation parameter c3 | 54.717 | Biochemical |
| `c4` | - | Activation parameter c4 | -18.847 | Biochemical |
| `c5` | - | Activation parameter c5 | 3.905 | Biochemical |
| `alpha` | - | Muscle activation exponent | 2 | Biochemical |
| **System Parameters** |
| `mn_number` | - | Number of motoneurons in the pool | 250 | System |
| `CST_number` | - | Number of corticospinal tract neurons | 400 | System |
| `MVC` | N | Maximum voluntary contraction force | 300 | System |
| `CV` | - | Coefficient of variation for parameter noise | 0.01 | System |
| `connection_prob` | - | Synaptic connection probability | 0.1 | System |
| **Control Parameters** |
| `gamma_order` | - | Shape parameter for gamma distribution (feedback) | 16 | Control |
| `gamma_order_feedforward` | - | Shape parameter for gamma distribution (feedforward) | 8 | Control |
| `feedforward` | Hz | Feedforward drive strength | 0 | Control |
| `feedback_strength` | - | Feedback control strength (0-1) | 1 | Control |
| `delay` | ms | Feedback delay | 60 | Control |
| `Kp` | - | Proportional gain for PID controller | 0.07 | Control |
| `Ki` | - | Integral gain for PID controller | 0.007 | Control |
| **Simulation Parameters** |
| `Tf` | ms | Total simulation time | 10000 | Simulation |
| `timestep` | ms | Integration time step | 0.05 | Simulation |
| `force_mvc` | - | Target force as fraction of MVC | 0.2 | Simulation |
| `trial` | - | Random seed modifier for trial | 1 | Simulation |
| `condition` | - | Experimental condition ('normal', 'low_affected', 'severe') | 'normal' | Simulation |
| **Synaptic Parameters** |
| `syn_weight` | μS | Synaptic weight | 0.6 | Synaptic |
| `syn_delay` | ms | Synaptic delay | 0.2 | Synaptic |
| `e_syn` | mV | Synaptic reversal potential | 0 | Synaptic |
| `tau_syn` | ms | Synaptic time constant | 0.6 | Synaptic |

## Condition-Specific Parameter Modifications

### Normal Condition
All parameters use their default values as listed above.

### Low Affected Condition (Mild Diabetes Neuropathy)
- `Fmin`: 0.04/1.2 = 0.033 N (reduced muscle force)
- `Fmax`: 4/1.2 = 3.33 N (reduced muscle force)
- `Tcmin`: 110×1.2 = 132 ms (slower contraction)
- `Tcmax`: 25×1.2 = 30 ms (slower contraction)
- `vel_min`: 44×0.92 = 40.5 m/s (reduced conduction velocity)
- `vel_max`: 53×0.92 = 48.8 m/s (reduced conduction velocity)
- `CST_number`: 300 (reduced cortical input)

### Severe Condition (Severe Diabetes Neuropathy)
- `Fmin`: 0.04/1.4 = 0.029 N (severely reduced muscle force)
- `Fmax`: 4/1.4 = 2.86 N (severely reduced muscle force)
- `Tcmin`: 110×1.4 = 154 ms (much slower contraction)
- `Tcmax`: 25×1.4 = 35 ms (much slower contraction)
- `vel_min`: 44×0.85 = 37.4 m/s (severely reduced conduction velocity)
- `vel_max`: 53×0.85 = 45.1 m/s (severely reduced conduction velocity)
- `CST_number`: 200 (severely reduced cortical input)

## Parameter Categories

1. **Morphological**: Physical dimensions and spatial organization of neurons
2. **Electrical**: Membrane properties and ion channel characteristics
3. **Mechanical**: Muscle force generation and contraction properties
4. **Physiological**: Biological timing and conduction properties
5. **Biochemical**: Calcium dynamics and metabolic processes
6. **System**: Population-level organization parameters
7. **Control**: Feedback and feedforward control system parameters
8. **Simulation**: Computational and experimental setup parameters
9. **Synaptic**: Inter-neuronal communication parameters

## Notes

- Parameters with `_min` and `_max` suffixes define ranges for exponential distributions across the motoneuron pool
- The model implements size-ordered recruitment following Henneman's size principle
- Diabetes neuropathy effects are modeled through systematic parameter modifications that reflect:
  - Reduced muscle force capacity
  - Slower muscle contraction times
  - Reduced nerve conduction velocities
  - Decreased cortical drive
- All random variations are controlled by the `CV` parameter and seeded for reproducibility
