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
    # Get Choghadiya blocks
    choghadiya_url = "https://api.prokerala.com/v2/astrology/choghadiya"
    choghadiya_params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    choghadiya_response = requests.get(choghadiya_url, headers=HEADERS, params=choghadiya_params)
    choghadiya_response.raise_for_status()
    choghadiya_data = choghadiya_response.json()

    blocks = choghadiya_data.get("data", [])
    if not isinstance(blocks, list):
        print("❌ Invalid choghadiya response format:", blocks)
        return {"data": []}

    # Get inauspicious periods
    try:
        inauspicious_data = get_inauspicious_periods(coordinates, datetime_str)
        inauspicious_periods_raw = inauspicious_data.get("data", {}).get("muhurat", [])
        inauspicious_periods = []
        for muhurat in inauspicious_periods_raw:
            for period in muhurat.get("period", []):
                start = isoparse(period["start"])
                end = isoparse(period["end"])
                inauspicious_periods.append((start, end))
    except Exception as e:
        print("⚠️ Could not fetch inauspicious periods:", e)
        inauspicious_periods = []

    # Filter out overlapping choghadiya blocks
    def overlaps_with_inauspicious(start, end):
        for ina_start, ina_end in inauspicious_periods:
            if (start < ina_end and end > ina_start):
                return True
        return False

    filtered_blocks = []
    for block in blocks:
        try:
            block_start = isoparse(block["start"])
            block_end = isoparse(block["end"])
            if not overlaps_with_inauspicious(block_start, block_end):
                filtered_blocks.append(block)
        except Exception as e:
            print("❌ Error parsing choghadiya block:", e)

    return {"data": filtered_blocks}


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