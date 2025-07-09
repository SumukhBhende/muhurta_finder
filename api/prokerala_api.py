import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

AUTH_URL = "https://api.prokerala.com/token"
BASE_URL = "https://api.prokerala.com/v2"

_token_cache = {
    "token": None,
    "expires_at": 0
}

def get_access_token():
    if _token_cache["token"] and _token_cache["expires_at"] > time.time():
        return _token_cache["token"]

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(AUTH_URL, data=data, headers=headers)
    response.raise_for_status()
    token_data = response.json()

    _token_cache["token"] = token_data["access_token"]
    _token_cache["expires_at"] = time.time() + token_data["expires_in"] - 10
    return _token_cache["token"]

def make_api_call(endpoint, params):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# 🔮 Get Kundli (used to extract Rashi/Nakshatra from birth info)
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

def get_rashi_nakshatra(birth_datetime, coordinates):
    url = "https://api.prokerala.com/v2/astrology/kundli"

    dt_utc = birth_datetime.isoformat() + "+00:00"  # or use .astimezone(timezone.utc).isoformat()
    lat = coordinates["latitude"]
    lon = coordinates["longitude"]

    params = {
        "ayanamsa": 1,
        "coordinates": f"{lat},{lon}",
        "datetime": dt_utc,
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Extract Moon sign (Rashi) and Nakshatra
    rashi = data["data"]["kundli"]["moon"]["rasi"]["name"]
    nakshatra = data["data"]["kundli"]["moon"]["nakshatra"]["name"]

    return {
        "rashi": rashi,
        "nakshatra": nakshatra
    }


# 📍 DigiPin decoding (if you’re doing it via API instead of utils)
def get_location_coordinates(digipin):
    raise NotImplementedError("Use utils/digipin_utils.py to decode DigiPin using CEPT system.")
