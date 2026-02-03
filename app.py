import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. UI SETTINGS & LIGHT-NEON CSS ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    .neon-title {
        color: #000000;
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px;
        margin-bottom: 10px;
        text-shadow: 2px 2px 8px rgba(0, 255, 170, 0.4);
    }

    .metric-card {
        background-color: #ffffff; 
        border-radius: 20px;
        padding: 30px;
        color: #000000;
        text-align: center;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid #e0e0e0; /* Light Gray Outline */
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.2); /* Neon Glow */
    }

    .metric-value {
        font-size: 3.5rem;
        font-weight: bold;
        color: #000000;
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE AUTH ---
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"Auth Error: {e}")

# --- 3. UI LAYOUT ---
st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = db.reference("/UNIT_01").get()
            if data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'<div class="metric-card"><h3>GAS LEVEL</h3><p class="metric-value">{data.get("gas_level", 0)}</p><p>ppm</p></div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'<div class="metric-card"><h3>TEMPERATURE</h3><p class="metric-value">{data.get("temp_level", 0)}°</p><p>Celsius</p></div>', unsafe_allow_html=True)
                
                with col3:
                    gas = data.get("gas_level", 0)
                    status = "STABLE" if gas < 400 else "ANOMALY"
                    color = "#28a745" if status == "STABLE" else "#dc3545"
                    glow = "rgba(40, 167, 69, 0.3)" if status == "STABLE" else "rgba(220, 53, 69, 0.3)"
                    st.markdown(f'<div class="metric-card" style="box-shadow: 0 0 20px {glow}; border-color: {color};"><h3>STATUS</h3><p style="font-size:3rem; color:{color}; font-weight:bold;">{status}</p></div>', unsafe_allow_html=True)
            else:
                st.warning("Awaiting data from UNIT_01...")
        except:
            st.error("Database Connection Lost")
        time.sleep(5)
