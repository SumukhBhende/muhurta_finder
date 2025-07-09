import streamlit as st
from datetime import datetime
from api.prokerala_api import decode_digipin, get_location_coordinates
from logic.muhurta_engine import get_muhurtas
from utils.digipin_utils import get_coordinates_from_digipin

st.set_page_config(page_title="Muhurta Finder", page_icon="🌙")
st.title("🌟 Auspicious Muhurta Finder")

# Utility to clean/standardize digipin
def normalize_digipin(code: str) -> str:
    return code.replace("-", "").replace(" ", "").strip().upper()

def format_digipin(code: str) -> str:
    code = normalize_digipin(code)
    return f"{code[:3]}-{code[3:6]}-{code[6:]}" if len(code) == 10 else code

st.markdown("---")
st.subheader("📍 Enter Your Current Location")

digipin = st.text_input("📌 Enter DigiPin (location code)", max_chars=15)
normalized_digipin = normalize_digipin(digipin)

if digipin and len(normalized_digipin) != 10:
    st.error("❌ Please enter a valid 10-character DigiPin (with or without hyphens, e.g. 4K9MCM52K7 or 4K9-MCM-52K7).")
    st.stop()

coordinates = get_coordinates_from_digipin(normalized_digipin) if digipin else None
if coordinates:
    st.success(f"📌 Location: {format_digipin(digipin)} → {coordinates['latitude']}, {coordinates['longitude']}")

st.markdown("---")
st.subheader("🪔 Enter Birth Details")

option = st.radio(
    "How would you like to provide birth info?",
    ["Date, Time & Place of Birth", "Directly Enter Rashi & Nakshatra"]
)

rashi = nakshatra = birth_datetime = birth_coordinates = None

if option == "Date, Time & Place of Birth":
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("📅 Date of Birth")
    with col2:
        tob = st.time_input("⏰ Time of Birth", value=datetime.strptime("04:02", "%H:%M").time())

    birth_digipin = st.text_input("📍 Birth Place DigiPin", max_chars=15)
    normalized_birth_digipin = normalize_digipin(birth_digipin)

    if birth_digipin and len(normalized_birth_digipin) != 10:
        st.error("❌ Please enter a valid 10-character Birth DigiPin.")
        st.stop()

    if birth_digipin:
        birth_coordinates = get_coordinates_from_digipin(normalized_birth_digipin)
        if not birth_coordinates:
            st.error("❌ Could not decode Birth DigiPin.")
            st.stop()

    if dob and tob and birth_coordinates:
        birth_datetime = datetime.combine(dob, tob)
        st.success(f"🎯 Birth details recorded successfully.")

elif option == "Directly Enter Rashi & Nakshatra":
    rashi = st.selectbox("🌙 Your Chandra Rashi", [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", 
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ])
    nakshatra = st.selectbox("✨ Your Janma Nakshatra", [
        "Ashwini", "Bharani", "Krithika", "Rohini", "Mrigashirsha", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishaka", "Anuradha", "Jyeshta",
        "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ])

    st.success("✅ Rashi and Nakshatra recorded successfully.")

st.markdown("---")

if st.button("🔍 Find Muhurtas"):
    if not coordinates:
        st.error("⚠️ Please enter a valid current location DigiPin.")
        st.stop()

    with st.spinner("Calculating best Muhurtas..."):
        results = get_muhurtas(
            current_location=coordinates,
            birth_datetime=birth_datetime,
            birth_location=birth_coordinates,
            rashi=rashi,
            nakshatra=nakshatra
        )

    if not results:
        st.warning("No auspicious muhurta found for the given parameters.")
    else:
        st.success("🎉 Auspicious Muhurtas Found:")
        for muhurta in results:
            st.markdown(f"""
            - 🕒 **Start**: `{muhurta['start']}`
            - ⏳ **End**: `{muhurta['end']}`
            - 🌟 **Type**: `{muhurta['type']}`
            - 🔖 **Choghadiya**: `{muhurta['choghadiya']}`
            ---
            """)

