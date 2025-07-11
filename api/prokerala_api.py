import requests
from dateutil import parser
import json
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


# --- Constants ---
GOOD_CHOICES = {'Char', 'Labh', 'Amrit', 'Shubh','Amrut'}

# --- Delay helper ---
def throttle():
    time.sleep(12)  # 5000 milliseconds delay

# --- Inauspicious Periods ---
def get_inauspicious_periods(datetime_iso: str, coordinates: str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/inauspicious-period"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_iso,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json().get("data", {}).get("muhurat", [])
    
    bad_periods = []
    for entry in data:
        for period in entry["period"]:
            bad_periods.append((
                parser.isoparse(period["start"]),
                parser.isoparse(period["end"])
            ))
    return bad_periods

# --- Choghadiya ---
def get_choghadiya(coordinates: str, datetime_iso: str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_iso,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    choghadiya = response.json().get("data", {}).get("muhurat", [])

    # Get inauspicious periods
    bad_periods = get_inauspicious_periods(datetime_iso, coordinates)

    # Helper to check if two intervals overlap
    def overlaps(start1, end1, start2, end2):
        return max(start1, start2) < min(end1, end2)

    # Filter logic
    good_blocks = []
    for block in choghadiya:
        block_start = parser.isoparse(block["start"])
        block_end = parser.isoparse(block["end"])
        name = block["name"]
        
        # Check if good type and does not overlap with any inauspicious period
        if name in GOOD_CHOICES and not any(overlaps(block_start, block_end, bad_start, bad_end) for bad_start, bad_end in bad_periods):
            good_blocks.append({
                "name": name,
                "type": block["type"],
                "is_day": block["is_day"],
                "start": block["start"],
                "end": block["end"]
            })

    return {"data": {"muhurat": good_blocks}}

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