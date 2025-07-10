import requests
import os
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
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# Global token reuse (optional: implement auto-refresh logic later)
ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# ----------------------------
# 📌 Location Utilities
# ----------------------------
def get_coordinates_str(coordinates_dict):
    return f"{coordinates_dict['latitude']},{coordinates_dict['longitude']}"

# ----------------------------
# 🌙 Choghadiya API
# ----------------------------
def get_choghadiya(coords, dt_iso):
    params = {
        "ayanamsa": 1,
        "coordinates": coords,
        "datetime": dt_iso,
        "la": "en"
    }
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# ----------------------------
# 🌕 Chandra Bala API
# ----------------------------
def get_chandra_bala(coords, dt_iso):
    params = {
        "ayanamsa": 1,
        "coordinates": coords,
        "datetime": dt_iso,
        "la": "en"
    }
    url = "https://api.prokerala.com/v2/astrology/chandra-bala"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# ----------------------------
# 🌟 Tara Bala API
# ----------------------------
def get_tara_bala(coords, dt_iso):
    params = {
        "ayanamsa": 1,
        "coordinates": coords,
        "datetime": dt_iso,
        "la": "en"
    }
    url = "https://api.prokerala.com/v2/astrology/tara-bala"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

# ----------------------------
# 🧠 Get Rashi & Nakshatra from DOB/TOB/Location
# ----------------------------
def get_kundali(datetime_iso, coordinates_dict):
    coords = get_coordinates_str(coordinates_dict)
    params = {
        "ayanamsa": 1,
        "coordinates": coords,
        "datetime": datetime_iso,
        "la": "en"
    }
    url = "https://api.prokerala.com/v2/astrology/birth-details"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()["data"]
    return {
        "chandra_rasi": data["chandra_rasi"]["name"],
        "nakshatra": data["nakshatra"]["name"],
        "pada": data["nakshatra"]["pada"]
    }
