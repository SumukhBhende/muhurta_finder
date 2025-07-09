import streamlit as st
from datetime import datetime, date, time
from api.prokerala_api import decode_digipin, get_location_coordinates
from logic.muhurta_engine import get_muhurtas

# App Title and Description
st.set_page_config(page_title="Muhurta Finder", page_icon="🕉️", layout="centered")

st.title("🕉️ Muhurta Finder")
st.markdown("""
This app finds **auspicious muhurta timings** using your location (DigiPin) and date/time, based on  
**Choghadiya**, **Chandra Balam**, and **Tara Balam** using authentic Panchang data.
""")

# Option to input birth details or direct Nakshatra/Rashi
input_mode = st.radio("Select Input Method:", ["📍 Use Date, Time & Place of Birth", "🔮 Directly Enter Rashi & Nakshatra"])

if input_mode == "📍 Use Date, Time & Place of Birth":
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("🗓️ Birth Date", value=date(2004, 4, 15))
        birth_time = st.time_input("🕰️ Birth Time", value=time(4, 2))
    with col2:
        birth_digipin = st.text_input("📍 Birth Place DigiPin", max_chars=6)

else:
    rashi_input = st.selectbox("🌙 Select your Moon Sign (Chandra Rashi)", [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ])
    nakshatra_input = st.selectbox("⭐ Select your Birth Nakshatra", [
        "Ashwini", "Bharani", "Krithika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya",
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishaka",
        "Anuradha", "Jyeshta", "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ])

# DigiPin for the current location where muhurta is needed
digipin = st.text_input("📌 Enter DigiPin (6-character location code)")

# Date and time for which muhurta is to be calculated
selected_date = st.date_input("📅 Select Date", date.today())
selected_time = st.time_input("🕒 Select Time", datetime.now().time())

# Submit Button
if st.button("🔍 Find Muhurta"):
    if not digipin or len(digipin.strip()) != 10:
        st.error("Please enter a valid 10-character DigiPin (with or without hyphens, e.g. 4K9MCM52K7 or 4K9-MCM-52K7).")
    else:
        # Get coordinates for current location
        coords = get_location_coordinates(digipin)
        if not coords:
            st.error("Could not decode DigiPin. Please try again.")
        else:
            # Determine Rashi & Nakshatra
            if input_mode == "📍 Use Date, Time & Place of Birth":
                if not birth_digipin or len(birth_digipin.strip()) != 6:
                    st.error("Please enter a valid 6-character birth place DigiPin.")
                else:
                    birth_coords = get_location_coordinates(birth_digipin)
                    if not birth_coords:
                        st.error("Could not decode birth place DigiPin.")
                    else:
                        birth_datetime = datetime.combine(birth_date, birth_time)
                        rashi, nakshatra = decode_digipin(birth_coords, birth_datetime)
                        if not rashi or not nakshatra:
                            st.error("Could not calculate Rashi/Nakshatra.")
                        else:
                            result = get_muhurtas(rashi, nakshatra, coords, selected_date, selected_time)
                            st.success("✅ Muhurta Found")
                            st.write(result)
            else:
                # Direct input path
                result = get_muhurtas(rashi_input, nakshatra_input, coords, selected_date, selected_time)
                st.success("✅ Muhurta Found")
                st.write(result)
