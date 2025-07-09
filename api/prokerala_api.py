import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

PROKERALA_CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
PROKERALA_CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")

def get_access_token():
    if not PROKERALA_CLIENT_ID or not PROKERALA_CLIENT_SECRET:
        raise ValueError("Client credentials not found in environment")

    credentials = f"{PROKERALA_CLIENT_ID}:{PROKERALA_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials"
    }

    resp = requests.post("https://api.prokerala.com/token", headers=headers, data=data)
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
