import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. THEME & UI ---
st.set_page_config(page_title="L.I.G.H.T. Dashboard", layout="wide")

# White, Gray, Black Theme
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .device-box {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        # Building the credentials from your secrets
        # The .replace() ensures your private key is read correctly by Python
        key_dict = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"].replace("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCmjnTVmiysps22\nK2iON5mTU7JaVmVqQVuzh+fGIVbBuIXNTEnnpQS9FqS3D5GYYqaYD+OwObpvGtxA\niBrmBMy3abA+tZOiVllWoI6NlYsSAUzHNL4ktlBbNHTAiSFwLrJUn4mG/4Sv44+C\nw1fZjBI63asro6lm0ihA10ydKQ+/X9nUKZiJ9CPdLhu6cxtLPWK4TZc+Rd3qWegI\ndS1/op/xwiCy+iqp8zIgufz5GwgiADPo7Kmp6ks10iyZL3/6w+2yPUXC+xy56kaw\nMnYTfzylHgeKQlpo36simYQlH+4dZDGNc8JDjEnX/9Dp8/BH9wv2aQ8Ea5LcR626\n6kGXGhNFAgMBAAECggEABNDjsfV2Szu7gQP6Tvpul2L5KkGLRypCo4tPeVwnbQyP\n2eLV1DviSjFoa96oYBaiKI11EPhqWqIVMkx9Mp965+bHcNjBPxVuGeIknRVw4wFk\nnfH5eYhIBIscwSB19g9zmpzOVjf3NzrGQIqzdJfnQwp705Q05sM25MEU9wpj6S2p\nYOieByHtT/XJjoVQA2lLlDJbX8xcrsCZIa7f+w5kWrhCkSoJOrHJwxotle0k2FJI\nb90ByM1ac3b9+OvZMPB2GXfq2PE/z1dJUTbpm36MUfBPjW9FCrOiNL1xsXBRiJt4\nWIHv5yOahnM0LTZt0c5wzVOHxbsQvrTJVsUMIQ2d4QKBgQDbp/1Fow0nn1rDd3q4\nZwRGibArKfGGY0qzdxCrNH0sg8cPsGMcRgi88QtxmR9hGTHcLzNbPcLcy8esYjZn\n+ygawLRQ7e1waG/S6XYsn/KD6rMMfdFQ0wqkRXWR3vPOLrMT5C7YLhEUPkHC2089\nQosDHNzyPNmuyfo25cp0YJcPmQKBgQDCHVBEWIVjd6GyMQVIc2EZR1hyrY9P8mt9\nNan96Y8sOIlHqksUxqp/VT7dfznTarsOnupkd+NyFha8NRsfL+Izrdn4F+k7TSRx\n0T3dUpDvPV9L3kOVASOpvBcN2UlO9F2AAu6rhp7ItXkSuqtQgc6R3WuKtZ/gUdv7\nA0YL4dfcjQKBgQCXCOiu5FGcSAd51gLNHxCii/RVia6oUEfCJQGSJzJW1HmgwRE1\nFLbXbAsJXldkRZWyJ8ZxW4NMnNY8Iv/z+Y927cBO0XrtSvJxHNSEFKsFp/DbivvN\nTn/HuncACUStJhE+gSzwuqRFvhUrre7LWaEKT+NgsRShCgKBkvnlkbDtKQKBgDyc\nyqOMwJn+kQ8DH5Mv8/HgxU2JxGZCXC4Mw7f1Zi94t+UY17j1D+gSxj6Dq5rIiQBX\nvvkANpU5MIA0VPO4D/nzH0zIqptJy0d+/sJNNdR+ZXNbQ98TK/+kK863Opzc0RVX\n1Q7aSlqBz/x5LWVGIyqI6Tu22uVAqmAG9ahgLPdBAoGAJVT53p0kM3O7ogptZ6jF\nF4M6qw6Z5c47N/m6CEDrXR8kfDbptvjjTYoy3L3tBI74YS33mxNarpuQf90OCL4S\ntl+to4x83WtSBGjahIE/fXPTAeJx16pPioHaXBdsmgY1bJIG+9ZVy8DtyNow1zr9\njABhQGbVviHmvU4dSv3wVrM=\n-----END PRIVATE KEY-----"),
            "client_email": st.secrets["client_email"],
            "token_uri": st.secrets["token_uri"],
        }
        
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")

# --- 3. THE "RESTORED" DASHBOARD LOGIC ---
st.title("Project L.I.G.H.T. Monitoring")
st.write("Localized Inspection using Gas and Heat Thermography")

# This is the "magic" line that finds all your devices at once
all_data = db.reference("/").get()

if all_data:
    # Iterate through each unique device found in Firebase
    for device_id, values in all_data.items():
        # Ensure we are looking at a device folder, not metadata
        if isinstance(values, dict):
            with st.container():
                st.markdown(f"### 📡 Unit ID: {device_id}")
                
                # Create separate columns for metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    gas = values.get('gas_level', 0)
                    st.metric("Gas Level", f"{gas} ppm")
                
                with col2:
                    temp = values.get('temp_level', 0)
                    st.metric("Temperature", f"{temp}°C")
                    
                with col3:
                    # Simple safety logic: adjust the '400' based on your testing
                    if gas < 400:
                        st.success("STATUS: SAFE")
                    else:
                        st.error("STATUS: ANOMALY")
                
                st.divider()
else:
    st.warning("No units detected. Please check if your ESP32 is powered on and connected to WiFi.")
