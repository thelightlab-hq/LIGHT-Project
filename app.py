import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. THEME & UI ---
st.set_page_config(page_title="L.I.G.H.T. Network", layout="wide")
st.markdown("<style>.stApp { background-color: #FFFFFF; }</style>", unsafe_allow_html=True)

# --- 2. SECURE FIREBASE CONNECTION ---
if not firebase_admin._apps:
    # This dictionary contains the secret key you sent earlier
    firebase_creds = {
        "type": "service_account",
        "project_id": "light-40317",
        "private_key_id": "3770ac85dc5b83de8aa8d537eb9a5d7cb7438ee7",
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": "firebase-adminsdk-fbsvc@light-40317.iam.gserviceaccount.com",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# --- 3. DYNAMIC MULTI-UNIT DASHBOARD ---
st.title("Project L.I.G.H.T. Real-time Network")
st.write("Automatically detecting localized inspection units...")

all_data = db.reference("/").get()

if all_data:
    for device_id, sensors in all_data.items():
        if isinstance(sensors, dict):
            with st.expander(f"📟 UNIT: {device_id}", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gas Level", f"{sensors.get('gas_level', 0)} ppm")
                with col2:
                    st.metric("Temperature", f"{sensors.get('temp_level', 0)}°C")
                with col3:
                    gas = sensors.get('gas_level', 0)
                    status = "✅ SAFE" if gas < 400 else "⚠️ ANOMALY"
                    st.subheader(status)
else:
    st.warning("No hardware units detected. Please check your ESP32.")

  delay(3000); 
}

