import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(layout="wide")

# ===============================
# 🎨 CUSTOM THEME
# ===============================
st.markdown("""
<style>

/* Background */
body {
    background-color: #f7fff9;
}

/* Main container */
.main {
    background-color: white;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    padding: 15px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size:18px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Buttons */
.stButton>button {
    background: #2ecc71;
    color: white;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: #27ae60;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ecfdf5;
}

/* Titles */
h1, h2, h3 {
    color: #27ae60;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# 📂 LOAD DEFAULT DATA
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "outputs", "anomaly_results.csv")

df = pd.read_csv(file_path)

# ===============================
# 📥 SIDEBAR
# ===============================
st.sidebar.title("⚙️ Configuration")

uploaded_file = st.sidebar.file_uploader("Upload Fitness Data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Handle timestamp column safely
    possible_cols = ['timestamp', 'time', 'datetime', 'date']
    found = None

    for col in possible_cols:
        if col in df.columns:
            found = col
            break

    if found:
        df.rename(columns={found: 'timestamp'}, inplace=True)
    else:
        st.error("❌ No timestamp column found in uploaded file")
        st.stop()

# ===============================
# 🧹 CLEAN DATA
# ===============================
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

for col in ['heart_rate_bpm', 'steps', 'spo2_pct']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ===============================
# ❤️ HEADER
# ===============================
st.markdown("""
<h1 style='text-align:center; color:#27ae60;'>
💚 FitPulse Health Monitor
</h1>
""", unsafe_allow_html=True)

# ===============================
# 📅 DATE FILTER
# ===============================
date_range = st.date_input(
    "Select date range",
    [df['timestamp'].min(), df['timestamp'].max()]
)

df = df[
    (df['timestamp'].dt.date >= date_range[0]) &
    (df['timestamp'].dt.date <= date_range[1])
]

# ===============================
# 📊 METRICS
# ===============================
total = len(df)
anomalies = len(df[df['severity'] != "normal"]) if 'severity' in df.columns else 0
high = (df['severity'] == 'high').sum() if 'severity' in df.columns else 0

avg_hr = df['heart_rate_bpm'].mean()
avg_spo2 = df['spo2_pct'].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(f"<div class='metric-card'>📊 Total<br>{total:,}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'>⚠️ Anomalies<br>{anomalies:,}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'>🔴 High<br>{high}</div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card'>❤️ Avg HR<br>{avg_hr:.1f}</div>", unsafe_allow_html=True)
col5.markdown(f"<div class='metric-card'>🩸 SpO2<br>{avg_spo2:.1f}%</div>", unsafe_allow_html=True)

# ===============================
st.subheader("🧠 Health Insights & Recommendations")

recommendations = []

# Heart Rate
if avg_hr > 100:
    recommendations.append("⚠️ High heart rate detected. Try relaxation, breathing exercises, or consult a doctor.")
elif avg_hr < 60:
    recommendations.append("⚠️ Low heart rate detected. Ensure proper nutrition and check with a physician.")
else:
    recommendations.append("✅ Heart rate is in a healthy range.")

# Steps
if 'steps' in df.columns:
    avg_steps = df['steps'].mean()
    if avg_steps < 3000:
        recommendations.append("🚶 You should walk more. Aim for at least 6000–8000 steps daily.")
    elif avg_steps < 7000:
        recommendations.append("👍 Good activity, but increasing steps will improve fitness.")
    else:
        recommendations.append("💪 Excellent step count! Keep it up.")

# SpO2
if avg_spo2 < 95:
    recommendations.append("⚠️ Low oxygen levels detected. Consider medical advice.")
else:
    recommendations.append("✅ Oxygen levels are normal.")

# Display
for rec in recommendations:
    st.success(rec)
# 📈 HEART RATE GRAPH
# ===============================
fig = px.scatter(
    df,
    x="timestamp",
    y="heart_rate_bpm",
    color="severity",
    title="Heart Rate Analysis",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
# ===============================
# 📊 DAILY ANOMALY RATE
# ===============================
if 'severity' in df.columns:
    df['date'] = df['timestamp'].dt.date

    daily = df.groupby('date')['severity'].apply(
        lambda x: (x != 'normal').mean()*100
    ).reset_index(name='rate')

    fig2 = px.bar(daily, x='date', y='rate',
                  title="Daily Anomaly Rate (%)",
                  template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)

# ===============================
# 🥧 PIE CHART
# ===============================
types = {
    "Tachycardia": (df['heart_rate_bpm'] > 120).sum(),
    "Bradycardia": (df['heart_rate_bpm'] < 45).sum(),
    "Low SpO2": (df['spo2_pct'] < 94).sum(),
}

pie_df = pd.DataFrame({
    "Type": list(types.keys()),
    "Count": list(types.values())
})

fig3 = px.pie(pie_df, names='Type', values='Count',
              title="Anomaly Type Distribution",
              template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)

# ===============================
# 📋 TABLE
# ===============================
st.dataframe(
    df[df['severity'] != "normal"],
    use_container_width=True,
    height=300
)
st.subheader("🚨 Anomaly Log")

if 'severity' in df.columns:
    st.dataframe(df[df['severity'] != "normal"], use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

# ===============================
# 📥 DOWNLOAD
# ===============================
st.subheader("📥 Export Reports")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "anomaly_data.csv"
)

report = f"""
FITPULSE HEALTH REPORT

Total Records: {total}
Anomalies: {anomalies}
Avg HR: {avg_hr:.1f}
Avg SpO2: {avg_spo2:.1f}
"""

st.download_button(
    "Download Summary Report",
    report,
    "report.txt"
)