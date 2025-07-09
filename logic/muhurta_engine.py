from datetime import datetime, timedelta
from api.prokerala_api import (
    get_choghadiya,
    get_chandra_balam,
    get_tara_balam,
    get_kundali,
)


def parse_iso_datetime(dt_str):
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def get_favorable_muhurtas(date_str, location):
    """
    Main function to determine favorable muhurta blocks based on:
    - Choghadiya
    - Chandra Balam
    - Tara Balam
    """
    # Build datetime string with time (midnight start)
    date_start = f"{date_str}T00:00:00+00:00"

    # Step 1: Get user's nakshatra and rasi
    kundli = get_kundali(date_start, location)
    if not kundli:
        raise ValueError("Failed to fetch Kundli")

    nakshatra = kundli["nakshatra"]
    rasi = kundli["chandra_rasi"]

    # Step 2: Fetch individual scores
    choghadiya_periods = get_choghadiya(date_start, location)
    chandra = get_chandra_balam(date_start, location, rasi)
    tara = get_tara_balam(date_start, location, nakshatra)

    final_muhurtas = []

    if not chandra["is_favorable"] or not tara["is_favorable"]:
        return []  # No overlapping good period

    chandra_end = parse_iso_datetime(chandra["until"])
    tara_end = parse_iso_datetime(tara["valid_until"])

    # Final check range is the intersection window of both
    favorable_window_end = min(chandra_end, tara_end)

    # Step 3: Filter choghadiya within favorable windows
    for muhurta in choghadiya_periods:
        muhurta_start = parse_iso_datetime(muhurta["start"])
        muhurta_end = parse_iso_datetime(muhurta["end"])

        if muhurta_start < favorable_window_end:
            end_time = min(muhurta_end, favorable_window_end)

            final_muhurtas.append({
                "start": muhurta_start.isoformat(),
                "end": end_time.isoformat(),
                "name": muhurta["name"],
                "vela": muhurta["vela"],
                "is_day": muhurta["is_day"]
            })

    return final_muhurtas
