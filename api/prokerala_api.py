import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse  # required for encoding datetime

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
def get_kundali(datetime_str, coordinates):
    encoded_datetime = urllib.parse.quote(datetime_str)

    params = {
        "ayanamsa": 1,  # Lahiri
        "datetime": encoded_datetime,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
        "la": "en"
    }

    data = make_api_call("/astrology/kundli/basic", params)
    
    if not data or "data" not in data:
        return None

    kundli_data = data["data"]
    
    nakshatra_name = (
        kundli_data.get("nakshatra_details", {})
        .get("nakshatra", {})
        .get("name")
    )

    chandra_rasi_name = (
        kundli_data.get("chandra_rasi", {})
        .get("name")
    )

    return {
        "nakshatra": nakshatra_name,
        "chandra_rasi": chandra_rasi_name
    }

# 🌙 Chandra Balam
def get_chandra_balam(datetime_str, coordinates, target_rasi):
    encoded_datetime = urllib.parse.quote(datetime_str)

    params = {
        "ayanamsa": 1,  # Lahiri
        "datetime": encoded_datetime,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
        "la": "en"
    }

    data = make_api_call("/astrology/chandra-bala", params)

    if not data or "data" not in data:
        return None

    favorable_rasis = data["data"].get("favorableRasi", [])
    chandra_bala_periods = data["data"].get("chandraBala", [])

    for period in chandra_bala_periods:
        rasi = period.get("rasi", {}).get("name")
        end_time = period.get("end")
        if rasi == target_rasi and rasi in favorable_rasis:
            return {
                "is_favorable": True,
                "until": end_time  # ISO 8601 format
            }

    return {
        "is_favorable": False,
        "until": None
    }

# ✨ Tara Balam
def get_tara_balam(datetime_str, coordinates, target_nakshatra):
    encoded_datetime = urllib.parse.quote(datetime_str)

    params = {
        "ayanamsa": 1,  # Lahiri
        "datetime": encoded_datetime,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
        "la": "en"
    }

    data = make_api_call("/astrology/tara-bala", params)

    if not data or "data" not in data:
        return None

    tara_periods = data["data"].get("tara_bala", [])

    for period in tara_periods:
        for nak in period.get("nakshatras", []):
            if nak.get("name") == target_nakshatra:
                return {
                    "is_favorable": period.get("type") in ["Good", "Very Good"],
                    "valid_until": period.get("end")  # ISO 8601 format
                }

    return {
        "is_favorable": False,
        "valid_until": None
    }

# 🕰️ Choghadiya
def get_choghadiya(datetime_str, coordinates):
    encoded_datetime = urllib.parse.quote(datetime_str)

    params = {
        "ayanamsa": 1,
        "datetime": encoded_datetime,
        "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
        "la": "en"
    }

    data = make_api_call("/astrology/choghadiya", params)

    if not data or "data" not in data:
        return []

    favorable_types = {"Good", "Most Auspicious"}
    favorable_periods = []

    for muhurat in data["data"].get("muhurat", []):
        if muhurat.get("type") in favorable_types:
            favorable_periods.append({
                "name": muhurat.get("name"),
                "start": muhurat.get("start"),
                "end": muhurat.get("end"),
                "vela": muhurat.get("vela"),
                "is_day": muhurat.get("is_day")
            })

    return favorable_periods

# 🚫 Stub for DigiPin (should be handled in utils)
def get_location_coordinates(digipin):
    raise NotImplementedError("Use utils/digipin_utils.py to decode DigiPin.")
