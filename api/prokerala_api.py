import requests
import os
import time
from datetime import datetime
from dateutil.parser import parse as parse_datetime
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


# --- Inauspicious Periods Helper ---
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
    return response.json()

# --- Choghadiya ---
def get_choghadiya(coordinates, datetime_str):
    throttle()

    # Step 1: Fetch choghadiya
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    choghadiya_data = response.json()

    # Step 2: Fetch inauspicious periods
    inauspicious_data = get_inauspicious_periods(coordinates, datetime_str)
    inauspicious_periods = []
    for muhurta in inauspicious_data.get("data", {}).get("muhurat", []):
        for period in muhurta.get("period", []):
            start = parse_datetime(period["start"])
            end = parse_datetime(period["end"])
            inauspicious_periods.append((start, end))

    # Step 3: Filter out overlapping choghadiya blocks
    filtered_choghadiyas = []
    for ch in choghadiya_data.get("data", []):
        ch_start = parse_datetime(ch["start"])
        ch_end = parse_datetime(ch["end"])

        overlaps = any(
            ch_start < bad_end and ch_end > bad_start
            for bad_start, bad_end in inauspicious_periods
        )

        if not overlaps:
            filtered_choghadiyas.append(ch)

    # Step 4: Return in same JSON structure
    choghadiya_data["data"] = filtered_choghadiyas
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