import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ PROKERALA_CLIENT_ID or PROKERALA_CLIENT_SECRET not set in .env")

BASE_URL = "https://api.prokerala.com/v2"

_token_data = {
    "access_token": None,
    "expires_at": 0
}

# 🔑 Token Generator
def get_access_token():
    global _token_data

    if _token_data["access_token"] and time.time() < _token_data["expires_at"]:
        return _token_data["access_token"]

    url = "https://api.prokerala.com/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.post(url, data=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    _token_data["access_token"] = data["access_token"]
    _token_data["expires_at"] = time.time() + data["expires_in"] - 30  # buffer

    return _token_data["access_token"]

# 📡 Generic API Caller
def make_api_call(endpoint, params):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# 🧠 Kundli Data (includes moon sign and nakshatra)
def get_kundli_data(datetime_str, coordinates):
    params = {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}"
    }
    return make_api_call("/astrology/kundli", params)

# 🌙 Chandra Balam
def get_chandra_balam(datetime_str, coordinates, target_rashi):
    params = {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}"
    }
    data = make_api_call("/astrology/chandra-bala", params)
    return target_rashi in data.get("data", {}).get("favorableRashi", [])

# ✨ Tara Balam
def get_tara_balam(datetime_str, coordinates, target_nakshatra):
    params = {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}"
    }
    data = make_api_call("/astrology/tara-bala", params)
    return target_nakshatra in data.get("data", {}).get("favorableNakshatra", [])

# 🕰️ Choghadiya
def get_choghadiya(datetime_str, coordinates):
    params = {
        "datetime": datetime_str,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}"
    }
    return make_api_call("/astrology/choghadiya", params)

# 🌙 Extract Rashi & Nakshatra (wrapper around kundli API)
def get_rashi_nakshatra(birth_datetime, coordinates):
    dt_utc = birth_datetime.isoformat() + "+00:00"
    kundli_data = get_kundli_data(dt_utc, coordinates)

    moon_data = kundli_data["data"]["kundli"]["moon"]
    rashi = moon_data["rasi"]["name"]
    nakshatra = moon_data["nakshatra"]["name"]

    return {
        "rashi": rashi,
        "nakshatra": nakshatra
    }

# 🚫 Stub for DigiPin (should be handled in utils)
def get_location_coordinates(digipin):
    raise NotImplementedError("Use utils/digipin_utils.py to decode DigiPin.")
