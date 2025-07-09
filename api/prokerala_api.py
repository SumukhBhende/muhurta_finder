import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.digipin_utils import get_coordinates_from_digipin

load_dotenv()

# Load API credentials from .env file
CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")
BASE_URL = "https://api.prokerala.com/v2/astrology/"

# Get access token
def get_access_token():
    auth_url = "https://api.prokerala.com/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(auth_url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Get coordinates from DigiPin (via local decoder)
def get_location_coordinates(digipin_code):
    return get_coordinates_from_digipin(digipin_code)

# Panchang API
def get_panchang(datetime_obj, latitude, longitude, timezone_offset="+05:30"):
    url = BASE_URL + "panchang"
    payload = {
        "datetime": datetime_obj.isoformat(),
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone_offset,
    }
    response = requests.get(url, params=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Detailed Panchang API
def get_detailed_panchang(datetime_obj, latitude, longitude, timezone_offset="+05:30"):
    url = BASE_URL + "advanced-panchang"
    payload = {
        "datetime": datetime_obj.isoformat(),
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone_offset,
    }
    response = requests.get(url, params=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Choghadiya API
def get_choghadiya(date_obj, latitude, longitude):
    url = BASE_URL + "choghadiya"
    payload = {
        "date": date_obj.strftime("%Y-%m-%d"),
        "latitude": latitude,
        "longitude": longitude,
    }
    response = requests.get(url, params=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Chandra Bala API
def get_chandra_bala(date_obj):
    url = BASE_URL + "chandra-bala"
    payload = {"date": date_obj.strftime("%Y-%m-%d")}
    response = requests.get(url, params=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Tara Bala API
def get_tara_bala(date_obj):
    url = BASE_URL + "tara-bala"
    payload = {"date": date_obj.strftime("%Y-%m-%d")}
    response = requests.get(url, params=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Decode Rashi and Nakshatra from location + birth date/time
def decode_digipin(coords: dict, birth_datetime: datetime):
    lat = coords["latitude"]
    lon = coords["longitude"]
    data = get_detailed_panchang(birth_datetime, lat, lon)
    rashi = data["data"]["nakshatra"]["rasi"]["name"]
    nakshatra = data["data"]["nakshatra"]["name"]
    print(f"🌙 Moon Sign (Rashi): {rashi}, ⭐ Nakshatra: {nakshatra}")
    return rashi, nakshatra
