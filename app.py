import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. UI SETTINGS & DARK CARTOONY CSS ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Deep Black Background */
    .stApp { background-color: #000000; }
    
    /* Massive White Title with Neon Glow */
    .neon-title {
        color: #ffffff;
        font-size: 90px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 12px;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.5), 0 0 30px #0fa;
    }

    /* THE CARDS: Dark background with Bold Light-Gray/White outlines */
    .metric-card {
        background-color: #0e1117; /* Dark Grey/Blue internal */
        border-radius: 25px;
        padding: 35px;
        color: #ffffff;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        /* BOLD OUTLINE - Thick Light Gray */
        border: 5px solid #d1d1d1; 
        
        /* Neon Drop Shadow */
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.2); 
    }

    .metric-value {
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    h3 {
        color: #d1d1d1 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE AUTH ---
if not firebase_admin._apps:
    try:
        # Use your Streamlit Secrets key
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
            # Targeting UNIT_01 exclusively
            data = db.reference("/UNIT_01").get()
            if data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #ffffff;">
                            <h3>GAS LEVEL</h3>
                            <p class="metric-value">{data.get("gas_level", 0)}</p>
                            <p style="font-weight:bold; color: #0fa;">ppm</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #d1d1d1;">
                            <h3>TEMPERATURE</h3>
                            <p class="metric-value">{data.get("temp_level", 0)}°</p>
                            <p style="font-weight:bold; color: #0fa;">Celsius</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    gas = data.get("gas_level", 0)
                    status = "STABLE" if gas < 400 else "ANOMALY"
                    status_color = "#00ffaa" if status == "STABLE" else "#ff4b4b"
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: {status_color};">
                            <h3>STATUS</h3>
                            <p style="font-size:3.5rem; color:{status_color}; font-weight:900;">{status}</p>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.warning("Waiting for UNIT_01 to send data...")
        except:
            st.error("Lost connection to Firebase.")
        time.sleep(5)
