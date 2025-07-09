from digipin import decode

def get_coordinates_from_digipin(digipin_code):
    try:
        lat, lon = decode(digipin_code.strip())
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        print("Invalid DigiPin:", e)
        return None
