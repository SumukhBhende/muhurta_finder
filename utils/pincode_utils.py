import indiapins

def get_coordinates_from_pincode(pincode: str):
    pc = pincode.strip()
    if not pc.isdigit() or len(pc) != 6:
        print("❌ Invalid PIN code format.")
        return None
    data = indiapins.matching(pc)
    if not data:
        print(f"❌ No data found for PIN: {pc}")
        return None
    # Use first matching entry
    first = data[0]
    coords = indiapins.coordinates(pc)
    if not coords:
        print(f"❌ No coordinates for PIN: {pc}")
        return None
    # Pick the first location
    _, loc = next(iter(coords.items()))
    lat, lon = float(loc["latitude"]), float(loc["longitude"])
    print(f"✅ PIN decoded: {pc} → {lat}, {lon}")
    return {"latitude": lat, "longitude": lon}
