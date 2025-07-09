import os
import requests
from datetime import datetime

# Read API credentials from environment variables
CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

BASE_URL = "https://api.prokerala.com/v2"
TOKEN_URL = f"{BASE_URL}/token"

def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    resp = requests.post(TOKEN_URL, data=payload)
    resp.raise_for_status()
    return resp.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Panchang (optional if needed)
def get_panchang(date, latitude, longitude):
    url = f"{BASE_URL}/astrology/panchang"
    params = {
        "datetime": date.isoformat(),
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# Nakshatra and Rashi calculation from birth details
def get_detailed_panchang(date, latitude, longitude):
    url = f"{BASE_URL}/astrology/panchang/detailed"
    params = {
        "datetime": date.isoformat(),
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# Choghadiya for a date/location
def get_choghadiya(date, latitude, longitude):
    url = f"{BASE_URL}/astrology/choghadiya"
    params = {
        "datetime": date.isoformat(),
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# Chandra Balam
def get_chandra_bala(date, latitude, longitude):
    url = f"{BASE_URL}/astrology/chandra-bala"
    params = {
        "datetime": date.isoformat(),
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# Tara Balam
def get_tara_bala(date, latitude, longitude):
    url = f"{BASE_URL}/astrology/tara-bala"
    params = {
        "datetime": date.isoformat(),
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# (DEPRECATED – local decoding used instead)
# DigiPin decoding is done locally using digipin_utils.py
def decode_digipin(code):
    from utils.digipin_utils import get_coordinates_from_digipin
    return get_coordinates_from_digipin(code)

# For compatibility if needed
def get_location_coordinates(digipin):
    return decode_digipin(digipin)
