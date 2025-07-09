import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.prokerala.com/v2"
CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

def get_access_token():
    url = f"{BASE_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def get_panchang(datetime_obj, lat, lon):
    params = {
        "datetime": datetime_obj.isoformat(),
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1,
        "la": "en"
    }
    response = requests.get(f"{BASE_URL}/astrology/panchang", headers=HEADERS, params=params)
    return response.json()

def get_detailed_panchang(datetime_obj, lat, lon):
    params = {
        "datetime": datetime_obj.isoformat(),
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1,
        "la": "en"
    }
    response = requests.get(f"{BASE_URL}/astrology/panchang/advanced", headers=HEADERS, params=params)
    return response.json()

def get_choghadiya(datetime_obj, lat, lon):
    params = {
        "datetime": datetime_obj.isoformat(),
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1,
        "la": "en"
    }
    response = requests.get(f"{BASE_URL}/astrology/choghadiya", headers=HEADERS, params=params)
    return response.json()

def get_chandra_bala(datetime_obj, lat, lon):
    params = {
        "datetime": datetime_obj.isoformat(),
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1,
        "la": "en"
    }
    response = requests.get(f"{BASE_URL}/astrology/chandra-bala", headers=HEADERS, params=params)
    return response.json()

def get_tara_bala(datetime_obj, lat, lon):
    params = {
        "datetime": datetime_obj.isoformat(),
        "coordinates": f"{lat},{lon}",
        "ayanamsa": 1,
        "la": "en"
    }
    response = requests.get(f"{BASE_URL}/astrology/tara-bala", headers=HEADERS, params=params)
    return response.json()
