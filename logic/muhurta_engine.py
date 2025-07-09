from datetime import timedelta, datetime
from prokerala_api import get_panchang, get_detailed_panchang, get_choghadiya, get_chandra_bala, get_tara_bala

def get_muhurtas(start_date, end_date, time_str, lat, lon, birth_nakshatra, birth_rashi):
    current_date = start_date
    results = {}

    while current_date <= end_date:
        dt_str = f"{current_date}T{time_str}:00+05:30"

        try:
            # Fetch all required data
            panchang = get_panchang(dt_str, lat, lon)
            detailed = get_detailed_panchang(dt_str, lat, lon)
            choghadiya = get_choghadiya(dt_str, lat, lon)
            chandra = get_chandra_bala(dt_str, lat, lon)
            tara = get_tara_bala(dt_str, lat, lon)

            info = []

            # Check Chandra Bala
            good_rasis = []
            for period in chandra['data']['chandra_bala']:
                for r in period['rasis']:
                    good_rasis.append(r['name'])
            if birth_rashi in good_rasis:
                info.append("🌕 Chandra Bala: ✔️")

            # Check Tara Bala
            good_nakshatras = []
            for period in tara['data']['tara_bala']:
                for nk in period['nakshatras']:
                    good_nakshatras.append(nk['name'])
            if birth_nakshatra in good_nakshatras:
                info.append("✨ Tara Bala: ✔️")

            # Check Auspicious Choghadiya
            good_chogs = []
            for muhurta in choghadiya['data']['muhurat']:
                if muhurta['type'] in ['Good', 'Most Auspicious']:
                    start = muhurta['start'][11:16]
                    end = muhurta['end'][11:16]
                    good_chogs.append(f"{muhurta['name']} ({start} - {end})")
            if good_chogs:
                info.append("🕒 Choghadiya: " + ", ".join(good_chogs))

            # Add detailed panchanga auspicions
            aus_list = []
            for period in detailed['data'].get('auspicious_period', []):
                for p in period['period']:
                    aus_list.append(f"{period['name']} ({p['start'][11:16]} - {p['end'][11:16]})")
            if aus_list:
                info.append("🔱 Muhurtas: " + ", ".join(aus_list))

            results[str(current_date)] = "\n".join(info)

        except Exception as e:
            results[str(current_date)] = f"❌ Error: {e}"

        current_date += timedelta(days=1)

    return results
