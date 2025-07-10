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
from dateutil import parser

# Helper to check overlap
def intervals_overlap(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

# Fetch inauspicious periods
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

    periods = []
    muhurats = response.json().get("data", {}).get("muhurat", [])
    for muhurta in muhurats:
        for p in muhurta.get("period", []):
            periods.append({
                "start": parser.isoparse(p["start"]),
                "end": parser.isoparse(p["end"])
            })
    return periods

# Choghadiya with filtering
def get_choghadiya(coordinates, datetime_str):
    throttle()
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

    # Fetch and filter inauspicious periods
    inauspicious = get_inauspicious_periods(coordinates, datetime_str)

    # Filter vela blocks
    original_vela = choghadiya_data.get("data", {}).get("vela", [])
    filtered_vela = []
    for block in original_vela:
        start = parser.isoparse(block["start"])
        end = parser.isoparse(block["end"])
        if not any(intervals_overlap(start, end, bad["start"], bad["end"]) for bad in inauspicious):
            filtered_vela.append(block)

    # Replace vela with filtered ones
    choghadiya_data["data"]["vela"] = filtered_vela
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