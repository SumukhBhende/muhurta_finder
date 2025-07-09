from api.prokerala_api import (
    get_chandra_bala,
    get_tara_bala,
    get_choghadiya,
    get_detailed_panchang,
)
from datetime import datetime
from dateutil import parser


def parse_iso(dt_str):
    return parser.isoparse(dt_str)


def rashi_in_chandra_bala(rashi_name, chandra_bala_data):
    for period in chandra_bala_data["data"]["chandra_bala"]:
        for r in period["rasis"]:
            if r["name"].lower() == rashi_name.lower():
                return {
                    "start": parse_iso(period["start"]),
                    "end": parse_iso(period["end"]),
                }
    return None


def nakshatra_in_tara_bala(nakshatra_name, tara_bala_data):
    for period in tara_bala_data["data"]["tara_bala"]:
        for n in period["nakshatras"]:
            if n["name"].lower() == nakshatra_name.lower():
                return {
                    "start": parse_iso(period["start"]),
                    "end": parse_iso(period["end"]),
                }
    return None


def overlap_time(period1, period2):
    if not period1 or not period2:
        return None
    start = max(period1["start"], period2["start"])
    end = min(period1["end"], period2["end"])
    if start >= end:
        return None
    return {"start": start, "end": end}


def filter_choghadiya(choghadiya_data, overlap):
    good_muhurtas = []
    for muhurta in choghadiya_data["data"]["muhurat"]:
        m_start = parse_iso(muhurta["start"])
        m_end = parse_iso(muhurta["end"])

        if m_end <= overlap["start"] or m_start >= overlap["end"]:
            continue  # Outside the overlap

        if muhurta["type"] in ["Good", "Most Auspicious"]:
            good_muhurtas.append({
                "start": m_start.strftime("%Y-%m-%d %H:%M"),
                "end": m_end.strftime("%Y-%m-%d %H:%M"),
                "type": muhurta["type"],
                "choghadiya": muhurta["name"]
            })
    return good_muhurtas


def get_muhurtas(current_location, birth_datetime=None, birth_location=None, rashi=None, nakshatra=None):
    today = datetime.now()
    latitude = current_location["latitude"]
    longitude = current_location["longitude"]

    # If birth details provided, compute Rashi/Nakshatra
    if birth_datetime and birth_location:
        detailed = get_detailed_panchang(
            birth_datetime, birth_location["latitude"], birth_location["longitude"]
        )
        rashi = detailed["data"]["nakshatra"]["rasi"]["name"]
        nakshatra = detailed["data"]["nakshatra"]["name"]

    # Check if Rashi and Nakshatra are available
    if not rashi or not nakshatra:
        return None

    # Step 1: Chandra Bala
    chandra_data = get_chandra_bala(today, latitude, longitude)
    chandra_window = rashi_in_chandra_bala(rashi, chandra_data)
    if not chandra_window:
        return []

    # Step 2: Tara Bala
    tara_data = get_tara_bala(today, latitude, longitude)
    tara_window = nakshatra_in_tara_bala(nakshatra, tara_data)
    if not tara_window:
        return []

    # Step 3: Find overlapping time window
    overlap = overlap_time(chandra_window, tara_window)
    if not overlap:
        return []

    # Step 4: Get Choghadiya
    choghadiya_data = get_choghadiya(today, latitude, longitude)
    filtered_muhurtas = filter_choghadiya(choghadiya_data, overlap)
    return filtered_muhurtas
