import os
import requests
from dotenv import load_dotenv
from utils.digipin_utils import get_coordinates_from_digipin

load_dotenv()

# Load API credentials
CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

# Token URL
TOKEN_URL = "https://api.prokerala.com/token"

def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_location_coordinates(digipin):
    return get_coordinates_from_digipin(digipin)

def get_panchang(lat, lon, datetime, ayanamsa=1, lang="en"):
    url = "https://api.prokerala.com/v2/astrology/panchang"
    params = {
        "ayanamsa": ayanamsa,
        "coordinates": f"{lat},{lon}",
        "datetime": datetime,
        "la": lang
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_detailed_panchang(lat, lon, datetime, ayanamsa=1, lang="en"):
    url = "https://api.prokerala.com/v2/astrology/panchang/advanced"
    params = {
        "ayanamsa": ayanamsa,
        "coordinates": f"{lat},{lon}",
        "datetime": datetime,
        "la": lang
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_choghadiya(lat, lon, datetime, ayanamsa=1, lang="en"):
    url = "https://api.prokerala.com/v2/astrology/choghadiya"
    params = {
        "ayanamsa": ayanamsa,
        "coordinates": f"{lat},{lon}",
        "datetime": datetime,
        "la": lang
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_chandra_bala(lat, lon, datetime, ayanamsa=1, lang="en"):
    url = "https://api.prokerala.com/v2/astrology/chandra-bala"
    params = {
        "ayanamsa": ayanamsa,
        "coordinates": f"{lat},{lon}",
        "datetime": datetime,
        "la": lang
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_tara_bala(lat, lon, datetime, ayanamsa=1, lang="en"):
    url = "https://api.prokerala.com/v2/astrology/tara-bala"
    params = {
        "ayanamsa": ayanamsa,
        "coordinates": f"{lat},{lon}",
        "datetime": datetime,
        "la": lang
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()
