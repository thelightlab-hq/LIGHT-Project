import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

#Website Layout Theme
st.set_page_config(page_title="L.I.G.H.T.", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Individual Device Cards with Soft Glow */
    .device-container {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }
    
    .unit-id-badge {
        background-color: #000000;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

#Firebase Bridge
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_key"]))
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

#Multi-Device Dashboard
st.title("Project L.I.G.H.T.")
st.caption("Food Bacteria Detector")
st.divider()

#Gather Data From Firebase Root
network_data = db.reference("/").get()

if network_data:
    #Overlap Security
    for device_id, data in network_data.items():
        #Declining Other Data
        if not isinstance(data, dict): continue
        
        #Specific Device ID
        with st.container():
            st.markdown(f"### <span class='unit-id-badge'>UNIT ID: {device_id}</span>", unsafe_allow_html=True)
            
            #Layout Columns
            col_l, col_c, col_r = st.columns([1, 2, 1])
            
            with col_l:
                # Unique Differentiated Data
                st.metric(label="MQ-2 Gas Sensor", value=f"{data.get('gas_level', 0)} ppm")
                st.metric(label="Status", value=data.get('status', 'Online'))

            with col_c:
                #Symbol
                st.markdown(f"""
                    <div style='text-align: center; padding: 20px; border: 1px solid #EEE; border-radius: 10px;'>
                        <div style='width: 120px; height: 100px; background: #333; margin: auto; border: 3px solid #AAA;'></div>
                        <p style='margin-top: 10px; color: #666;'>Polycarbonate Prototype</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_r:
                temp = data.get('temp_level', 22)
                st.metric(label="Internal Temp", value=f"{temp}°C")
                # Automated Safety Logic
                gas_val = data.get('gas_level', 0)
                safety = "SAFE" if gas_val < 400 else "SPOILAGE RISK"
                st.metric(label="Safety Level", value=safety)
            
            st.divider()
else:
    st.info("Searching for active L.I.G.H.T. units... Please ensure your ESP32 is powered on.")
