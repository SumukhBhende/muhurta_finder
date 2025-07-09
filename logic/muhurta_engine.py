from datetime import datetime
from api.prokerala_api import (
    get_kundli_data,
    get_chandra_balam,
    get_tara_balam,
    get_choghadiya,
    get_rashi_nakshatra
)

def parse_time_range_overlap(range1, range2):
    start = max(range1["start"], range2["start"])
    end = min(range1["end"], range2["end"])
    if start < end:
        return {"start": start, "end": end}
    return None

def get_muhurtas(current_location, birth_datetime=None, birth_location=None, rashi=None, nakshatra=None):
    now = datetime.utcnow().replace(second=0, microsecond=0)
    datetime_str = now.isoformat() + "+00:00"

    lat = current_location["latitude"]
    lon = current_location["longitude"]

    # If birth datetime/location is given, derive rashi/nakshatra
    if birth_datetime and birth_location:
        birth_str = birth_datetime.isoformat() + "+00:00"
        kundli = get_kundli_data(birth_str, birth_location)
        rashi = kundli["data"]["moon"]["rasi"]["name"]
        nakshatra = kundli["data"]["moon"]["nakshatra"]["name"]

    if not rashi or not nakshatra:
        return []

    # 🌙 Chandra Balam
    cb_data = get_chandra_balam(datetime_str, current_location, rashi)
    valid_cb_windows = []
    for period in cb_data["data"]["chandra_bala"]:
        rashi_names = [r["name"] for r in period["rasis"]]
        if rashi in rashi_names:
            valid_cb_windows.append({
                "start": datetime.fromisoformat(period["start"]),
                "end": datetime.fromisoformat(period["end"])
            })

    # ✨ Tara Balam
    tb_data = get_tara_balam(datetime_str, current_location, nakshatra) 
    valid_tb_windows = []
    for period in tb_data["data"]["tara_bala"]:
        nakshatra_names = [n["name"] for n in period["nakshatras"]]
        if nakshatra in nakshatra_names and period["type"].lower() in ["good", "very good"]:
            valid_tb_windows.append({
                "start": datetime.fromisoformat(period["start"]),
                "end": datetime.fromisoformat(period["end"])
            })

    # ⏳ Intersect time windows
    good_combined_windows = []
    for cb_win in valid_cb_windows:
        for tb_win in valid_tb_windows:
            overlap = parse_time_range_overlap(cb_win, tb_win)
            if overlap:
                good_combined_windows.append(overlap)

    if not good_combined_windows:
        return []

    # 🕰️ Choghadiya
    choghadiya_data = get_choghadiya(datetime_str, current_location)
    choghadiya_list = choghadiya_data.get("data", {}).get("choghadiya", [])

    final_muhurta_list = []

    for muhurta in choghadiya_list:
        start_dt = datetime.fromisoformat(muhurta["start"])
        end_dt = datetime.fromisoformat(muhurta["end"])

        if muhurta["muhurta"]["name"] not in ["Shubh", "Labh", "Amrit", "Chal"]:
            continue

        for win in good_combined_windows:
            if start_dt >= win["start"] and end_dt <= win["end"]:
                final_muhurta_list.append({
                    "start": start_dt.strftime("%I:%M %p"),
                    "end": end_dt.strftime("%I:%M %p"),
                    "type": "Auspicious",
                    "choghadiya": muhurta["muhurta"]["name"]
                })

    return final_muhurta_list
