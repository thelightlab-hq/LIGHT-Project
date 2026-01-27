import streamlit as st
import pandas as pd
import numpy as np

#Header
st.set_page_config(page_title="Project L.I.G.H.T", 
layout="wide")

#Layout Design
st.markdown("""
  <style>
  .stApp{background-color: #000000; color: #FFFFFF;}
  h1, h2, h3{color: #FFFFFF;}

  div[data-testid="stMetric"]{
     background-color: #1A1A1A:
     border: 1px solid #4D4D4D;
     padding: 15px;
     border-radius: 10px;
  }
  div[data-testid="stMetricValue"]{color: #FFFFFF;}
  div[data-testid+"stMetricLabel]{color: #B3B3B3;}

  .stButton>button{
     background-color: #333333;
     color: white;
     border: 1px solid #FFFFFF;
  }
  .stButton.button:hover{
     background-color: #FFFFFF;
     color: black;
  }
  </style>
  """, unsafe_allow_html=True)

st.title("Project L.I.G.H.T.")
st.write("Food Bacteria Sensor Dashboard")

#Dashboard Widget
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="GAS LEVEL (VOC)", value="0.04 PPM")

with col2:
    st.metric(label="AMBIENT TEMP", value="28.5°C")

with col3:
    st.metric(label="FOOD THERMAL", value="39.2°C")

st.markdown("---") # Gray divider line

#Thermal Imaging
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("THERMAL FEED")
    st.write("Scanning Hotspots...")
    thermal_data = np.random.rand(10, 10)
   
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Paloma_thermal_image.jpg/640px-Paloma_thermal_image.jpg", 
             caption="Thermal Signature Detected", use_container_width=True)

with col_right:
    st.subheader("SENSOR LOGS")
  
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Gas', 'Ambient', 'Food']
    )
    st.line_chart(chart_data)

#Buttons
st.subheader("SYSTEM CONTROLS")
btn_col1, btn_col2 = st.columns(2)
if btn_col1.button('START SENSOR SCAN', use_container_width=True):
    st.info("System initializing...")
if btn_col2.button('RESET SYSTEM', use_container_width=True):
    st.write("Sensors cleared.")