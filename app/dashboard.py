import streamlit as st
import pandas as pd
import plotly.express as px

def dashboard_page():

    st.markdown("<h1 style='text-align:center;'>💚 Health Dashboard</h1>", unsafe_allow_html=True)

    # LOAD DATA
    df = pd.read_csv("outputs/anomaly_results.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # METRICS
    total = len(df)
    anomalies = len(df[df['severity'] != "normal"])
    avg_hr = df['heart_rate_bpm'].mean()
    avg_spo2 = df['spo2_pct'].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", total)
    col2.metric("Anomalies", anomalies)
    col3.metric("Avg HR", round(avg_hr,1))
    col4.metric("Avg SpO2", round(avg_spo2,1))

    # GRAPH
    st.subheader("📈 Heart Rate Trend")

    fig = px.line(
        df,
        x="timestamp",
        y="heart_rate_bpm",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🧠 HEALTH INSIGHTS
    st.subheader("🧠 Health Suggestions")

    if avg_hr > 100:
        st.warning("⚠️ High heart rate → reduce stress, rest more.")
    elif avg_hr < 60:
        st.warning("⚠️ Low heart rate → improve nutrition.")
    else:
        st.success("✅ Heart rate is normal.")

    if df['steps'].mean() < 3000:
        st.warning("🚶 Walk more (6000–8000 steps recommended).")
    else:
        st.success("💪 Good activity level!")

    if avg_spo2 < 95:
        st.warning("⚠️ Low oxygen level detected.")
    else:
        st.success("✅ Oxygen level is healthy.")

    # NAVIGATION
    if st.button("⬅ Back to Input"):
        st.session_state.page = "input"
        st.rerun()