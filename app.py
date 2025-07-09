import streamlit as st
from datetime import datetime
from logic.muhurta_engine import get_favorable_muhurtas
from utils.digipin_utils import get_coordinates_from_digipin
from api.prokerala_api import get_kundali


st.set_page_config(page_title="Muhurta Finder", page_icon="🌙")
st.title("🌟 Auspicious Muhurta Finder")

# --- Utilities ---
def normalize_digipin(code: str) -> str:
    return code.replace("-", "").replace(" ", "").strip().upper()

def format_digipin(code: str) -> str:
    code = normalize_digipin(code)
    return f"{code[:3]}-{code[3:6]}-{code[6:]}" if len(code) == 10 else code

# --- Location Input ---
st.markdown("---")
st.subheader("📍 Enter Your Current Location")

digipin = st.text_input("📌 Enter DigiPin (location code)", max_chars=15)
normalized_digipin = normalize_digipin(digipin)

if digipin and len(normalized_digipin) != 10:
    st.error("❌ Please enter a valid 10-character DigiPin.")
    st.stop()

coordinates = get_coordinates_from_digipin(normalized_digipin) if digipin else None
if coordinates:
    st.success(f"📌 Location: {format_digipin(digipin)} → {coordinates['latitude']}, {coordinates['longitude']}")

# --- Birth Info Input ---
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

# --- Trigger Logic ---
st.markdown("---")

if st.button("🔍 Find Muhurtas"):
    if not coordinates:
        st.error("⚠️ Please enter a valid current location DigiPin.")
        st.stop()

    # Determine rashi & nakshatra
    if birth_datetime and birth_coordinates:
        try:
            birth_info = get_kundali(birth_datetime.isoformat(), birth_coordinates)
            user_rashi = birth_info["chandra_rasi"]
            user_nakshatra = birth_info["nakshatra"]
        except Exception as e:
            st.error(f"❌ Could not determine Rashi & Nakshatra from birth info: {e}")
            st.stop()
    elif rashi and nakshatra:
        user_rashi = rashi
        user_nakshatra = nakshatra
    else:
        st.error("❌ Rashi & Nakshatra not provided.")
        st.stop()

    with st.spinner("🧠 Calculating best Muhurtas..."):
        today = datetime.utcnow().strftime("%Y-%m-%d")
        try:
            muhurta_blocks = get_favorable_muhurtas(
                date_str=today,
                location=coordinates
            )
        except Exception as e:
            st.error(f"🚫 Failed to fetch Muhurtas: {e}")
            st.stop()

    if not muhurta_blocks:
        st.warning("😞 No favorable Muhurtas found today based on all 3 criteria.")
    else:
        st.success(f"🌟 Found {len(muhurta_blocks)} favorable Muhurtas!")
        for muhurta in muhurta_blocks:
            st.markdown(f"""
            ✅ **{muhurta['name']}**  
            ⏰ {muhurta['start']} → {muhurta['end']}  
            🕰️ Vela: *{muhurta['vela']}*  
            🌞 Period: {"Day" if muhurta['is_day'] else "Night"}  
            ---
            """)
