from digipin import decode

def get_coordinates_from_digipin(digipin_code):
    from digipin import decode
    try:
        lat, lon = decode(digipin_code.strip())
        print(f"✅ DigiPin decoded: {lat}, {lon}")
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        print("❌ Invalid DigiPin:", e)
        return None
