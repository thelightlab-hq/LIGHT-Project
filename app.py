import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

#Firebase Bridge for Hardware Connection
DB_URL ="https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"

st.markdown("""
    <style>
    /* Background and font */
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #000000 !important; font-family: 'Helvetica', sans-serif; }
    
    /* The Gray Metric Cards */
    [data-testid="stMetric"] {
        background-color: #F8F9FA; 
        border: 1px solid #E0E0E0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricLabel"] { color: #616161; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #000000; }
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

