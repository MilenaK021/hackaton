import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st_autorefresh(interval=3000, key="refresh")

st.title("Locomotive Digital Twin Dashboard")

data = pd.read_csv("locomotive_data.csv", parse_dates=["timestamp"])

# --- health score ---
def health_score(row):
    score = 100

    if row["temperature"] > 100:
        score -= 30
    if row["pressure"] > 55:
        score -= 20
    if row["vibration"] > 1.2:
        score -= 30

    return max(score, 0)

system = st.selectbox("Select System", data["system_id"].unique())

filtered = data[data["system_id"] == system].copy()
filtered["health"] = filtered.apply(health_score, axis=1)

latest = filtered.iloc[-1]

# --- metrics ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Temp", f"{latest['temperature']} C")
col2.metric("Pressure", f"{latest['pressure']}")
col3.metric("Speed", f"{latest['speed']} km/h")
col4.metric("Health", f"{latest['health']} %")

# --- chart ---
st.subheader("System Parameters")
st.line_chart(
    filtered.set_index("timestamp")[["temperature", "pressure", "speed", "vibration"]]
)

# --- status pie ---
st.subheader("System Condition")

status_counts = {
    "OK": (filtered["health"] > 70).sum(),
    "Warning": ((filtered["health"] <= 70) & (filtered["health"] > 40)).sum(),
    "Critical": (filtered["health"] <= 40).sum()
}

fig, ax = plt.subplots()
ax.pie(status_counts.values(), labels=status_counts.keys(), autopct="%1.1f%%")
ax.axis("equal")

st.pyplot(fig)

# --- anomaly detection ---
st.subheader("Anomalies")

mean_temp = filtered["temperature"].mean()
std_temp = filtered["temperature"].std()

anomalies = filtered[
    (filtered["temperature"] > mean_temp + 1.5 * std_temp) |
    (filtered["temperature"] < mean_temp - 1.5 * std_temp)
]

st.write(anomalies.tail())

# --- recommendations ---
st.subheader("Recommendations")

if latest["temperature"] > 100:
    st.error("Engine overheating! Reduce load.")
elif latest["temperature"] < 50:
    st.warning("Temperature too low.")

if latest["vibration"] > 1.2:
    st.error("High vibration! Possible mechanical issue.")

if latest["pressure"] > 55:
    st.warning("Pressure too high.")