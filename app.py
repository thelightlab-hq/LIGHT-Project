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
    
    /* Massive White Title with Glow */
    .neon-title {
        color: #ffffff;
        font-size: 100px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 15px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.4), 0 0 40px #0fa;
        margin-bottom: 0px;
    }

    .system-sub {
        color: #d1d1d1;
        text-align: center;
        font-size: 22px;
        letter-spacing: 5px;
        margin-bottom: 40px;
    }

    /* THE CARDS: Dark internal, Thick Light-Gray/White borders */
    .metric-card {
        background-color: #111111; 
        border-radius: 25px;
        padding: 40px;
        color: #ffffff;
        text-align: center;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        /* BOLD OUTLINE - Thick and defined */
        border: 6px solid #d1d1d1; 
        box-shadow: 0 0 25px rgba(0, 255, 170, 0.15); 
    }

    .metric-value {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        margin: 10px 0;
    }
    
    h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE AUTH ---
if not firebase_admin._apps:
    try:
        # Pulling from your Streamlit Secrets
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"Handshake Failed: {e}")

# --- 3. UI LAYOUT ---
st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)
st.markdown('<p class="system-sub">REAL-TIME MONITORING</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Targeted fetch for your device only
            data = db.reference("/UNIT_01").get()
            if data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #ffffff;">
                            <h3>GAS</h3>
                            <p class="metric-value">{data.get("gas_level", 0)}</p>
                            <p style="color:#0fa; font-weight:bold;">PPM</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #d1d1d1;">
                            <h3>TEMP</h3>
                            <p class="metric-value">{data.get("temp_level", 0)}°</p>
                            <p style="color:#0fa; font-weight:bold;">CELSIUS</p>
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
                st.info("Awaiting Stream from UNIT_01...")
        except:
            st.error("Database Link Interrupted")
        time.sleep(5)
