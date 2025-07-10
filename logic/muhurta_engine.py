from datetime import datetime, timedelta
from api.prokerala_api import get_choghadiya, get_chandra_bala, get_tara_bala
from utils.digipin_utils import get_coordinates_from_digipin

# ------------------------------------
# ⏳ Utility: ISO 8601 Date Generator
# ------------------------------------
def generate_dates(start_date_str, end_date_str):
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")
    date_list = []
    while start <= end:
        date_list.append(start.strftime("%Y-%m-%dT00:00:00+05:30"))
        start += timedelta(days=1)
    return date_list

# ------------------------------------
# 🌙 Main Muhurta Logic
# ------------------------------------
def get_good_muhurta_slots(start_date_str, end_date_str, coordinates, rasi, nakshatra):
    coords_str = f"{coordinates['latitude']},{coordinates['longitude']}"
    date_list = generate_dates(start_date_str, end_date_str)

    good_slots = []

    for date_iso in date_list:
        # 1. Chandra Bala (for rasi)
        cb_data = get_chandra_bala(coords_str, date_iso)
        cb_windows = [
            {"start": slot["start"], "end": slot["end"]}
            for slot in cb_data["data"]["chandra_bala"]
            if any(r["name"].lower() == rasi.lower() for r in slot["rasis"])
        ]

        if not cb_windows:
            continue  # No favorable rashi windows that day

        # 2. Tara Bala (for nakshatra)
        tb_data = get_tara_bala(coords_str, date_iso)
        tb_windows = [
            {"start": block["start"], "end": block["end"]}
            for block in tb_data["data"]["tara_bala"]
            if any(n["name"].lower() == nakshatra.lower() for n in block["nakshatras"])
        ]

        if not tb_windows:
            continue  # No favorable nakshatra windows that day

        # 3. Compute overlap between CB and TB
        for cb in cb_windows:
            cb_start = datetime.fromisoformat(cb["start"])
            cb_end = datetime.fromisoformat(cb["end"])

            for tb in tb_windows:
                tb_start = datetime.fromisoformat(tb["start"])
                tb_end = datetime.fromisoformat(tb["end"])

                # Overlap logic
                start = max(cb_start, tb_start)
                end = min(cb_end, tb_end)

                if start < end:
                    # 4. Fetch Choghadiya
                    ch_data = get_choghadiya(coords_str, date_iso)
                    choghadiya_blocks = ch_data["data"]["muhurat"]
                    for ch in choghadiya_blocks:
                        ch_start = datetime.fromisoformat(ch["start"])
                        ch_end = datetime.fromisoformat(ch["end"])

                        if ch["type"] in {"Good", "Most Auspicious"} and start <= ch_start and ch_end <= end:
                            good_slots.append({
                                "label": ch["name"],
                                "start": ch["start"],
                                "end": ch["end"],
                                "vela": ch["type"],
                                "is_day": ch["is_day"]
                            })

    return good_slots
