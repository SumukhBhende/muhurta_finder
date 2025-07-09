from api.prokerala_api import (
    get_panchang,
    get_detailed_panchang,
    get_choghadiya,
    get_chandra_bala,
    get_tara_bala
)

def get_muhurtas(digipin, datetime_iso, ayanamsa=1, lang="en"):
    """
    Given a DigiPin and datetime (ISO 8601), returns all Muhurta-related data.

    Parameters:
    - digipin: 6-character location code (to be decoded into lat/lon)
    - datetime_iso: e.g., '2025-07-09T06:00:00+05:30'
    - ayanamsa: 1 = Lahiri (default), 3 = Raman, 5 = KP
    - lang: language code ('en', 'hi', etc.)

    Returns:
    - Dictionary with Panchang, Detailed Panchang, Choghadiya, Chandra Bala, Tara Bala
    """
    from api.prokerala_api import get_location_coordinates

    # Get lat/lon from DigiPin
    location = get_location_coordinates(digipin)
    if not location:
        return {"error": "Invalid DigiPin provided."}

    lat = location["latitude"]
    lon = location["longitude"]

    try:
        panchang = get_panchang(lat, lon, datetime_iso, ayanamsa, lang)
        detailed = get_detailed_panchang(lat, lon, datetime_iso, ayanamsa, lang)
        choghadiya = get_choghadiya(lat, lon, datetime_iso, ayanamsa, lang)
        chandra_bala = get_chandra_bala(lat, lon, datetime_iso, ayanamsa, lang)
        tara_bala = get_tara_bala(lat, lon, datetime_iso, ayanamsa, lang)

        return {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "panchang": panchang["data"],
            "detailed_panchang": detailed["data"],
            "choghadiya": choghadiya["data"],
            "chandra_bala": chandra_bala["data"],
            "tara_bala": tara_bala["data"]
        }

    except Exception as e:
        return {"error": str(e)}
