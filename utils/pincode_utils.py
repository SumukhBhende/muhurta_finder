import indiapins

def get_coordinates_from_pincode(pc):
    data = indiapins.matching(pc)
    if not data:
        return None

    print(data[0])  # 👈 Inspect this structure
    # Try different capitalizations like 'Pincode', 'pincode', etc.

    d = data[0]
    lat = float(d.get("Latitude", 0))
    lon = float(d.get("Longitude", 0))
    return {"latitude": lat, "longitude": lon}
