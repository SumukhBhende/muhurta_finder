from datetime import datetime, timedelta
from api.prokerala_api import get_chandra_balam, get_tara_balam, get_choghadiya


def parse_iso(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None


def get_good_muhurta_slots(start_date_str, end_date_str, coordinates, rasi, nakshatra):
    """
    Returns a list of muhurta periods where Chandra Balam, Tara Balam, and Choghadiya are all favorable.

    Parameters:
        - start_date_str (str): format "YYYY-MM-DD"
        - end_date_str (str): format "YYYY-MM-DD"
        - coordinates (dict): {"latitude": float, "longitude": float}
        - rasi (str): User's moon sign
        - nakshatra (str): User's birth star

    Returns:
        - List of dicts with start, end, vela, label, is_day
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    current_date = start_date
    results = []

    while current_date <= end_date:
        datetime_str = current_date.strftime("%Y-%m-%dT00:00:00")

        # Fetch data
        chandra = get_chandra_balam(datetime_str, coordinates, rasi)
        tara = get_tara_balam(datetime_str, coordinates, nakshatra)
        choghadiya_periods = get_choghadiya(datetime_str, coordinates)

        if not (chandra and chandra.get("is_favorable") and
                tara and tara.get("is_favorable")):
            current_date += timedelta(days=1)
            continue

        chandra_start = parse_iso(datetime_str)
        chandra_end = parse_iso(chandra.get("until"))
        tara_start = parse_iso(datetime_str)
        tara_end = parse_iso(tara.get("valid_until"))

        for muhurta in choghadiya_periods:
            m_start = parse_iso(muhurta["start"])
            m_end = parse_iso(muhurta["end"])

            if not all([m_start, m_end, chandra_start, chandra_end, tara_start, tara_end]):
                continue

            # Ensure Choghadiya fits within both Chandra & Tara Balam windows
            if chandra_start <= m_start <= chandra_end and \
               tara_start <= m_start <= tara_end and \
               m_end <= chandra_end and m_end <= tara_end:
                results.append({
                    "start": muhurta["start"],
                    "end": muhurta["end"],
                    "vela": muhurta["vela"],
                    "is_day": muhurta["is_day"],
                    "label": muhurta["name"]
                })

        current_date += timedelta(days=1)

    return results
