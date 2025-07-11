import streamlit as st
from datetime import datetime, timedelta
from logic.muhurta_engine import get_good_muhurta_slots
from utils.pincode_utils import get_coordinates_from_pincode
from api.prokerala_api import get_kundali

st.set_page_config(page_title="Muhurta Finder", page_icon="🌙")
st.title("🌟 Auspicious Muhurta Finder")

# --- Utilities ---
def clean_pincode(pin: str) -> str:
    return pin.strip().replace(" ", "")  # optional


# --- Rashi to Nakshatra Mapping ---
RASHI_TO_NAKSHATRAS = {
    "Mesha": ["Ashwini", "Bharani", "Krittika"],
    "Vrishabha": ["Krittika", "Rohini", "Mrigashirsha"],
    "Mithuna": ["Mrigashirsha", "Ardra", "Punarvasu"],
    "Karka": ["Punarvasu", "Pushya", "Ashlesha"],
    "Simha": ["Magha", "Purva Phalguni", "Uttara Phalguni"],
    "Kanya": ["Uttara Phalguni", "Hasta", "Chitra"],
    "Tula": ["Chitra", "Swati", "Vishaka"],
    "Vrischika": ["Vishaka", "Anuradha", "Jyeshta"],
    "Dhanu": ["Moola", "Purva Ashadha", "Uttara Ashadha"],
    "Makara": ["Uttara Ashadha", "Shravana", "Dhanishta"],
    "Kumbha": ["Dhanishta", "Shatabhisha", "Purva Bhadrapada"],
    "Meena": ["Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
}

# --- Location Input ---
st.markdown("---")
st.subheader("📍 Enter Your Current Location")

pincode = st.text_input("📌 Enter 6-digit Indian Pincode")

if pincode and (not pincode.isdigit() or len(pincode) != 6):
    st.error("❌ Please enter a valid 6-digit Indian Pincode.")
    st.stop()

# You’ll need to replace this with a working pincode-to-coordinates function
from utils.pincode_utils import get_coordinates_from_pincode

coordinates = get_coordinates_from_pincode(pincode) if pincode else None
if coordinates:
    st.success(f"📌 Location (Pincode: {pincode}) → {coordinates['latitude']}, {coordinates['longitude']}")
else:
    if pincode:
        st.error("❌ Could not fetch coordinates for the entered pincode.")

# --- Birth Info Input ---
st.markdown("---")
st.subheader("🪔 Enter Birth Details")

option = st.radio(
    "How would you like to provide birth info?",
    ["Date, Time & Place of Birth", "Directly Enter Rashi & Nakshatra"]
)

rashi = nakshatra = birth_datetime = birth_coordinates = user_rashi = user_nakshatra = None

if option == "Date, Time & Place of Birth":
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("📅 Date of Birth", min_value=datetime(1950, 1, 1))
    with col2:
        tob = st.time_input("⏰ Time of Birth", value=datetime.strptime("00:00", "%H:%M").time())

    birth_pincode = st.text_input("📍 Birth Place Pincode")

    if birth_pincode and (not birth_pincode.isdigit() or len(birth_pincode) != 6):
        st.error("❌ Please enter a valid 6-digit Indian Pincode.")
        st.stop()

    if birth_pincode:
        birth_coordinates = get_coordinates_from_pincode(birth_pincode)
        if not birth_coordinates:
            st.error("❌ Could not fetch coordinates for the entered Pincode.")
            st.stop()

    if dob and tob and birth_coordinates:
        birth_datetime = datetime.combine(dob, tob)
        try:
            datetime_with_tz = birth_datetime.isoformat() + "+05:30"
            rashi, nakshatra, pada = get_kundali(
                datetime_with_tz,
                f"{birth_coordinates['latitude']},{birth_coordinates['longitude']}"
            )
            user_rashi = rashi
            user_nakshatra = nakshatra
            st.success(f"🌙 Your Rashi is **{user_rashi}** and your Nakshatra is **{user_nakshatra}**")
        except Exception as e:
            st.error(f"❌ Failed to fetch Kundali details: {e}")
            st.stop()

elif option == "Directly Enter Rashi & Nakshatra":
    rashi = st.selectbox("🌙 Your Chandra Rashi", list(RASHI_TO_NAKSHATRAS.keys()))
    if rashi:
        valid_nakshatras = RASHI_TO_NAKSHATRAS[rashi]
        nakshatra = st.selectbox("✨ Your Janma Nakshatra", valid_nakshatras)
        user_rashi = rashi
        user_nakshatra = nakshatra

# --- Date Range Input ---
st.markdown("---")
st.subheader("📆 Select Date Range to Find Muhurtas")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🔸 Start Date", value=datetime.today())
with col2:
    end_date = st.date_input("🔸 End Date", value=datetime.today() + timedelta(days=1))

if start_date > end_date:
    st.error("🚫 Start date cannot be after end date.")
    st.stop()

# --- Trigger Logic ---
st.markdown("---")

if st.button("🔍 Find Muhurtas"):
    if not coordinates:
        st.error("⚠️ Please enter a valid current location DigiPin.")
        st.stop()

    if not (user_rashi and user_nakshatra):
        st.error("❌ Rashi & Nakshatra not provided.")
        st.stop()

    with st.spinner("🧠 Calculating best Muhurtas..."):
        try:
            muhurta_blocks = get_good_muhurta_slots(
                start_date_str=start_date.strftime("%Y-%m-%d"),
                end_date_str=end_date.strftime("%Y-%m-%d"),
                coordinates=coordinates,
                rasi=user_rashi,
                nakshatra=user_nakshatra
            )
        except Exception as e:
            st.error(f"🚫 Failed to fetch Muhurtas: {e}")
            st.stop()

    if not muhurta_blocks:
        st.warning("😞 No favorable Muhurtas found in the selected date range.")
    else:
        st.success(f"🌟 Found {len(muhurta_blocks)} favorable Muhurtas!")
        for muhurta in muhurta_blocks:
            st.markdown(f"""
            ✅ **{muhurta['label']}**  
            ⏰ {muhurta['start']} → {muhurta['end']}  
            🕰️ Vela: *{muhurta['vela']}*  
            🌞 Period: {"Day" if muhurta['is_day'] else "Night"}  
            ---
            """)
