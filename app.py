import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
from datetime import datetime

#CSS Layout & Website Interior
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* Title Styling */
    .neon-title {
        color: #ffffff !important;
        text-decoration: none !important;
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 15px;
        text-shadow: 0 0 20px #0fa;
        margin-bottom: 0px;
    }

    /* Card Styling - Fixed alignment and glow */
    .metric-card {
        background-color: #111111; 
        border-radius: 25px;
        padding: 30px;
        color: #ffffff !important;
        text-align: center;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 6px solid #d1d1d1; 
        transition: all 0.5s ease-in-out;
    }

    /* Removing the "Link" look from text */
    .metric-card h3, .metric-card p {
        color: #ffffff !important;
        text-decoration: none !important;
        margin: 5px 0px;
    }

    .metric-value {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1;
    }

    .status-label {
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

#Firebase Connection
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"Firebase Error: {e}")

st.markdown('<p class="neon-title">L.I.G.H.T.</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#d1d1d1; letter-spacing:5px; margin-bottom:30px;">REAL-TIME MONITORING SYSTEM</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            #Data Fetcher
            data = db.reference("/UNIT_01").get()
            
            if data:
                gas_val = data.get("gas_level", 0)
                temp_val = data.get("temp_level", 0)
                
                #Gas Indicator
                gas_status = "CLEAN" if gas_val < 400 else "CONTAMINATED"
                gas_glow = "#00ffaa" if gas_status == "CLEAN" else "#ff4b4b"
                
                #Temperature Indicator
                if temp_val < 28:
                    temp_status, temp_glow = "COLD", "#00ccff"
                elif 28 <= temp_val < 35:
                    temp_status, temp_glow = "WARM", "#ffcc00"
                else:
                    temp_status, temp_glow = "HOT", "#ff4b4b"
                
                #Final Judger
                overall_status = "STABLE" if (gas_val < 400 and temp_val < 35) else "ANOMALY"
                overall_glow = "#00ffaa" if overall_status == "STABLE" else "#ff4b4b"

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f'<div class="metric-card" style="border-color:{gas_glow}; box-shadow: 0 0 20px {gas_glow}44;"><h3>GAS</h3><p class="metric-value">{gas_val}</p><p style="color:{gas_glow};" class="status-label">{gas_status}</p></div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f'<div class="metric-card" style="border-color:{temp_glow}; box-shadow: 0 0 20px {temp_glow}44;"><h3>TEMP</h3><p class="metric-value">{temp_val}°</p><p style="color:{temp_glow};" class="status-label">{temp_status}</p></div>', unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f'<div class="metric-card" style="border-color:{overall_glow}; box-shadow: 0 0 20px {overall_glow}44;"><h3>STATUS</h3><p style="font-size:3rem; color:{overall_glow}; font-weight:900;">{overall_status}</p></div>', unsafe_allow_html=True)
            
            else:
                #Device disconnection warning
                st.warning("DEVICE DISCONNECTED: UNIT_01 is offline.")
                
        except Exception as e:
            st.error("DATABASE ERROR: Check your internet connection or Firebase Rules.")
        
        time.sleep(5)
