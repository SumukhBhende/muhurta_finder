import streamlit as st
from datetime import datetime, date
from logic.muhurta_engine import find_auspicious_muhurtas
from api.prokerala_api import get_rashi_nakshatra_from_birth
from utils.digipin_utils import get_coordinates_from_digipin

st.set_page_config(page_title="🕉️ Muhurta Finder", layout="centered")

st.title("🕉️ Muhurta Finder")
st.markdown("Find the next auspicious Muhurtas based on your birth details or Chandra Rashi + Nakshatra.")

mode = st.radio("Choose input method:", ["🧬 Birth Details (with DigiPin)", "🔭 Rashi + Nakshatra"])

user_info = {}
coords = {}

# ---------------------
# Mode 1: Birth Details
# ---------------------
if mode.startswith("🧬"):
    st.subheader("📜 Birth Details")

    name = st.text_input("Full Name (Optional)", placeholder="e.g., Sumukh Bhende")

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1950, 1, 1),
        max_value=date.today(),
        value=date(2000, 1, 1)
    )

    time_str = st.text_input("Time of Birth (hh:mm)", placeholder="hh:mm")
    digipin = st.text_input("Place of Birth (DigiPin)", placeholder="e.g., M2J-T3L-747J")

    if st.button("🔍 Fetch Rashi + Nakshatra"):
        if digipin and time_str:
            try:
                tob = datetime.strptime(time_str.strip(), "%H:%M").time()
            except ValueError:
                st.error("Please enter time in correct hh:mm format.")
                tob = None

            if tob:
                with st.spinner("Calling Prokerala API..."):
                    rashi, nakshatra = get_rashi_nakshatra_from_birth(dob, tob, digipin)
                    coords = get_coordinates_from_digipin(digipin)

                if rashi and nakshatra:
                    st.success(f"✅ Rashi: `{rashi}`, Nakshatra: `{nakshatra}`")
                    user_info["rashi"] = rashi
                    user_info["nakshatra"] = nakshatra
                    user_info["coords"] = coords
                else:
                    st.error("Could not fetch data. Check DigiPin and try again.")
        else:
            st.warning("Please enter both DigiPin and time of birth.")

# -----------------------------
# Mode 2: Direct Rashi + Nakshatra
# -----------------------------
else:
    st.subheader("🌙 Enter Rashi + Nakshatra Directly")

    rashi = st.selectbox("Moon Sign (Chandra Rashi)", [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ])

    nakshatra = st.selectbox("Nakshatra", [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ])

    digipin = st.text_input("Current Location (DigiPin)", placeholder="e.g., M2J-T3L-747J")

    if digipin:
        coords = get_coordinates_from_digipin(digipin)

    user_info["rashi"] = rashi
    user_info["nakshatra"] = nakshatra
    user_info["coords"] = coords

# ---------------------
# Common: Find Muhurtas
# ---------------------
days = st.slider("Check for next N days:", 1, 10, 3)

if st.button("🕉️ Find Auspicious Muhurtas"):
    if "rashi" in user_info and "nakshatra" in user_info and "coords" in user_info and user_info["coords"]:
        with st.spinner("Calculating auspicious periods..."):
            df = find_auspicious_muhurtas(
                user_info["rashi"],
                user_info["nakshatra"],
                days,
                user_info["coords"]["latitude"],
                user_info["coords"]["longitude"]
            )
        st.success("Here are the upcoming Muhurtas:")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Please ensure Rashi, Nakshatra and coordinates (from DigiPin) are provided.")
