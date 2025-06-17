import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

LOG_FILE = "activity_log.jsonl"

# Load and preprocess activity log
def load_activity_log():
    entries = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry["timestamp"] = datetime.fromisoformat(entry["timestamp"])
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        st.error(f"Could not find '{LOG_FILE}'. Please run the activity logger.")
    return pd.DataFrame(entries)
import pandas as pd

# Load activity log
with open("activity_log.jsonl", "r", encoding="utf-8") as f:
    logs = [json.loads(line.strip()) for line in f if line.strip()]

# Convert to DataFrame
df = pd.DataFrame(logs)

# Parse timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Streamlit UI
st.set_page_config(page_title="Activity Timeline", layout="wide")
st.title("📊 Activity Timeline Viewer")

log_df = load_activity_log()
if log_df.empty:
    st.warning("No activity records found.")
    st.stop()

# Filters
min_time = log_df["timestamp"].min()
max_time = log_df["timestamp"].max()
st.sidebar.markdown("### Filter by Time Range")
from datetime import datetime

# Convert to native datetime
min_time = df["timestamp"].min().to_pydatetime()
max_time = df["timestamp"].max().to_pydatetime()

time_range = st.sidebar.slider(
    "Select time range",
    min_value=min_time,
    max_value=max_time,
    value=(min_time, max_time),
    format="HH:mm"
)


# Filtered data
filtered_df = log_df[(log_df["timestamp"] >= time_range[0]) & (log_df["timestamp"] <= time_range[1])]

# Timeline Plot
fig = px.timeline(
    filtered_df,
    x_start="timestamp",
    x_end=filtered_df["timestamp"] + pd.Timedelta(seconds=5),
    y="app",
    color="app",
    hover_data=["title"],
    title="Active Application Timeline"
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(height=600, margin=dict(t=60))

st.plotly_chart(fig, use_container_width=True)

# Table View
st.subheader("🗂️ Detailed Log")
st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)
