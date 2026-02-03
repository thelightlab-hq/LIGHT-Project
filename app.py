import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. UI SETTINGS & NEON CSS ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    .neon-title {
        color: #ffffff;
        font-size: 100px !important; /* BUMPED SIZE */
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px;
        margin-bottom: 0px;
        text-shadow: 0 0 10px #fff, 0 0 20px #0fa, 0 0 40px #0fa;
    }

    .system-sub {
        color: #lightgray;
        text-align: center;
        font-size: 24px;
        margin-bottom: 50px;
    }

    .metric-card {
        background-color: #f0f2f6; 
        border-radius: 20px;
        padding: 30px;
        color: #000000;
        text-align: center;
        min-height: 300px; /* FORCES EQUAL HEIGHT */
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid #ffffff;
    }

    .metric-value {
        font-size: 3.5rem;
        font-weight: bold;
        color: #008080;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE AUTH ---
if not firebase_admin._apps:
    try:
        # Assuming you've set up Streamlit Secrets
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except:
        st.error("Firebase Auth Failed. Check your Secrets.")

# --- 3. DASHBOARD MAIN UI ---
st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)
st.markdown('<p class="system-sub">Safety Monitoring System</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Fetching specifically for UNIT_01
            data = db.reference("/UNIT_01").get()
            
            if data:
                col1, col2, col3 = st.columns([1, 1, 1]) # MATHEMATICALLY EQUAL
                
                with col1:
                    st.markdown(f'<div class="metric-card"><h3>GAS LEVEL</h3><p class="metric-value">{data.get("gas_level", 0)}</p><p>ppm</p></div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'<div class="metric-card"><h3>TEMPERATURE</h3><p class="metric-value">{data.get("temp_level", 0)}°</p><p>Celsius</p></div>', unsafe_allow_html=True)
                
                with col3:
                    gas = data.get("gas_level", 0)
                    status = "STABLE" if gas < 400 else "ANOMALY"
                    color = "#28a745" if status == "STABLE" else "#dc3545"
                    st.markdown(f'<div class="metric-card" style="border-color:{color};"><h3>SYSTEM STATUS</h3><p style="font-size:3rem; color:{color}; font-weight:bold;">{status}</p></div>', unsafe_allow_html=True)
            else:
                st.warning("No data found. ESP32 might be offline.")
        except Exception as e:
            st.error(f"Error: {e}")
        
        time.sleep(5)
