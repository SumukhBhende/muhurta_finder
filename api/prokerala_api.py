# api/prokerala_api.py

import requests
import urllib.parse
import os
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()

API_KEY = os.getenv("PROKERALA_API_KEY")
API_SECRET = os.getenv("PROKERALA_API_SECRET")
API_BASE_URL = "https://api.prokerala.com"

def get_access_token():
    url = f"{API_BASE_URL}/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("⚠️ Failed to get token:", response.status_code, response.text)
        return None

def get_coordinates_from_place(place):
    # Static fallback – replace with real geocoder if needed
    return {"latitude": 15.591, "longitude": 73.815}

def get_rashi_nakshatra_from_birth(dob, tob, place):
    coords = get_coordinates_from_place(place)
    date_str = dob.strftime("%Y-%m-%d")
    time_str = tob.strftime("%H:%M:%S")

    access_token = get_access_token()
    if not access_token:
        return None, None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "ayanamsa": 1,  # Lahiri
        "date": date_str,
        "time": time_str,
        "coordinates": f"{coords['latitude']},{coords['longitude']}"
    }

    query_string = urllib.parse.urlencode(params)
    url = f"{API_BASE_URL}/astrology/birth-details?{query_string}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        moon = data["data"]["planet_positions"]["moon"]
        nakshatra = data["data"]["nakshatra"]["name"]
        rashi = moon["rasi"]["name"]
        return rashi, nakshatra
    else:
        print("⚠️ API Error:", response.status_code, response.text)
        return None, None
