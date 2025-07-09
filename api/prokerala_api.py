import requests
import os
from urllib.parse import quote_plus

PROKERALA_API_KEY = os.getenv("PROKERALA_API_KEY")
TOKEN_URL = "https://api.prokerala.com/token"
API_BASE_URL = "https://api.prokerala.com/v2/astrology"

# Get access token once
def get_access_token():
    client_id = os.getenv("PROKERALA_CLIENT_ID")
    client_secret = os.getenv("PROKERALA_CLIENT_SECRET")
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

ACCESS_TOKEN = get_access_token()
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def fetch_api(endpoint, params):
    url = f"{API_BASE_URL}/{endpoint}"
    encoded_params = "&".join(f"{k}={quote_plus(str(v))}" for k, v in params.items())
    full_url = f"{url}?{encoded_params}"
    print("🌀 Request:", full_url)
    resp = requests.get(full_url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def decode_digipin(digipin):
    try:
        url = f"https://api.digipin.in/v1/code/{digipin}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return float(data['location']['lat']), float(data['location']['lon'])
    except:
        return None, None

# Wrapper functions for different APIs
def get_panchang(datetime_str, lat, lon):
    return fetch_api("panchang", {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{lat},{lon}",
        "timezone": "Asia/Kolkata"
    })

def get_detailed_panchang(datetime_str, lat, lon):
    return fetch_api("panchang/advanced", {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{lat},{lon}",
        "timezone": "Asia/Kolkata"
    })

def get_choghadiya(datetime_str, lat, lon):
    return fetch_api("choghadiya", {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{lat},{lon}",
        "timezone": "Asia/Kolkata"
    })

def get_chandra_bala(datetime_str, lat, lon):
    return fetch_api("chandra-bala", {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{lat},{lon}",
        "timezone": "Asia/Kolkata"
    })

def get_tara_bala(datetime_str, lat, lon):
    return fetch_api("tara-bala", {
        "ayanamsa": 1,
        "datetime": datetime_str,
        "coordinates": f"{lat},{lon}",
        "timezone": "Asia/Kolkata"
    })
