import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

#Firebase Bridge for Hardware Connection
DB_URL ="https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Soft Neon Floating Cards */
    [data-testid="stMetric"] {
        background-color: #F8F9FA; 
        border: 1px solid #E0E0E0;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.02);
    }

    /* Custom CSS Device Visual (30x30 Unit) */
    .device-box {
        width: 280px;
        height: 280px;
        background: #F8F9FA;
        border: 3px solid #E0E0E0;
        border-radius: 20px;
        margin: auto;
        position: relative;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }
    .device-window {
        width: 200px;
        height: 150px;
        background: #FFFFFF;
        border: 1px solid #EEEEEE;
        margin: 30px auto;
        border-radius: 5px;
    }
    .status-light {
        width: 10px;
        height: 10px;
        background: #00FF00;
        border-radius: 50%;
        position: absolute;
        top: 15px;
        right: 15px;
        box-shadow: 0 0 10px #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_key"]))
    firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})

    st.title("Project L.I.G.H.T.")
    st.subheader("Food Safety Scanning System")

#Real-time Data
try:
    ref = db.reference('mq2_data')
    gas_val = ref.get()

    if gas_val is not None:
        st.metric(label="Current Gas Level (MQ2)", value=f"{gas_val} PPM")
        if gas_val > 400:
            st.error("ALERT: High Gas Level Detected!")
        else:
            st.success("Air Quality is Normal")
    else:
        st.info("System Online: Awaiting data from the microcontroller...")

except Exception as e:

    st.warning("Connect plug in the hardware components to see real-time results.")


