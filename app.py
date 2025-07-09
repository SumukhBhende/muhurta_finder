import streamlit as st
from datetime import datetime, date
from api.prokerala_api import decode_digipin, get_location_coordinates
from logic.muhurta_engine import get_muhurtas

st.set_page_config(page_title="Muhurta Finder", layout="wide")

st.title("🔱 Muhurta Finder based on Birth Nakshatra and Rashi")

with st.sidebar:
    st.header("📍 Location Input")
    input_method = st.radio("Choose location input method:", ["Manual Entry", "DigiPin"])

    if input_method == "Manual Entry":
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
    else:
        digipin_code = st.text_input("Enter DigiPin code")
        if digipin_code:
            latitude, longitude = decode_digipin(digipin_code)
            if latitude and longitude:
                st.success(f"DigiPin decoded: {latitude}, {longitude}")
            else:
                st.error("Failed to decode DigiPin")
        else:
            latitude = longitude = None

    st.markdown("---")

    st.header("🧬 Birth Details")
    col1, col2 = st.columns(2)
    with col1:
        rashi = st.selectbox("Chandra Rashi", [
            "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
        ])
    with col2:
        nakshatra = st.selectbox("Nakshatra", [
            "Ashwini", "Bharani", "Krithika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu",
            "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
            "Chitra", "Swati", "Vishaka", "Anuradha", "Jyeshta", "Moola", "Purva Ashadha",
            "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ])

    st.markdown("---")

    st.header("📆 Muhurta Range")
    today = date.today()
    start_date = st.date_input("Start Date", value=today)
    end_date = st.date_input("End Date", value=today)
    time_input = st.text_input("Preferred Time (hh:mm)", placeholder="hh:mm", value="05:00")

    # Ensure valid date range
    if end_date < start_date:
        st.error("End date must be after start date")

if st.button("🔍 Find Auspicious Muhurtas"):
    if latitude is None or longitude is None:
        st.error("Please provide valid coordinates.")
    else:
        try:
            st.info("Fetching data from Prokerala API...")
            good_times = get_muhurtas(
                start_date, end_date,
                time_input,
                latitude, longitude,
                nakshatra, rashi
            )

            if good_times:
                st.success("✅ Auspicious Muhurtas Found:")
                for dt, info in good_times.items():
                    st.markdown(f"### {dt}")
                    st.write(info)
            else:
                st.warning("⚠️ No auspicious muhurta found in the given range.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
