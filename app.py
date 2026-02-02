import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. UI SETUP ---
st.set_page_config(page_title="L.I.G.H.T. Monitoring System", layout="wide")
st.title("Project L.I.G.H.T. Dashboard")

# --- 2. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        # Reconstructing the key dictionary from your provided secret
        # This fixes the 'Line 48' error by correctly mapping the JSON fields
        key_dict = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["client_email"],
            "token_uri": st.secrets["token_uri"],
        }
        
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"⚠️ Secret Key Error: {e}. Check your Streamlit Secrets.")

# --- 3. THE NO-OVERLAP LOOP ---
# This looks at the ROOT of your database
all_units = db.reference("/").get()

if all_units:
    # Iterate through every 'folder' in Firebase (e.g., UNIT_01, UNIT_02)
    for unit_id, data in all_units.items():
        # This check ensures we only process folders with sensor data
        if isinstance(data, dict):
            with st.container():
                st.markdown(f"### 📡 Unit ID: **{unit_id}**")
                
                # Display metrics in a professional grid
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    gas = data.get('gas_level', 0)
                    st.metric("Gas Concentration", f"{gas} ppm")
                
                with col2:
                    temp = data.get('temp_level', 0)
                    st.metric("Internal Temperature", f"{temp}°C")
                
                with col3:
                    # Safety logic based on your 11-STEM 2 parameters
                    if gas < 400:
                        st.success("✅ STATUS: STABLE")
                    else:
                        st.error("🚨 STATUS: ANOMALY")
                
                st.divider() # Keeps different units visually separated
else:
    st.warning("No active L.I.G.H.T. units detected in the database.")
