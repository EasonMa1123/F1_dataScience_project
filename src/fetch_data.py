import os
import fastf1

fastf1.Cache.enable_cache('.gitignore/data/')


def load_driver_laps(year: int, grand_prix: str, session_type: str, driver1: str, driver2: str):
    """Loads session data and extracts the fastest laps for two drivers."""
    session = fastf1.get_session(int(year), grand_prix, session_type)
    session.load()

    lap_d1 = session.laps.pick_driver(driver1).pick_fastest()
    lap_d2 = session.laps.pick_driver(driver2).pick_fastest()

    if lap_d1.empty or lap_d2.empty:
        raise ValueError("One or both drivers do not have valid lap data for this session.")

    return session, lap_d1, lap_d2