from api.prokerala_api import get_choghadiya, get_chandra_bala, get_tara_bala
from datetime import datetime, timedelta

def get_good_muhurta_slots(start_date_str, end_date_str, coordinates, rasi, nakshatra):
    all_good_slots = []

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = timedelta(days=1)

    current_date = start_date

    while current_date <= end_date:
        date_iso = current_date.strftime("%Y-%m-%dT00:00:00+05:30")

        try:
            # Get all good Choghadiya
            coordinate_str = f"{coordinates['latitude']},{coordinates['longitude']}"
            choghadiya_data = get_choghadiya(coordinate_str, date_iso)
            choghadiyas = choghadiya_data.get("data", {}).get("muhurat", [])
            good_choghadiyas = [c for c in choghadiyas if c["type"] in {"Good", "Most Auspicious"}]

            # Get favorable Chandra Bala slots
            chandra_data = get_chandra_bala(coordinate_str, date_iso)
            favorable_chandra = [
                window for window in chandra_data.get("data", {}).get("chandra_bala", [])
                if any(r["name"].lower() == rasi.lower() for r in window.get("rasis", []))
            ]

            # Get favorable Tara Bala nakshatras
            tara_data = get_tara_bala(coordinate_str, date_iso)
            favorable_tara = [
                tb for tb in tara_data.get("data", {}).get("tara_bala", [])
                if any(n["name"].lower() == nakshatra.lower() for n in tb.get("nakshatras", []))
            ]

            # Overlap logic: check if Choghadiya slots lie within both Chandra & Tara windows
            for ch in good_choghadiyas:
                ch_start = datetime.fromisoformat(ch["start"])
                ch_end = datetime.fromisoformat(ch["end"])

                for cb in favorable_chandra:
                    cb_start = datetime.fromisoformat(cb["start"])
                    cb_end = datetime.fromisoformat(cb["end"])

                    if cb_end < ch_start or cb_start > ch_end:
                        continue  # No overlap

                    for tb in favorable_tara:
                        tb_start = datetime.fromisoformat(tb["start"])
                        tb_end = datetime.fromisoformat(tb["end"])

                        # Check full overlap
                        if tb_end < ch_start or tb_start > ch_end:
                            continue

                        start_time = max(ch_start, cb_start, tb_start)
                        end_time = min(ch_end, cb_end, tb_end)

                        if start_time < end_time:
                            all_good_slots.append({
                                "label": f"{ch['name']} Muhurat",
                                "start": start_time.strftime("%Y-%m-%d %H:%M"),
                                "end": end_time.strftime("%Y-%m-%d %H:%M"),
                                "vela": ch["name"],
                                "is_day": ch["is_day"]
                            })

        except Exception as e:
            print(f"⚠️ Failed to fetch data for {current_date.date()}: {e}")

        current_date += delta

    return all_good_slots
