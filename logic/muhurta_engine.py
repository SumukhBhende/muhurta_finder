import pandas as pd
from datetime import datetime, timedelta

# List of Rashi (Moon Signs)
RAASHIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# List of 27 Nakshatras
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# -----------------------------
# Chandrabalam Logic
# -----------------------------

def is_chandrabalam_good(user_rashi, today_rashi):
    """Returns True if today's Moon sign is favorable from user's Moon sign"""
    try:
        i = RAASHIS.index(user_rashi)
        j = RAASHIS.index(today_rashi)
        distance = (j - i) % 12 + 1  # 1-based distance
        return distance in [1, 3, 6, 7, 10, 11]
    except ValueError:
        return False

# -----------------------------
# Tarabalam Logic
# -----------------------------

def get_tarabalam(user_nakshatra, today_nakshatra):
    """Returns (tara_type, quality)"""
    try:
        start = NAKSHATRAS.index(user_nakshatra)
        current = NAKSHATRAS.index(today_nakshatra)
        position = (current - start) % 27 + 1  # 1 to 27

        tara_cycle = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyak", "Sadhana", "Naidhana", "Mitra", "Param Mitra"]
        tara_type = tara_cycle[(position - 1) % 9]

        if tara_type in ["Sampat", "Param Mitra"]:
            quality = "Very Good"
        elif tara_type in ["Kshema", "Sadhana", "Mitra"]:
            quality = "Good"
        elif tara_type in ["Janma", "Vipat", "Pratyak"]:
            quality = "Not Good"
        else:  # Naidhana
            quality = "Totally Bad"

        return tara_type, quality
    except ValueError:
        return None, "Unknown"

def is_tarabalam_good(user_nakshatra, today_nakshatra):
    _, quality = get_tarabalam(user_nakshatra, today_nakshatra)
    return quality in ["Very Good", "Good"]

# -----------------------------
# Final Muhurta Engine
# -----------------------------

def find_auspicious_muhurtas(user_rashi, user_nakshatra, days=3):
    """
    Main function to find next 'n' days where both Chandrabalam and Tarabalam are good.
    Returns a DataFrame with the results.
    """
    today = datetime.now()
    output = []

    for i in range(days):
        dt = today + timedelta(days=i)
        date_str = dt.strftime("%Y-%m-%d")

        # 🚧 Placeholder: Replace these with API calls to Prokerala to get moon_rashi and nakshatra for this day
        # For now, let's just rotate through some sample values
        moon_rashi = RAASHIS[(RAASHIS.index(user_rashi) + i) % 12]
        today_nakshatra = NAKSHATRAS[(NAKSHATRAS.index(user_nakshatra) + i) % 27]

        # Check balams
        chandra_good = is_chandrabalam_good(user_rashi, moon_rashi)
        tara_type, tara_quality = get_tarabalam(user_nakshatra, today_nakshatra)
        tara_good = tara_quality in ["Very Good", "Good"]

        status = "✅ Auspicious" if chandra_good and tara_good else "❌ Not Auspicious"

        output.append({
            "Date": date_str,
            "Moon Sign (Rashi)": moon_rashi,
            "Chandrabalam": "Good" if chandra_good else "Not Good",
            "Nakshatra": today_nakshatra,
            "Tarabalam": f"{tara_type} - {tara_quality}",
            "Overall Muhurta": status
        })

    return pd.DataFrame(output)
