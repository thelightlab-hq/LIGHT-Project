import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
from datetime import datetime

#Layouts
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    .stApp { background-color: #000000; }
    
    .neon-title {
        color: #ffffff !important;
        font-size: 60px !important; 
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px;
        text-shadow: 0 0 15px #0fa;
        margin-top: -20px;
        margin-bottom: 0px;
    }

    .metric-card {
        background-color: #111111; 
        border-radius: 20px;
        padding: 25px;
        color: #ffffff !important;
        text-align: center;
        min-height: 280px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 5px solid #d1d1d1; 
        transition: all 0.5s ease;
    }

    .card-header {
        font-size: 1.5rem; 
        font-weight: 800;
        letter-spacing: 2px;
        color: #ffffff !important;
    }

    .metric-value {
        font-size: 3.2rem; 
        font-weight: 900;
        line-height: 1.2;
        margin: 5px 0;
    }

    button[kind="header"] { display: none; }
    .stMarkdown h3 a, .stMarkdown h2 a, .stMarkdown h1 a { display: none !important; }
    [data-testid="stHeader"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

#Firebase
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
st.markdown('<p style="text-align:center; color:#d1d1d1; letter-spacing:5px; margin-bottom:20px;">REAL-TIME MONITORING SYSTEM</p>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            #Data from Firebase
            ref = db.reference("/UNIT_01")
            data = ref.get()
            
        
            is_offline = True
            if data:
                #Real-time Update Disconnection
                gas_val = float(data.get("gas_level", 0))
                temp_val = float(data.get("temp_level", 0))
                is_offline = False 

            if not is_offline:
                #Indicators
                gas_status = "CLEAN" if gas_val < 400 else "CONTAMINATED"
                gas_glow = "#00ffaa" if gas_status == "CLEAN" else "#ff4b4b"
                
                if temp_val < 28:
                    temp_status, temp_glow = "COLD", "#00ccff"
                elif 28 <= temp_val < 35:
                    temp_status, temp_glow = "WARM", "#ffcc00"
                else:
                    temp_status, temp_glow = "HOT", "#ff4b4b"
                
                overall_status = "STABLE" if (gas_val < 400 and temp_val < 35) else "ANOMALY"
                overall_glow = "#00ffaa" if overall_status == "STABLE" else "#ff4b4b"

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<div class="metric-card" style="border-color:{gas_glow}; box-shadow: 0 0 20px {gas_glow}44;"><div class="card-header">GAS</div><div class="metric-value">{gas_val:.2f}</div><div style="color:{gas_glow}; font-weight:700;">{gas_status}</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-card" style="border-color:{temp_glow}; box-shadow: 0 0 20px {temp_glow}44;"><div class="card-header">TEMP</div><div class="metric-value">{temp_val:.2f}°</div><div style="color:{temp_glow}; font-weight:700;">{temp_status}</div></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="metric-card" style="border-color:{overall_glow}; box-shadow: 0 0 20px {overall_glow}44;"><div class="card-header">STATUS</div><div style="font-size:2.8rem; color:{overall_glow}; font-weight:900; margin-top:10px;">{overall_status}</div></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p style="text-align:center; color:#ffffff; font-weight:700; letter-spacing:2px;">● DEVICE ONLINE: UNIT_01 CONNECTED</p>', unsafe_allow_html=True)
            
            else:
                #Device Status Indicator
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                st.markdown('<p style="text-align:center; color:#ff4b4b; font-weight:900; letter-spacing:2px; font-size:1.5rem; border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px;">DEVICE OFFLINE: WAITING FOR UNIT_01 CONNECTION...</p>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
        
        time.sleep(7)
