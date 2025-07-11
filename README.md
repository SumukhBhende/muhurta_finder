# 🕉️ Muhurta Finder App — *v1.1 Stable*

A Streamlit-based Indian astrology web application that helps users find **auspicious muhurta (timings)** for personal and spiritual activities.

The app uses **traditional Vedic Panchang elements** and modern APIs to calculate Muhurtas that are astrologically favorable based on:
- ✅ **Chandra Balam** (Moon Strength)
- ✅ **Tara Balam** (Star Strength)
- ✅ **Choghadiya Muhurat**
- ❌ Avoids **Inauspicious Periods** (Rahu, Yamaganda, Gulika, Dur Muhurat, Varjyam)

---

## 🚀 Features

🔹 **Two Input Modes:**
1. Enter **Date, Time, and Place of Birth** — automatically calculates Rashi & Nakshatra.
2. Or directly provide your **Rashi** and **Nakshatra** if known.

🔹 **Location Input via DigiPin:**
- Accepts any format: `4K9-MCM-52K7`, `4k9mcm52k7`, etc.
- Case-insensitive and format-independent
- Internally decoded using [CEPT-VZG's DigiPin](https://github.com/CEPT-VZG/digipin) system

🔹 **Auspicious Muhurta Calculation Logic:**
- Step 1: Checks if **Chandra Balam** favors your Rashi
- Step 2: Checks if **Tara Balam** supports your Nakshatra
- Step 3: Finds overlapping windows
- Step 4: Filters for only “Good” or “Most Auspicious” **Choghadiya** blocks
- Step 5: 🛡️ **(NEW)** Filters out **inauspicious periods** like Rahu Kalam, Dur Muhurat, etc.

---

## 📁 Project Structure

```

muhurta\_finder/
│
├── app.py                  # 🎯 Streamlit frontend UI
│
├── api/
│   └── prokerala\_api.py     # 🔮 API calls to Prokerala (Choghadiya, Balam, etc.)
│
├── logic/
│   └── muhurta\_engine.py    # 🧠 Filtering logic across Choghadiya + Balam
│
├── utils/
│   └── digipin\_utils.py     # 📌 DigiPin decoding (CEPT library)
│
├── .env                    # 🔐 API credentials
└── README.md               # 📘 This file

````

---

## 🔧 Tech Stack

- 🌐 **Streamlit** – UI framework for rapid prototyping
- 🧠 **Prokerala Astrology API** – Panchang, Balam, Choghadiya, and Inauspicious Periods
- 🛰️ **CEPT DigiPin System** – For decoding location to lat/lon
- 🐍 **Python 3.10+**
- 📦 **venv** – Isolated Python environment

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

Open in browser: [http://localhost:8501](http://localhost:8501)

---

## 📸 Screenshots

> *(To be added soon: include UI walkthrough and results display preview)*

---

## 📜 Changelog

### v1.0 – Initial Version

* Basic logic for finding Choghadiya + Balam overlaps
* DigiPin-based location input
* Two input modes (birth details or Rashi/Nakshatra)

### v1.1 – Major Improvements

* ✅ Added support for Prokerala’s `/inauspicious-period` API
* ✅ Filters out Choghadiya blocks that overlap with Rahu, Yamaganda, Dur Muhurat, Gulika, and Varjyam
* ✅ Fixed Streamlit state issues and error handling
* ✅ Improved response formatting with `json.dumps()` fix
* ✅ Polished UI and input validations

---

## ✨ Planned Features

* 📂 Export results to PDF
* 🕉️ Add filters for event-based muhurta (marriage, travel, etc.)
* 💾 Save favorite profiles and birth presets
* 🌐 Deploy on Streamlit Cloud
* 📱 Mobile-optimized UI layout

---

## 🙏 Credits

* 🪐 [Prokerala API](https://www.prokerala.com/astrology/api/)
* 📍 [CEPT DigiPin](https://github.com/CEPT-VZG/digipin)
* 🖼️ UI built using [Streamlit](https://streamlit.io)

---

## 📜 License

This project is for academic and personal use. Not yet officially licensed.

---

*✨ Built with soul by **Sumukh Bhende***
