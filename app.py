import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. UI SETTINGS & BOLD CARTOONY CSS ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Pure White Background */
    .stApp { background-color: #ffffff; }
    
    /* Bold Title with subtle glow */
    .neon-title {
        color: #000000;
        font-size: 90px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 12px;
        margin-bottom: 5px;
        text-shadow: 3px 3px 0px rgba(0, 255, 170, 0.2);
    }

    /* THE CARDS: Thicker borders and bold rounded corners */
    .metric-card {
        background-color: #ffffff; 
        border-radius: 25px; /* More rounded like the picture */
        padding: 35px;
        color: #000000;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        /* BOLD OUTLINE - Thicker and Darker Gray */
        border: 4px solid #333333; 
        
        /* Clean Shadow for depth */
        box-shadow: 8px 8px 0px rgba(0, 0, 0, 0.05); 
    }

    .metric-value {
        font-size: 4rem;
        font-weight: 900;
        color: #000000;
    }
    
    h3 {
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
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
            # Targeting only UNIT_01
            data = db.reference("/UNIT_01").get()
            if data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #00d4ff; box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);">
                            <h3>GAS LEVEL</h3>
                            <p class="metric-value">{data.get("gas_level", 0)}</p>
                            <p style="font-weight:bold;">ppm</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: #00ffaa; box-shadow: 0 0 20px rgba(0, 255, 170, 0.2);">
                            <h3>TEMPERATURE</h3>
                            <p class="metric-value">{data.get("temp_level", 0)}°</p>
                            <p style="font-weight:bold;">Celsius</p>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    gas = data.get("gas_level", 0)
                    status = "STABLE" if gas < 400 else "ANOMALY"
                    status_color = "#28a745" if status == "STABLE" else "#dc3545"
                    st.markdown(f'''
                        <div class="metric-card" style="border-color: {status_color}; box-shadow: 0 0 25px {status_color}44;">
                            <h3>STATUS</h3>
                            <p style="font-size:3.5rem; color:{status_color}; font-weight:900;">{status}</p>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.warning("No data found for UNIT_01.")
        except:
            st.error("Connection Error")
        time.sleep(5)
