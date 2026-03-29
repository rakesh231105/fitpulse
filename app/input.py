import streamlit as st
import pandas as pd
import os

def input_page():

    st.markdown("<h2>📥 Enter Fitness Data</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date")
        time = st.time_input("Time")
        hr = st.number_input("Heart Rate", 30, 200)

    with col2:
        steps = st.number_input("Steps", 0, 50000)
        spo2 = st.number_input("SpO2", 80, 100)

    if st.button("Submit"):

        timestamp = f"{date} {time}"

        new = pd.DataFrame([{
            "timestamp": timestamp,
            "heart_rate_bpm": hr,
            "steps": steps,
            "spo2_pct": spo2,
            "severity": "normal"
        }])

        path = "outputs/anomaly_results.csv"

        if os.path.exists(path):
            df = pd.read_csv(path)
            df = pd.concat([df, new], ignore_index=True)
        else:
            df = new

        df.to_csv(path, index=False)

        st.success("Data saved!")

    if st.button("Go to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()