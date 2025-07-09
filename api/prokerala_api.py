# api/prokerala_api.py

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

API_BASE_URL = "https://api.prokerala.com/v2"
API_KEY = os.getenv("PROKERALA_API_KEY")
API_SECRET = os.getenv("PROKERALA_API_SECRET")

def get_access_token():
    url = "https://api.prokerala.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("⚠️ Failed to get token:", response.status_code, response.text)
        return None

def get_coordinates_from_place(place):
    # TODO: Add Google Geocoding later
    # Hardcoded fallback (Mapusa, Goa)
    return {"latitude": 15.591, "longitude": 73.815}

def get_rashi_nakshatra_from_birth(dob, tob, place):
    coords = get_coordinates_from_place(place)
    latitude = coords["latitude"]
    longitude = coords["longitude"]

    # Format datetime with timezone
    naive_dt = datetime.combine(dob, tob)
    ist = pytz.timezone("Asia/Kolkata")
    local_dt = ist.localize(naive_dt)
    iso_dt = local_dt.isoformat()  # → 2025-07-09T11:59:41+05:30

    access_token = get_access_token()
    if not access_token:
        return None, None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "ayanamsa": 1,
        "coordinates": f"{latitude},{longitude}",
        "datetime": iso_dt
    }

    url = f"{API_BASE_URL}/astrology/kundli"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        # Extract Moon's Rashi and Nakshatra
        for planet in data["data"]["planetaryPositions"]:
            if planet["planet"]["name"] == "Moon":
                rashi = planet["rasi"]["name"]
                nakshatra = planet["nakshatra"]["name"]
                return rashi, nakshatra
    else:
        print("⚠️ API Error:", response.status_code, response.text)

    return None, None


def get_choghadiya(date_str, latitude, longitude, timezone="Asia/Kolkata"):
    """
    Fetches Choghadiya slots for a given date & location.
    date_str: 'YYYY-MM-DD'
    Returns a list of dicts: [{start, end, type}, ...]
    """
    access_token = get_access_token()
    if not access_token:
        return []

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "date": date_str,
        "coordinates": f"{latitude},{longitude}",
        "timezone": timezone,
        "language": "en"
    }
    url = f"{API_BASE_URL}/astrology/choghadiya"
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print("⚠️ Choghadiya API failed:", resp.status_code, resp.text)
        return []

    data = resp.json().get("data", [])
    # Filter only the auspicious types
    good_types = {"Labh", "Shubh", "Amrit", "Chal"}
    return [
        {
            "start": slot["start"],
            "end": slot["end"],
            "type": slot["type"]
        }
        for slot in data if slot["type"] in good_types
    ]
