import os
import time
import requests
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

# 🧠 Kundli Data (Moon sign & Nakshatra)
def get_kundali(datetime_str, coordinates):
    try:
        params = {
            "ayanamsa": 1,
            "datetime": datetime_str,
            "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
            "la": "en"
        }

        data = make_api_call("/astrology/kundli", params)
        kundli_data = data.get("data", {})

        return {
            "nakshatra": kundli_data.get("nakshatra_details", {}).get("nakshatra", {}).get("name"),
            "chandra_rasi": kundli_data.get("chandra_rasi", {}).get("name")
        }

    except Exception as e:
        print(f"🚫 Failed to fetch Kundli: {e}")
        return None

# 🌙 Chandra Balam
def get_chandra_balam(datetime_str, coordinates, target_rasi):
    try:
        params = {
            "ayanamsa": 1,
            "datetime": datetime_str,
            "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
            "la": "en"
        }

        data = make_api_call("/astrology/chandra-bala", params)
        details = data.get("data", {})

        for period in details.get("chandraBala", []):
            rasi = period.get("rasi", {}).get("name")
            if rasi == target_rasi:
                is_fav = rasi in details.get("favorableRasi", [])
                return {
                    "is_favorable": is_fav,
                    "until": period.get("end") if is_fav else None,
                    "next_favorable_from": period.get("start") if not is_fav and is_fav_rasi(rasi, details) else None
                }

        return {
            "is_favorable": False,
            "until": None,
            "next_favorable_from": get_next_favorable_chandra_bala(details, target_rasi)
        }

    except Exception as e:
        print(f"🚫 Failed to fetch Chandra Balam: {e}")
        return None

def is_fav_rasi(rasi_name, data):
    return rasi_name in data.get("favorableRasi", [])

def get_next_favorable_chandra_bala(data, target_rasi):
    for period in data.get("chandraBala", []):
        rasi = period.get("rasi", {}).get("name")
        if rasi == target_rasi and rasi in data.get("favorableRasi", []):
            return period.get("start")
    return None

# ✨ Tara Balam
def get_tara_balam(datetime_str, coordinates, target_nakshatra):
    try:
        params = {
            "ayanamsa": 1,
            "datetime": datetime_str,
            "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
            "la": "en"
        }

        data = make_api_call("/astrology/tara-bala", params)
        details = data.get("data", {})

        for period in details.get("tara_bala", []):
            for nak in period.get("nakshatras", []):
                if nak.get("name") == target_nakshatra:
                    is_fav = period.get("type") in ["Good", "Very Good"]
                    return {
                        "is_favorable": is_fav,
                        "valid_until": period.get("end") if is_fav else None,
                        "next_favorable_from": None if is_fav else find_next_favorable_tara(details, target_nakshatra)
                    }

        return {
            "is_favorable": False,
            "valid_until": None,
            "next_favorable_from": find_next_favorable_tara(details, target_nakshatra)
        }

    except Exception as e:
        print(f"🚫 Failed to fetch Tara Balam: {e}")
        return None

def find_next_favorable_tara(data, target_nakshatra):
    for period in data.get("tara_bala", []):
        if period.get("type") in ["Good", "Very Good"]:
            for nak in period.get("nakshatras", []):
                if nak.get("name") == target_nakshatra:
                    return period.get("start")
    return None

# 🕰️ Choghadiya
def get_choghadiya(datetime_str, coordinates):
    try:
        params = {
            "ayanamsa": 1,
            "datetime": datetime_str,
            "coordinates": f"{coordinates['latitude']},{coordinates['longitude']}",
            "la": "en"
        }

        data = make_api_call("/astrology/choghadiya", params)
        muhurats = data.get("data", {}).get("muhurat", [])

        favorable_types = {"Good", "Most Auspicious"}
        favorable_periods = [
            {
                "name": muhurat.get("name"),
                "start": muhurat.get("start"),
                "end": muhurat.get("end"),
                "vela": muhurat.get("vela"),
                "is_day": muhurat.get("is_day")
            }
            for muhurat in muhurats if muhurat.get("type") in favorable_types
        ]

        return favorable_periods

    except Exception as e:
        print(f"🚫 Failed to fetch Choghadiya: {e}")
        return []

# 📍 DigiPin Stub
def get_location_coordinates(digipin):
    raise NotImplementedError("Use utils/digipin_utils.py to decode DigiPin.")
