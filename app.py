import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="L.I.G.H.T. Monitoring System", layout="wide")

# Custom CSS for the "Neon/Modern" look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #000000;
    }
    
    /* Card Styling */
    .metric-card {
        background-color: #f8f9fa; /* Light Gray */
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #ffffff;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        text-align: center;
        color: #000000;
    }

    /* Neon Glow Effect for Headers */
    .neon-text {
        color: #fff;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #0fa,
            0 0 82px #0fa;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
    }

    /* Custom Metric Text */
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #008080; /* Teal/Neon Blue */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["firebase_key"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except:
        st.error("Check your Streamlit Secrets for the Firebase Key!")

# --- 3. UI HEADER ---
st.markdown('<p class="neon-text">L.I.G.H.T. Monitoring System</p>', unsafe_allow_html=True)
st.divider()

# Placeholder for live updates
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = db.reference("/UNIT_01").get() # Specific to your unit
            
            if data:
                # Top Row: The Gauges/Metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <p style="font-size:1.2rem; color:#666;">GAS CONCENTRATION</p>
                            <p class="metric-value">{data.get('gas_level', 0)} <span style="font-size:1rem;">ppm</span></p>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <p style="font-size:1.2rem; color:#666;">INTERNAL TEMPERATURE</p>
                            <p class="metric-value">{data.get('temp_level', 0)}°C</p>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    status = "STABLE" if data.get('gas_level', 0) < 400 else "ANOMALY"
                    status_color = "#28a745" if status == "STABLE" else "#dc3545"
                    st.markdown(f"""
                        <div class="metric-card" style="border-color: {status_color};">
                            <p style="font-size:1.2rem; color:#666;">SYSTEM STATUS</p>
                            <p style="font-size:2rem; color:{status_color}; font-weight:bold;">{status}</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Space for the Symbol/Image you will send later
                st.write("")
                st.info("💡 Sensor calibration active. Data refreshing every 5 seconds.")
            
            else:
                st.warning("Awaiting Data from ESP32...")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")
        
        time.sleep(5)
