import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
from utils.digipin_utils import get_coordinates_from_digipin

# Load API credentials from .env
load_dotenv()
API_BASE_URL = "https://api.prokerala.com/v2"
CLIENT_ID = os.getenv("PROKERALA_API_KEY")
CLIENT_SECRET = os.getenv("PROKERALA_API_SECRET")

# ------------------------------------------
# Auth
# ------------------------------------------
def get_access_token():
    url = "https://api.prokerala.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        return response.json()["access_token"]
    else:
        print("⚠️ Token Error:", response.status_code, response.text)
        return None

# ------------------------------------------
# Get Rashi & Nakshatra from Birth Data + DigiPin
# ------------------------------------------
def get_rashi_nakshatra_from_birth(dob, tob, digipin):
    coords = get_coordinates_from_digipin(digipin)
    if coords is None:
        return None, None

    dt = datetime.combine(dob, tob)
    timezone = pytz.timezone("Asia/Kolkata")
    dt_iso = timezone.localize(dt).isoformat()

    access_token = get_access_token()
    if not access_token:
        return None, None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "ayanamsa": 1,
        "coordinates": f"{coords['latitude']},{coords['longitude']}",
        "datetime": dt_iso
    }

    url = f"{API_BASE_URL}/astrology/kundli"
    response = requests.get(url, headers=headers, params=params)

    if not response.ok:
        print("⚠️ Kundli API Error:", response.status_code, response.text)
        return None, None

    try:
        data = response.json()["data"]["planetaryPositions"]
        for planet in data:
            if planet["planet"]["name"] == "Moon":
                rashi = planet["rasi"]["name"]
                nakshatra = planet["nakshatra"]["name"]
                return rashi, nakshatra
        return None, None
    except Exception as e:
        print("Parsing Error:", e)
        return None, None

# ------------------------------------------
# Get Choghadiya for a date and coordinates
# ------------------------------------------
def get_choghadiya(date_str, latitude, longitude, timezone="Asia/Kolkata"):
    access_token = get_access_token()
    if not access_token:
        return []

    url = f"{API_BASE_URL}/astrology/choghadiya"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "date": date_str,
        "coordinates": f"{latitude},{longitude}",
        "timezone": timezone
    }

    response = requests.get(url, headers=headers, params=params)
    if not response.ok:
        print("⚠️ Choghadiya Error:", response.status_code, response.text)
        return []

    data = response.json().get("data", [])
    good_types = {"Labh", "Shubh", "Amrit", "Chal"}
    return [slot for slot in data if slot["type"] in good_types]

def get_daily_moon_data(date_str, latitude, longitude, timezone="Asia/Kolkata"):
    """
    Fetches the Moon Rashi and Nakshatra for the full day using Panchang API.
    """
    access_token = get_access_token()
    if not access_token:
        return None, None

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "date": date_str,
        "coordinates": f"{latitude},{longitude}",
        "timezone": timezone
    }

    url = f"{API_BASE_URL}/astrology/panchang"
    response = requests.get(url, headers=headers, params=params)
    if not response.ok:
        print("⚠️ Panchang API failed:", response.status_code, response.text)
        return None, None

    data = response.json().get("data", {})
    try:
        moon_rashi = data["rasi"]["moon"]["name"]
        nakshatra = data["nakshatra"]["nakshatra"]["name"]
        return moon_rashi, nakshatra
    except:
        return None, None
