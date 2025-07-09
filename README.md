# 🕉️ Muhurta Finder App

A Streamlit-based astrology application that helps users find **auspicious muhurta (timing)** for activities based on traditional Indian astrology using:
- ✅ Chandra Balam (Moon Strength)
- ✅ Tara Balam (Star Strength)
- ✅ Choghadiya Muhurat

---

## 🚀 Features

🔹 **Two Input Modes:**
1. Enter **Date, Time, and Place of Birth** — system calculates Rashi and Nakshatra.
2. Or directly provide your **Rashi** and **Nakshatra**.

🔹 **Location Input via DigiPin:**
- Enter DigiPin in any format: `4K9-MCM-52K7` or `4k9mcm52k7`
- Supports lowercase and uppercase automatically
- Internally decoded using CEPT-VZG’s DigiPin open-source system

🔹 **Auspicious Muhurta Calculation:**
- Checks if Chandra Balam is favorable for your Rashi
- Then checks Tara Balam for your Nakshatra
- Finds overlapping good time window
- Finally filters Choghadiya Muhurat blocks in that time window that are “Good” or “Most Auspicious”

---

## 📁 Project Structure

```

muhurta\_finder/
│
├── app.py                    # Streamlit frontend UI
│
├── api/
│   └── prokerala\_api.py      # Handles all API calls to Prokerala
│
├── logic/
│   └── muhurta\_engine.py     # Core logic for filtering auspicious muhurta
│
├── utils/
│   └── digipin\_utils.py      # DigiPin decoding using CEPT-VZG open source
│
├── .env                      # Contains PROKERALA\_CLIENT\_ID and CLIENT\_SECRET
└── README.md

````

---

## 🔧 Technologies Used

- 🌐 **Streamlit** – for the user interface
- 🧠 **Prokerala Astrology API** – for Panchang, Choghadiya, Chandra Balam, Tara Balam
- 🛰️ **CEPT DigiPin System** – for place-based coordinate decoding
- 🐍 **Python 3.10+**

---

## 📦 Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/your-username/muhurta-finder.git
cd muhurta-finder
````

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up `.env` file**

```
PROKERALA_CLIENT_ID=your_client_id_here
PROKERALA_CLIENT_SECRET=your_client_secret_here
```

5. **Run the app**

```bash
streamlit run app.py
```

---

## 📸 Screenshots

> *Add Streamlit UI screenshots here once finalized*

---

## ✨ Future Features

* Add support for event-specific muhurta (e.g., Griha Pravesh, Marriage, Travel)
* Allow saving favorite locations or profiles
* Offline fallback using pre-fetched data or Panchang rules

---

## 🙏 Credits

* [Prokerala API](https://www.prokerala.com/astrology/api/)
* [CEPT DigiPin](https://github.com/CEPT-VZG/digipin)
* UI built using [Streamlit](https://streamlit.io)

---

## 📜 License

This project is not yet Licensed.
