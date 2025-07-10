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

# --- Delay helper ---
def throttle():
    time.sleep(5)  # 5000 milliseconds delay

# --- Choghadiya ---
def get_choghadiya(coordinates, datetime_str):
    throttle()
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "ayanamsa": 1,
        "coordinates": coordinates,
        "datetime": datetime_str,
        "la": "en"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

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
    return {
        "chandra_rasi": rashi,
        "nakshatra": nakshatra,
        "pada": pada
    }