import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

#Layout
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .unit-card {
        background-color: #FBFBFB;
        border: 1px solid #E0E0E0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .status-online { color: #00FF00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

#Firebase Connection
if not firebase_admin._apps:
    # Use your secret key from Streamlit Cloud Secrets
    cred = credentials.Certificate(dict(st.secrets["firebase_key"]))
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

#Differentiation Logic
st.title("Project L.I.G.H.T. Public Network")
st.write("Monitoring localized inspection units in real-time.")

#Fetch Files
all_units = db.reference("/").get()

if all_units:
    #Prevent Overlap
    for unit_id, sensors in all_units.items():
        if not isinstance(sensors, dict): continue
        
        with st.container():
            # Header for each specific device
            st.markdown(f"### 📟 Device ID: **{unit_id}**")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                # Differentiated data: pulls 'temp_level'
                temp = sensors.get('temp_level', 0.0)
                st.metric("Temperature", f"{temp}°C")
            
            with col2:
                # Differentiated data: pulls 'gas_level'
                gas = sensors.get('gas_level', 0)
                st.metric("Gas Anomaly", f"{gas} ppm")
            
            with col3:
                # Safety Logic
                is_safe = "SAFE" if gas < 400 else "DANGER"
                st.subheader(f"Status: {is_safe}")
            
            st.divider() #Separation line
else:
    st.info("No active hardware detected. Check ESP32 connection.")
