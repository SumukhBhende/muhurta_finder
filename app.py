import streamlit as st
from logic.muhurta_engine import find_auspicious_muhurtas
from api.prokerala_api import get_rashi_nakshatra_from_birth

st.set_page_config(page_title="Muhurta Finder", layout="centered", page_icon="🕉️")

st.title("🕉️ Muhurta Finder")
st.markdown("Find your next **auspicious muhurta** using your Vedic astrological profile.")

# Choose input mode
input_mode = st.radio("Select Input Method:", ["Birth Details", "Rashi + Nakshatra"], horizontal=True)

user_data = {}

if input_mode == "Birth Details":
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        tob = st.time_input("Time of Birth")
    with col2:
        place = st.text_input("Place of Birth (City)")

    if st.button("Get Rashi & Nakshatra"):
        if name and place:
            with st.spinner("Fetching data from Prokerala..."):
                rashi, nakshatra = get_rashi_nakshatra_from_birth(dob, tob, place)
            if rashi and nakshatra:
                st.success(f"✅ {name}'s Rashi: **{rashi}**, Nakshatra: **{nakshatra}**")
                user_data["rashi"] = rashi
                user_data["nakshatra"] = nakshatra
            else:
                st.error("Failed to fetch birth chart data. Please check your inputs.")
else:
    col1, col2 = st.columns(2)
    with col1:
        rashi = st.selectbox("Select your Chandra Rashi", [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ])
    with col2:
        nakshatra = st.selectbox("Select your Nakshatra", [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
            "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
            "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ])
    user_data["rashi"] = rashi
    user_data["nakshatra"] = nakshatra

# Time window
window = st.selectbox("Find Muhurtas for the next...", ["1 Day", "3 Days", "7 Days"])
days = int(window.split()[0])

if st.button("🔍 Find Auspicious Muhurtas"):
    if "rashi" in user_data and "nakshatra" in user_data:
        with st.spinner("Calculating..."):
            results = find_auspicious_muhurtas(user_data["rashi"], user_data["nakshatra"], days)
        if results:
            st.success("Here are your upcoming auspicious time windows:")
            st.table(results)
        else:
            st.warning("No auspicious muhurta found in the selected range.")
    else:
        st.error("Please provide valid astrological inputs first.")
