from digipin import decode

def get_coordinates_from_digipin(digipin_code: str):
    """
    Decodes a DigiPin into coordinates (lat, lon).
    Returns a dict with 'latitude' and 'longitude' or None on failure.
    """
    try:
        cleaned_code = digipin_code.replace("-", "").strip().upper()
        if len(cleaned_code) != 10:
            return None
        lat, lon = decode(cleaned_code)
        return {"latitude": lat, "longitude": lon}
    except Exception:
        return None
