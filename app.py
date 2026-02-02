import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. THEME & UI ---
st.set_page_config(page_title="L.I.G.H.T. Network", layout="wide")
st.markdown("<style>.stApp { background-color: #FFFFFF; }</style>", unsafe_allow_html=True)

# --- 2. SECURE FIREBASE CONNECTION ---
if not firebase_admin._apps:
    # This dictionary contains the secret key you sent earlier
    firebase_creds = {
        "type": "service_account",
        "project_id": "light-40317",
        "private_key_id": "3770ac85dc5b83de8aa8d537eb9a5d7cb7438ee7",
        "private_key": st.secrets["private_key"].replace('\\n',[firebase_key]
type = "service_account"
project_id = "light-40317"
private_key_id = "3770ac85dc5b83de8aa8d537eb9a5d7cb7438ee7"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCmjnTVmiysps22\nK2iON5mTU7JaVmVqQVuzh+fGIVbBuIXNTEnnpQS9FqS3D5GYYqaYD+OwObpvGtxA\niBrmBMy3abA+tZOiVllWoI6NlYsSAUzHNL4ktlBbNHTAiSFwLrJUn4mG/4Sv44+C\nw1fZjBI63asro6lm0ihA10ydKQ+/X9nUKZiJ9CPdLhu6cxtLPWK4TZc+Rd3qWegI\ndS1/op/xwiCy+iqp8zIgufz5GwgiADPo7Kmp6ks10iyZL3/6w+2yPUXC+xy56kaw\nMnYTfzylHgeKQlpo36simYQlH+4dZDGNc8JDjEnX/9Dp8/BH9wv2aQ8Ea5LcR626\n6kGXGhNFAgMBAAECggEABNDjsfV2Szu7gQP6Tvpul2L5KkGLRypCo4tPeVwnbQyP\n2eLV1DviSjFoa96oYBaiKI11EPhqWqIVMkx9Mp965+bHcNjBPxVuGeIknRVw4wFk\nnfH5eYhIBIscwSB19g9zmpzOVjf3NzrGQIqzdJfnQwp705Q05sM25MEU9wpj6S2p\nYOieByHtT/XJjoVQA2lLlDJbX8xcrsCZIa7f+w5kWrhCkSoJOrHJwxotle0k2FJI\nb90ByM1ac3b9+OvZMPB2GXfq2PE/z1dJUTbpm36MUfBPjW9FCrOiNL1xsXBRiJt4\nWIHv5yOahnM0LTZt0c5wzVOHxbsQvrTJVsUMIQ2d4QKBgQDbp/1Fow0nn1rDd3q4\nZwRGibArKfGGY0qzdxCrNH0sg8cPsGMcRgi88QtxmR9hGTHcLzNbPcLcy8esYjZn\n+ygawLRQ7e1waG/S6XYsn/KD6rMMfdFQ0wqkRXWR3vPOLrMT5C7YLhEUPkHC2089\nQosDHNzyPNmuyfo25cp0YJcPmQKBgQDCHVBEWIVjd6GyMQVIc2EZR1hyrY9P8mt9\nNan96Y8sOIlHqksUxqp/VT7dfznTarsOnupkd+NyFha8NRsfL+Izrdn4F+k7TSRx\n0T3dUpDvPV9L3kOVASOpvBcN2UlO9F2AAu6rhp7ItXkSuqtQgc6R3WuKtZ/gUdv7\nA0YL4dfcjQKBgQCXCOiu5FGcSAd51gLNHxCii/RVia6oUEfCJQGSJzJW1HmgwRE1\nFLbXbAsJXldkRZWyJ8ZxW4NMnNY8Iv/z+Y927cBO0XrtSvJxHNSEFKsFp/DbivvN\nTn/HuncACUStJhE+gSzwuqRFvhUrre7LWaEKT+NgsRShCgKBkvnlkbDtKQKBgDyc\nyqOMwJn+kQ8DH5Mv8/HgxU2JxGZCXC4Mw7f1Zi94t+UY17j1D+gSxj6Dq5rIiQBX\nvvkANpU5MIA0VPO4D/nzH0zIqptJy0d+/sJNNdR+ZXNbQ98TK/+kK863Opzc0RVX\n1Q7aSlqBz/x5LWVGIyqI6Tu22uVAqmAG9ahgLPdBAoGAJVT53p0kM3O7ogptZ6jF\nF4M6qw6Z5c47N/m6CEDrXR8kfDbptvjjTYoy3L3tBI74YS33mxNarpuQf90OCL4S\ntl+to4x83WtSBGjahIE/fXPTAeJx16pPioHaXBdsmgY1bJIG+9ZVy8DtyNow1zr9\njABhQGbVviHmvU4dSv3wVrM=\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-fbsvc@light-40317.iam.gserviceaccount.com"
client_id = "112988571583883113259"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40light-40317.iam.gserviceaccount.com"
universe_domain = "googleapis.com" '\n'),
        "client_email": "firebase-adminsdk-fbsvc@light-40317.iam.gserviceaccount.com",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://light-40317-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

# --- 3. DYNAMIC MULTI-UNIT DASHBOARD ---
st.title("Project L.I.G.H.T. Real-time Network")
st.write("Automatically detecting localized inspection units...")

all_data = db.reference("/").get()

if all_data:
    for device_id, sensors in all_data.items():
        if isinstance(sensors, dict):
            with st.expander(f"📟 UNIT: {device_id}", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gas Level", f"{sensors.get('gas_level', 0)} ppm")
                with col2:
                    st.metric("Temperature", f"{sensors.get('temp_level', 0)}°C")
                with col3:
                    gas = sensors.get('gas_level', 0)
                    status = "✅ SAFE" if gas < 400 else "⚠️ ANOMALY"
                    st.subheader(status)
else:
    st.warning("No hardware units detected. Please check your ESP32.")


