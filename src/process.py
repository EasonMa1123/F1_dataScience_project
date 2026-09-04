import numpy as np
import pandas as pd
import fastf1


def process_telemetry_comparison(lap_d1, lap_d2):
    """Processes telemetry and calculates spatial delta time between two drivers."""
    tel_d1 = lap_d1.get_telemetry().add_distance()
    tel_d2 = lap_d2.get_telemetry().add_distance()

    d1_code = lap_d1['Driver']
    d2_code = lap_d2['Driver']
    
    # Safely retrieve team colors
    color_d1 = get_safe_team_color(lap_d1)
    color_d2 = get_safe_team_color(lap_d2)

    delta_time, ref_distance = calculate_delta_time(tel_d1, tel_d2)

    meta = {
        'd1_code': d1_code,
        'd2_code': d2_code,
        'd1_color': color_d1,
        'd2_color': color_d2,
        'd1_time': lap_d1['LapTime'],
        'd2_time': lap_d2['LapTime']
    }

    return tel_d1, tel_d2, delta_time, ref_distance, meta

def calculate_delta_time(tel_d1, tel_d2):
    """Interpolates time profiles over common distance points to derive lap time delta."""
    ref_distance = np.linspace(0, max(tel_d1['Distance'].max(), tel_d2['Distance'].max()), 1000)

    time_d1 = np.interp(ref_distance, tel_d1['Distance'], tel_d1['Time'].dt.total_seconds())
    time_d2 = np.interp(ref_distance, tel_d2['Distance'], tel_d2['Time'].dt.total_seconds())

    # Positive value indicates Driver 1 is slower (behind) than Driver 2
    delta_time = time_d1 - time_d2
    return delta_time, ref_distance



def get_safe_team_color(lap):
    """Safely extracts team color with '#' prefix and default fallbacks."""
    # Method 1: Using FastF1's built-in color helper
    try:
        color = fastf1.plotting.get_team_color(lap['TeamName'], session=lap.session)
        if color:
            return color
    except Exception:
        pass

    # Method 2: Fallback to lap['TeamColor'] attribute
    raw_color = lap.get('TeamColor') if hasattr(lap, 'get') else None
    if pd.notna(raw_color) and str(raw_color).strip():
        raw_str = str(raw_color).strip()
        return f"#{raw_str}" if not raw_str.startswith('#') else raw_str

    # Default fallback color if no team color is found
    return '#00FFFF'