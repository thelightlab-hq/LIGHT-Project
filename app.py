import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

#Layout & Appearance
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    .neon-title {
        color: #ffffff !important;
        font-size: 60px !important; 
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 10px;
        text-shadow: 0 0 15px #0fa;
        margin-bottom: 0px;
    }

    /*Borders*/
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
        font-size: 3.2rem; /* Adjusted for decimal space */
        font-weight: 900;
        line-height: 1.2;
        margin: 5px 0;
    }

    .status-label {
        font-size: 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /*Achor Links from Header Remover*/
    button[kind="header"] { display: none; }
    .stMarkdown h3 a, .stMarkdown h2 a, .stMarkdown h1 a { display: none !important; }
    [data-testid="stHeader"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

#Firebase Bridge
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
            #Data Checking
            data = db.reference("/UNIT_01").get()
            
            if data is not None:
                # Raw data with two decimals
                gas_val = float(data.get("gas_level", 0))
                temp_val = float(data.get("temp_level", 0))
                
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
                
                #Final Judge Indicator
                overall_status = "STABLE" if (gas_val < 400 and temp_val < 35) else "ANOMALY"
                overall_glow = "#00ffaa" if overall_status == "STABLE" else "#ff4b4b"

                col1, col2, col3 = st.columns(3)
                
                #Decimal Places
                with col1:
                    st.markdown(f'<div class="metric-card" style="border-color:{gas_glow}; box-shadow: 0 0 20px {gas_glow}44;"><div class="card-header">GAS</div><div class="metric-value">{gas_val:.2f}</div><div style="color:{gas_glow};" class="status-label">{gas_status}</div></div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f'<div class="metric-card" style="border-color:{temp_glow}; box-shadow: 0 0 20px {temp_glow}44;"><div class="card-header">TEMP</div><div class="metric-value">{temp_val:.2f}°</div><div style="color:{temp_glow};" class="status-label">{temp_status}</div></div>', unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f'<div class="metric-card" style="border-color:{overall_glow}; box-shadow: 0 0 20px {overall_glow}44;"><div class="card-header">STATUS</div><div style="font-size:2.8rem; color:{overall_glow}; font-weight:900; margin-top:10px;">{overall_status}</div></div>', unsafe_allow_html=True)
            
            else:
                #Disconnection of UNIT_01 Warning
                st.write("")
                st.error("OFFLINE: Device is disconnected. Waiting for connection...")
                
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
        
        #Refresh rate
        time.sleep(7)
