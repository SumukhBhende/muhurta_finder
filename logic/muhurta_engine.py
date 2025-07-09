from api.prokerala_api import get_panchang, get_detailed_panchang, get_choghadiya, get_chandra_bala, get_tara_bala
from datetime import datetime

def parse_time_range_overlap(range1, range2):
    start = max(range1["start"], range2["start"])
    end = min(range1["end"], range2["end"])
    if start < end:
        return {"start": start, "end": end}
    return None

def get_muhurtas(datetime_obj, lat, lon, user_rashi, user_nakshatra):
    cb_data = get_chandra_bala(datetime_obj, lat, lon)
    tb_data = get_tara_bala(datetime_obj, lat, lon)

    valid_cb_windows = []
    for period in cb_data["data"]["chandra_bala"]:
        rashi_names = [r["name"] for r in period["rasis"]]
        if user_rashi in rashi_names:
            valid_cb_windows.append({
                "start": datetime.fromisoformat(period["start"]),
                "end": datetime.fromisoformat(period["end"])
            })

    valid_tb_windows = []
    for period in tb_data["data"]["tara_bala"]:
        nakshatra_names = [n["name"] for n in period["nakshatras"]]
        if user_nakshatra in nakshatra_names and period["type"].lower() in ["good", "very good"]:
            valid_tb_windows.append({
                "start": datetime.fromisoformat(period["start"]),
                "end": datetime.fromisoformat(period["end"])
            })

    # Intersect chandra and tara time windows
    good_combined_windows = []
    for cb_win in valid_cb_windows:
        for tb_win in valid_tb_windows:
            overlap = parse_time_range_overlap(cb_win, tb_win)
            if overlap:
                good_combined_windows.append(overlap)

    # Fetch Choghadiya within those ranges
    choghadiya_data = get_choghadiya(datetime_obj, lat, lon)
    final_muhurta_list = []

    for muhurta in choghadiya_data["data"]["muhurat"]:
        muhurta_start = datetime.fromisoformat(muhurta["start"])
        muhurta_end = datetime.fromisoformat(muhurta["end"])
        if muhurta["type"] not in ["Good", "Most Auspicious"]:
            continue

        for window in good_combined_windows:
            if muhurta_start >= window["start"] and muhurta_end <= window["end"]:
                final_muhurta_list.append({
                    "name": muhurta["name"],
                    "start": muhurta_start.strftime("%I:%M %p"),
                    "end": muhurta_end.strftime("%I:%M %p"),
                    "type": muhurta["type"]
                })
    return final_muhurta_list
