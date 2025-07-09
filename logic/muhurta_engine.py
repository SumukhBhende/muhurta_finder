from datetime import datetime, timedelta
from api.prokerala_api import (
    get_panchang,
    get_detailed_panchang,
    get_choghadiya,
    get_chandra_bala,
    get_tara_bala,
)

# Utility function: Convert string to datetime
def parse_datetime(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# Utility: Check if time ranges overlap
def overlaps(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

# Main Muhurta Engine
def get_muhurtas(date_str, time_str, latitude, longitude, rashi, nakshatra):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    selected_datetime = parse_datetime(date_str, time_str)

    print(f"\n📅 Input Date & Time: {selected_datetime}")
    print(f"📍 Location: lat={latitude}, lon={longitude}")
    print(f"🌙 Rashi: {rashi} | Nakshatra: {nakshatra}")

    # STEP 1: Get Chandra Balam
    chandra_data = get_chandra_bala(date_obj)
    chandra_windows = []
    for entry in chandra_data["data"]["chandra_bala"]:
        rasis = [r["name"] for r in entry["rasis"]]
        if rashi in rasis:
            start = datetime.fromisoformat(entry["start"])
            end = datetime.fromisoformat(entry["end"])
            chandra_windows.append((start, end))
    if not chandra_windows:
        return {"status": "No good Chandra Balam window found."}

    # STEP 2: Get Tara Balam
    tara_data = get_tara_bala(date_obj)
    tara_windows = []
    for entry in tara_data["data"]["tara_bala"]:
        nakshatras = [n["name"] for n in entry["nakshatras"]]
        if nakshatra in nakshatras and entry["type"].lower() in ["good", "very good"]:
            start = datetime.fromisoformat(entry["start"])
            end = datetime.fromisoformat(entry["end"])
            tara_windows.append((start, end))
    if not tara_windows:
        return {"status": "No good Tara Balam window found."}

    # STEP 3: Find overlapping windows of Chandra + Tara
    combined_windows = []
    for c_start, c_end in chandra_windows:
        for t_start, t_end in tara_windows:
            if overlaps(c_start, c_end, t_start, t_end):
                start = max(c_start, t_start)
                end = min(c_end, t_end)
                combined_windows.append((start, end))
    if not combined_windows:
        return {"status": "No overlapping Chandra Balam + Tara Balam window."}

    print(f"✅ Found {len(combined_windows)} overlapping window(s)")

    # STEP 4: Filter Choghadiya Muhurtas in these windows
    choghadiya_data = get_choghadiya(date_obj, latitude, longitude)
    all_muhurtas = choghadiya_data["data"]["muhurat"]

    # Only allow "Good" or "Most Auspicious"
    good_types = ["Good", "Most Auspicious"]
    final_muhurtas = []
    for muhurta in all_muhurtas:
        m_type = muhurta["type"]
        if m_type not in good_types:
            continue
        start = datetime.fromisoformat(muhurta["start"])
        end = datetime.fromisoformat(muhurta["end"])

        for win_start, win_end in combined_windows:
            if overlaps(start, end, win_start, win_end):
                final_muhurtas.append({
                    "name": muhurta["name"],
                    "type": muhurta["type"],
                    "start": start,
                    "end": end,
                    "vela": muhurta.get("vela"),
                })
                break

    if not final_muhurtas:
        return {"status": "No good Choghadiya Muhurta within the good window."}

    return {
        "status": "Success",
        "total": len(final_muhurtas),
        "muhurtas": final_muhurtas,
        "combined_window": combined_windows,
    }
