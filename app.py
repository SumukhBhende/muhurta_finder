import streamlit as st
from datetime import datetime
from logic.muhurta_engine import find_auspicious_muhurtas
from api.prokerala_api import get_rashi_nakshatra_from_birth

st.set_page_config(page_title="🕉️ Muhurta Finder", layout="centered")

st.title("🕉️ Muhurta Finder")
st.markdown("Find upcoming auspicious Muhurta based on your birth details or Nakshatra-Rashi.")

mode = st.radio("Choose input method:", ["Birth Details", "Rashi + Nakshatra"])

user_info = {}

if mode == "Birth Details":
    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    tob = st.time_input("Time of Birth")
    place = st.text_input("Place of Birth (e.g., Mapusa)")

    if st.button("Fetch Rashi & Nakshatra"):
        if name and place:
            with st.spinner("Fetching from Prokerala API..."):
                rashi, nakshatra = get_rashi_nakshatra_from_birth(dob, tob, place)
            if rashi and nakshatra:
                st.success(f"✅ Rashi: {rashi}, Nakshatra: {nakshatra}")
                user_info["rashi"] = rashi
                user_info["nakshatra"] = nakshatra
            else:
                st.error("Could not fetch birth data.")
else:
    rashi = st.selectbox("Select Rashi (Moon Sign)", [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ])
    nakshatra = st.selectbox("Select Nakshatra", [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ])
    user_info["rashi"] = rashi
    user_info["nakshatra"] = nakshatra

days = st.slider("Find Muhurtas for the next...", 1, 7, 3)

if st.button("🔍 Find Auspicious Muhurtas"):
    if "rashi" in user_info and "nakshatra" in user_info:
        with st.spinner("Calculating..."):
            df = find_auspicious_muhurtas(user_info["rashi"], user_info["nakshatra"], days)
        st.success("Here are your upcoming Muhurta windows:")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Please fill in your Rashi and Nakshatra.")
