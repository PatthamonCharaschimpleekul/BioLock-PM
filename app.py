import streamlit as st
import pandas as pd
import numpy as np
from predictive_engine import predict_filter_safety as pfs

#configuration
st.set_page_config(page_title="BioLock PM Simulation", page_icon="😶‍🌫️🍀", layout="wide")
st.title("🌿 BioLock-PM: Intelligent Airflow & Safety Simulator")
st.markdown("""This dashboard uses a **Support Vector Regressor (SVR)** to predict the aerodynamic impact 
of natural fiber filters on AC units.""")

#sidebar / input
st.sidebar.header("Filter Configuration")

#user input
v_input = st.sidebar.slider("Air velocity (m/s)", 1.0, 5.0, 2.5)
t_input = st.sidebar.slider("Filter Thickness (cm)", 1.0,5.0,2.0)/100 #convert to metres
k_input = st.sidebar.selectbox("Fiber Packing Density (Permeability) ",
                               options=[1.0e-9, 5.0e-9, 1.0e-8],
                               format_func=lambda x: "High Density" if x == 1.0e-9 else "Low Density")

#prediction logic
predicted_dp = pfs(v_input, k_input, t_input)

#visualization
st.subheader("Real-time Safety Analysis")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Predicted Pressure Drop", value=f"{predicted_dp:.2f} Pa")

with col2:
    if predicted_dp < 50:
        st.success("✅ STATUS: SAFE")
        st.write("The AC compressor is operating within normal thermal safety margins.")
    else:
        st.error("⚠️ STATUS: CRITICAL")
        st.write("Pressure drop is too high! This may cause overheating. Activate Bypass Valve.")

# --- ADDING VALUE (MANAGEMENT ENGINEERING) ---
st.divider()
st.subheader("Environmental Impact (Estimated)")
# Simple logic: 1cm of filter traps ~150mg of PM2.5 per month (estimated)
captured_pm = (t_input * 100) * 150 
st.info(f"By using this filter, you are sequestrating approximately **{captured_pm:.1f} mg** of PM2.5 into cement matrix per month.")

st.markdown("---")
st.caption("Developed by Patthamon Charaschimpleekul | AI & Management Engineering")
