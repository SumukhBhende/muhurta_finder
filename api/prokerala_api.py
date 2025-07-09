import os
import base64
import requests
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

PROKERALA_CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
PROKERALA_CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

if not PROKERALA_CLIENT_ID or not PROKERALA_CLIENT_SECRET:
    raise EnvironmentError("Client credentials not found in .env file")

def get_access_token():
    credentials = f"{PROKERALA_CLIENT_ID}:{PROKERALA_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post("https://api.prokerala.com/token", headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# ----------------------------
# Utility Functions
# ----------------------------

def decode_digipin(digipin):
    response = requests.get(f"https://api.prokerala.com/v2/geo/digipin/{digipin}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_location_coordinates(digipin):
    data = decode_digipin(digipin)
    lat = data["data"]["location"]["latitude"]
    lon = data["data"]["location"]["longitude"]
    return f"{lat},{lon}"

def get_panchang(datetime_str, coordinates, ayanamsa=1):
    url = "https://api.prokerala.com/v2/astrology/panchang"
    params = {
        "datetime": datetime_str,
        "coordinates": coordinates,
        "ayanamsa": ayanamsa
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_detailed_panchang(datetime_str, coordinates, ayanamsa=1):
    url = "https://api.prokerala.com/v2/astrology/panchang/advanced"
    params = {
        "datetime": datetime_str,
        "coordinates": coordinates,
        "ayanamsa": ayanamsa
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_choghadiya(datetime_str, coordinates, ayanamsa=1):
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "datetime": datetime_str,
        "coordinates": coordinates,
        "ayanamsa": ayanamsa
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_chandra_bala(datetime_str, coordinates, ayanamsa=1):
    url = "https://api.prokerala.com/v2/astrology/chandra-bala"
    params = {
        "datetime": datetime_str,
        "coordinates": coordinates,
        "ayanamsa": ayanamsa
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_tara_bala(datetime_str, coordinates, ayanamsa=1):
    url = "https://api.prokerala.com/v2/astrology/tara-bala"
    params = {
        "datetime": datetime_str,
        "coordinates": coordinates,
        "ayanamsa": ayanamsa
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()
