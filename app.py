import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONNECT TO FIREBASE USING SECRETS ---
if not firebase_admin._apps:
    # This pulls the data you put in the 'Secrets' tab automatically
    cred = credentials.Certificate(dict(st.secrets["firebase_key"]))
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# --- 2. THE DASHBOARD ---
st.title("Project L.I.G.H.T. Dashboard")

# The 'for' loop that keeps devices from overlapping
all_units = db.reference("/").get()
if all_units:
    for unit_id, data in all_units.items():
        if isinstance(data, dict):
            with st.container():
                st.write(f"### 📡 Device: {unit_id}")
                st.metric("Gas Level", f"{data.get('gas_level', 0)} ppm")
                st.metric("Temperature", f"{data.get('temp_level', 0)}°C")
                st.divider()





