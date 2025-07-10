import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# 🔐 Prokerala API Credentials
# ----------------------------
CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")
TOKEN_URL = "https://api.prokerala.com/token"

# ----------------------------
# 🪙 Authentication
# ----------------------------
def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post("https://api.prokerala.com/token", data=data)
    response.raise_for_status()
    return response.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# --- Delay helper ---
def throttle():
    time.sleep(8)  # 5000 milliseconds delay

# --- Choghadiya ---
from dateutil.parser import isoparse

# --- Inauspicious Period ---
def get_inauspicious_periods(coordinates, datetime_str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/inauspicious-period"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json().get("data", {}).get("muhurat", [])
    # Flatten all inauspicious periods into (start, end) datetime tuples
    periods = []
    for muhurta in data:
        for p in muhurta.get("period", []):
            start = isoparse(p["start"])
            end = isoparse(p["end"])
            periods.append((start, end))
    return periods

# --- Choghadiya with Inauspicious Filter ---
def get_choghadiya(coordinates, datetime_str):
    throttle()

    # Step 1: Get original Choghadiya
    choghadiya_url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    choghadiya_response = requests.get(choghadiya_url, headers=HEADERS, params=params)
    choghadiya_response.raise_for_status()
    choghadiya_data = choghadiya_response.json()

    # Step 2: Get inauspicious periods
    inauspicious_periods = get_inauspicious_periods(coordinates, datetime_str)

    # Step 3: Filter out overlapping choghadiyas
    filtered_choghadiya = []
    for block in choghadiya_data.get("data", []):
        block_start = isoparse(block["start"])
        block_end = isoparse(block["end"])

        overlaps = any(
            not (block_end <= period_start or block_start >= period_end)
            for period_start, period_end in inauspicious_periods
        )

        if not overlaps:
            filtered_choghadiya.append(block)

    # Step 4: Return same JSON structure, but with filtered data
    choghadiya_data["data"] = filtered_choghadiya
    return choghadiya_data


# --- Chandra Bala ---
def get_chandra_bala(coordinates, datetime_str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/chandra-bala"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# --- Tara Bala ---
def get_tara_bala(coordinates, datetime_str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/tara-bala"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# --- Birth Details for Rashi/Nakshatra ---
def get_kundali(datetime_iso, coordinates):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/birth-details"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_iso,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json().get("data", {})
    rashi = data.get("chandra_rasi", {}).get("name")
    nakshatra = data.get("nakshatra", {}).get("name")
    pada = data.get("nakshatra", {}).get("pada")
    return rashi,nakshatra,pada