def plot_force_with_plateau_cv(file_path, ref_signal, ramp_defs, force_level, output_dir, FSAMP=10240):
    """
    Plota o sinal de força com destaque para os plateaus e mostra o CV de cada plateau.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    time_ref = np.arange(len(ref_signal)) / FSAMP
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time_ref, ref_signal, 'k-', label='Force (% MVC)')

    plateau_colors = ['g', 'b', 'r', 'c', 'm', 'y']
    for plateau_idx, (start_idx, stop_idx) in ramp_defs.items():
        start_time = start_idx / FSAMP
        stop_time = stop_idx / FSAMP
        color = plateau_colors[plateau_idx % len(plateau_colors)]
        plateau_signal = ref_signal[start_idx:stop_idx+1]
        if len(plateau_signal) > 1:
            mean = np.mean(plateau_signal)
            std = np.std(plateau_signal)
            cv = std / mean if mean != 0 else np.nan
        else:
            cv = np.nan
        ax.axvspan(start_time, stop_time, color=color, alpha=0.2)
        ax.text((start_time+stop_time)/2, np.max(ref_signal)*0.95, f'CV: {cv:.3f}',
                color=color, ha='center', va='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        ax.axvline(x=start_time, color=color, linestyle='--', alpha=0.7)
        ax.axvline(x=stop_time, color=color, linestyle=':', alpha=0.7)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Force (% MVC)')
    ax.set_title(f'Force Signal with Plateau CVs - {file_path.name} ({force_level}% MVC)')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.tight_layout()
    output_file = output_dir / f"{file_path.stem}_force_plateau_CV.png"
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print(f"Saved force+CV plot to {output_file}")