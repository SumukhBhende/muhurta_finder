import streamlit as st
from datetime import datetime
from api.prokerala_api import get_location_coordinates
from logic.muhurta_engine import get_muhurtas

st.set_page_config(page_title="🕉️ Muhurta Finder", layout="centered")
st.title("🕉️ Muhurta Finder")

st.markdown("""
This app finds **auspicious muhurta timings** using your location (**DigiPin**) and date/time, 
based on **Choghadiya**, **Chandra Balam**, and **Tara Balam** using authentic Panchang data.
""")

# Input Fields
digipin = st.text_input("📍 Enter DigiPin (6-character location code)", max_chars=6)

date = st.date_input("📅 Select Date", value=datetime.now().date())
time = st.time_input("🕒 Select Time", value=datetime.now().time())

if st.button("🔍 Find Muhurta"):
    if not digipin or len(digipin.strip()) != 6:
        st.error("❌ Please enter a valid 6-character DigiPin.")
    else:
        datetime_input = datetime.combine(date, time).isoformat()
        st.info(f"Calculating Muhurta for {digipin.upper()} on {datetime_input}...")

        result = get_muhurtas(digipin, datetime_input)

        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            # Location
            st.subheader("📌 Location Coordinates")
            st.write(result["location"])

            # Panchang
            st.subheader("📖 Basic Panchang")
            st.json(result["panchang"])

            # Detailed Panchang
            st.subheader("📜 Detailed Panchang")
            st.json(result["detailed_panchang"])

            # Choghadiya
            st.subheader("🕒 Choghadiya Muhurtas")
            for muhurta in result["choghadiya"]["muhurat"]:
                st.write(f"**{muhurta['name']}** ({muhurta['type']}) — {muhurta['start']} to {muhurta['end']}")

            # Chandra Bala
            st.subheader("🌙 Chandra Bala (Favorable Moon Signs)")
            for period in result["chandra_bala"]["chandra_bala"]:
                st.write(f"From **{period['start']}** to **{period['end']}**:")
                signs = [rasi["name"] for rasi in period["rasis"]]
                st.write(", ".join(signs))

            # Tara Bala
            st.subheader("🌟 Tara Bala (Favorable Nakshatras)")
            for bala in result["tara_bala"]["tara_bala"]:
                st.write(f"**{bala['name']}** ({bala['type']}) — {bala['start']} to {bala['end']}")
                nakshatras = [n["name"] for n in bala["nakshatras"]]
                st.write("Nakshatras:", ", ".join(nakshatras))
