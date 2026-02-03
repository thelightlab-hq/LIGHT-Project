import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. UI SETTINGS & LIGHT-NEON CSS ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Main Background: White */
    .stApp { 
        background-color: #ffffff; 
    }
    
    /* THE TITLE: Black with a subtle white/cyan glow */
    .neon-title {
        color: #000000;
        font-size: 100px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px;
        margin-bottom: 0px;
        text-shadow: 2px 2px 10px rgba(0, 255, 170, 0.3);
    }

    .system-sub {
        color: #333333;
        text-align: center;
        font-size: 24px;
        margin-bottom: 50px;
        font-weight: bold;
    }

    /* THE CARDS: Light Gray outline with Neon Glow */
    .metric-card {
        background-color: #ffffff; 
        border-radius: 20px;
        padding: 30px;
        color: #000000; /* Black Text */
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        /* Light Gray Border */
        border: 2px solid #e0e0e0;
        
        /* NEON GLOW ON THE BOX OUTLINE */
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.4); 
    }

    .metric-value {
        font-size: 3.5rem;
        font-weight: bold;
        color: #000000; /* Black numbers */
        /* Neon text glow */
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.6);
    }

    h3 {
        color: #000000 !important;
        letter-spacing: 2px;
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
    except:
        st.error("Firebase Auth Failed. Please check the Secrets tab.")

# --- 3. DASHBOARD MAIN UI ---
st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)
st.markdown('<p class="system-sub">Safety Monitoring System</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = db.reference("/UNIT_01").get()
            
            if data:
                col1, col2, col3 = st.columns([1, 1, 1]) 
                
                with col1:
                    st.markdown(f'''
                        <div class="metric-card" style="box-shadow: 0 0 20px rgba(0, 150, 255, 0.3);">
                            <h3>GAS LEVEL</h3>
                            <p class="metric-value">{data.get("gas_level", 0)}</p>
                            <p style="font-weight:bold;">ppm</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                        <div class="metric-card" style="box-shadow: 0 0 20px rgba(0, 255, 170, 0.3);">
                            <h3>TEMPERATURE</h3>
                            <p class="metric-value">{data.get("temp_level", 0)}°</p>
                            <p style="font-weight:bold;">Celsius</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    gas = data.get("gas_level", 0)
                    status = "STABLE" if gas < 400 else "ANOMALY"
                    # Glow color changes based on status
                    glow_color = "rgba(40, 167, 69, 0.5)" if status == "STABLE" else "rgba(220, 53, 69, 0.6)"
                    status_text_color = "#28a745" if status == "STABLE" else "#dc3545"
                    
                    st.markdown(f'''
                        <div class="metric-card" style="box-shadow: 0 0 20px {glow_color}; border-color: {status_text_color};">
                            <h3>SYSTEM STATUS</h3>
                            <p style="font-size:3rem; color:{status_text_color}; font-weight:bold; text-shadow: 0 0
