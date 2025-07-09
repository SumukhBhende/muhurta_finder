import pandas as pd
from datetime import datetime, timedelta
from api.prokerala_api import get_choghadiya
from api.prokerala_api import get_daily_moon_data


# --------------------------
# Static Lists
# --------------------------
RAASHIS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
           "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
              "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
              "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
              "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
              "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

# --------------------------
# Chandrabalam Logic
# --------------------------
def is_chandrabalam_good(user_rashi, today_rashi):
    try:
        i = RAASHIS.index(user_rashi)
        j = RAASHIS.index(today_rashi)
        dist = (j - i) % 12 + 1
        return dist in [1, 3, 6, 7, 10, 11]
    except ValueError:
        return False

# --------------------------
# Tarabalam Logic
# --------------------------
def get_tarabalam(user_nakshatra, today_nakshatra):
    try:
        start = NAKSHATRAS.index(user_nakshatra)
        current = NAKSHATRAS.index(today_nakshatra)
        position = (current - start) % 27 + 1

        cycle = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyak", "Sadhana", "Naidhana", "Mitra", "Param Mitra"]
        tara = cycle[(position - 1) % 9]

        if tara in ["Sampat", "Param Mitra"]:
            quality = "Very Good"
        elif tara in ["Kshema", "Sadhana", "Mitra"]:
            quality = "Good"
        elif tara in ["Janma", "Vipat", "Pratyak"]:
            quality = "Not Good"
        else:
            quality = "Totally Bad"

        return tara, quality
    except ValueError:
        return None, "Unknown"

# --------------------------
# Main Engine
# --------------------------
def find_auspicious_muhurtas(user_rashi, user_nakshatra, days, latitude, longitude):
    today = datetime.now()
    rows = []

    for d in range(days):
        dt = today + timedelta(days=d)
        date_str = dt.strftime("%Y-%m-%d")

        moon_rashi, nak_today = get_daily_moon_data(date_str, latitude, longitude)
        if not moon_rashi or not nak_today:
            rows.append({
                "Date": date_str,
                "Start": "-",
                "End": "-",
                "Moon Rashi": "N/A",
                "Chandrabalam": "Error",
                "Nakshatra": "N/A",
                "Tarabalam": "Error",
                "Choghadiya": "API Error"
            })
            continue

        # Evaluate Chandrabalam and Tarabalam
        chandra_good = is_chandrabalam_good(user_rashi, moon_rashi)
        tara_type, tara_quality = get_tarabalam(user_nakshatra, nak_today)
        tara_good = tara_quality in ["Good", "Very Good"]

        if chandra_good and tara_good:
            choghadiya_slots = get_choghadiya(date_str, latitude, longitude)
            for slot in choghadiya_slots:
                rows.append({
                    "Date": date_str,
                    "Start": slot["start"],
                    "End": slot["end"],
                    "Moon Rashi": moon_rashi,
                    "Chandrabalam": "✅ Good",
                    "Nakshatra": nak_today,
                    "Tarabalam": f"{tara_type} ({tara_quality})",
                    "Choghadiya": slot["type"]
                })
        else:
            rows.append({
                "Date": date_str,
                "Start": "-",
                "End": "-",
                "Moon Rashi": moon_rashi,
                "Chandrabalam": "✅ Good" if chandra_good else "❌ Bad",
                "Nakshatra": nak_today,
                "Tarabalam": f"{tara_type} ({tara_quality})",
                "Choghadiya": "❌ Not auspicious"
            })

    return pd.DataFrame(rows)
