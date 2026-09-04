import matplotlib.pyplot as plt

plt.style.use('dark_background')


def create_telemetry_figure(tel_d1, tel_d2, delta_time, ref_distance, meta, circuit_info=None):
    """Builds a 4-panel Matplotlib figure comparing lap telemetry with corner markers."""
    fig, (ax_delta, ax_speed, ax_throttle, ax_brake) = plt.subplots(
        4, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [1, 2, 1, 1]}
    )
    fig.patch.set_facecolor('#1e1e1e')

    # Panel 1: Delta Time
    ax_delta.plot(ref_distance, delta_time, color='white', linewidth=1.5)
    ax_delta.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax_delta.set_ylabel(f"Delta (s)\n<{meta['d1_code']} | {meta['d2_code']}>", fontsize=8)
    ax_delta.set_facecolor('#252526')

    # Panel 2: Speed Trace
    ax_speed.plot(tel_d1['Distance'], tel_d1['Speed'], color=meta['d1_color'], label=meta['d1_code'], linewidth=1.5)
    ax_speed.plot(tel_d2['Distance'], tel_d2['Speed'], color=meta['d2_color'], label=meta['d2_code'], linewidth=1.5)
    ax_speed.set_ylabel("Speed (km/h)", fontsize=8)
    ax_speed.legend(loc='upper right', fontsize=8)
    ax_speed.set_facecolor('#252526')

    # Panel 3: Throttle Input
    ax_throttle.plot(tel_d1['Distance'], tel_d1['Throttle'], color=meta['d1_color'], linewidth=1.2)
    ax_throttle.plot(tel_d2['Distance'], tel_d2['Throttle'], color=meta['d2_color'], linewidth=1.2)
    ax_throttle.set_ylabel("Throttle %", fontsize=8)
    ax_throttle.set_facecolor('#252526')

    # Panel 4: Braking Input
    ax_brake.plot(tel_d1['Distance'], tel_d1['Brake'], color=meta['d1_color'], linewidth=1.2)
    ax_brake.plot(tel_d2['Distance'], tel_d2['Brake'], color=meta['d2_color'], linewidth=1.2)
    ax_brake.set_ylabel("Brake", fontsize=8)
    ax_brake.set_xlabel("Distance (m)", fontsize=9)
    ax_brake.set_facecolor('#252526')

    axes = [ax_delta, ax_speed, ax_throttle, ax_brake]

    # --- ADD CORNER MARKERS ---
    if circuit_info is not None and hasattr(circuit_info, 'corners'):
        for _, corner in circuit_info.corners.iterrows():
            c_dist = corner['Distance']
            c_label = f"T{corner['Number']}{corner['Letter']}"

            # 1. Draw vertical reference line across all subplots
            for ax in axes:
                ax.axvline(x=c_dist, color='#444444', linestyle='--', linewidth=0.8, alpha=0.7)

            # 2. Annotate corner text above the top subplot (ax_delta)
            ax_delta.text(
                x=c_dist, y=ax_delta.get_ylim()[1], s=c_label,
                color='cyan', fontsize=7, fontweight='bold', ha='center', va='bottom'
            )

    for ax in axes:
        ax.tick_params(labelsize=8)
        ax.grid(True, color='#333333', linestyle=':', linewidth=0.5)

    fig.suptitle(f"{meta['d1_code']} vs {meta['d2_code']} Telemetry Comparison", color='white', fontsize=12)
    plt.tight_layout()
    return fig