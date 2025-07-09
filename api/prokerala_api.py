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
    r = requests.post(url, headers=headers, data=data)
    return r.json().get("access_token") if r.ok else None

def get_coordinates_from_place(place):
    return {"latitude": 15.591, "longitude": 73.815}  # TODO: Use geocoding later

def get_rashi_nakshatra_from_birth(dob, tob, place):
    coords = get_coordinates_from_place(place)
    dt = datetime.combine(dob, tob)
    tz = pytz.timezone("Asia/Kolkata")
    iso_dt = tz.localize(dt).isoformat()

    token = get_access_token()
    if not token: return None, None

    url = f"{API_BASE_URL}/astrology/kundli"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "ayanamsa": 1,
        "coordinates": f"{coords['latitude']},{coords['longitude']}",
        "datetime": iso_dt
    }

    r = requests.get(url, headers=headers, params=params)
    if not r.ok:
        return None, None

    data = r.json()
    for planet in data["data"]["planetaryPositions"]:
        if planet["planet"]["name"] == "Moon":
            return planet["rasi"]["name"], planet["nakshatra"]["name"]
    return None, None

def get_choghadiya(date_str, latitude, longitude, timezone="Asia/Kolkata"):
    token = get_access_token()
    if not token: return []

    url = f"{API_BASE_URL}/astrology/choghadiya"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "date": date_str,
        "coordinates": f"{latitude},{longitude}",
        "timezone": timezone
    }

    r = requests.get(url, headers=headers, params=params)
    if not r.ok: return []

    data = r.json().get("data", [])
    good = {"Shubh", "Labh", "Amrit", "Chal"}
    return [slot for slot in data if slot["type"] in good]
