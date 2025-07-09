from digipin import decode

def get_coordinates_from_digipin(digipin_code):
    try:
        # Normalize: remove hyphens and make uppercase
        cleaned_code = digipin_code.replace("-", "").strip().upper()
        if len(cleaned_code) != 10:
            print("❌ Invalid DigiPin length")
            return None
        lat, lon = decode(cleaned_code)
        print(f"✅ DigiPin decoded: {lat}, {lon}")
        return {"latitude": lat, "longitude": lon}
    except Exception as e:
        print("❌ Invalid DigiPin:", e)
        return None
