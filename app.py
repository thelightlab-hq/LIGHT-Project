import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# CSS CODES FOR THEME - Enhanced with 3-way color logic
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    .neon-title {
        color: #ffffff;
        font-size: 100px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 15px;
        text-shadow: 0 0 20px #0fa;
        margin-bottom: 0px;
    }

    .metric-card {
        background-color: #111111; 
        border-radius: 25px;
        padding: 40px;
        color: #ffffff;
        text-align: center;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 6px solid #d1d1d1; 
        transition: all 0.5s ease-in-out;
    }

    .metric-value {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 0px;
    }

    .status-label {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 10px;
        text-transform: uppercase;
    }
    
    h3 { color: #ffffff !important; letter-spacing: 3px; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# FIREBASE VERIFICATION
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"Firebase Error: {e}")

# LAYOUT
st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)
st.markdown('<p class="system-sub" style="text-align:center; color:#d1d1d1; letter-spacing:5px;">REAL-TIME MONITORING</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = db.reference("/UNIT_01").get()
            if data:
                gas_val = data.get("gas_level", 0)
                temp_val = data.get("temp_level", 0)
                
                # --- GAS LOGIC ---
                gas_status = "CLEAN" if gas_val < 400 else "CONTAMINATED"
                gas_glow = "#00ffaa" if gas_status == "CLEAN" else "#ff4b4b"
                
                # --- TEMP LOGIC (Cold, Warm, Hot) ---
                if temp_val < 28:
                    temp_status = "COLD"
                    temp_glow = "#00ccff" # Blue
                elif 28 <= temp_val < 35:
                    temp_status = "WARM"
                    temp_glow = "#ffcc00" # Yellow/Gold
                else:
                    temp_status = "HOT"
                    temp_glow = "#ff4b4b" # Red
                
                # --- OVERALL STATUS ---
                overall_status = "STABLE" if (gas_val < 400 and temp_val < 35) else "ANOMALY"
                overall_glow = "#00ffaa" if overall_status == "STABLE" else "#ff4b4b"

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="metric-card" style="border-color:{gas_glow}; box-shadow: 0 0 25px {gas_glow}55;">
                            <h3>GAS</h3>
                            <p class="metric-value">{gas_val}</p>
                            <p style="color:{gas_glow};" class="status-label">{gas_status}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"""
                        <div class="metric-card" style="border-color:{temp_glow}; box-shadow: 0 0 25px {temp_glow}55;">
                            <h3>TEMP</h3>
                            <p class="metric-value">{temp_val}°</p>
                            <p style="color:{temp_glow};" class="status-label">{temp_status}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f"""
                        <div class="metric-card" style="border-color:{overall_glow}; box-shadow: 0 0 25px {overall_glow}55;">
                            <h3>STATUS</h3>
                            <p style="font-size:3.5rem; color:{overall_glow}; font-weight:900; margin-top:20px;">{overall_status}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Awaiting Stream from UNIT_01...")
        except Exception as e:
            st.error(f"Connection Error: {e}")
        
        time.sleep(5)



