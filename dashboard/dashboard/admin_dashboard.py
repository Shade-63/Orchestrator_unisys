"""
Admin Dashboard - Monitoring and Analytics Interface
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="AI Orchestrator - Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
            
            

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}

body, .stApp {
    background: linear-gradient(145deg, #1c1e24, #111318, #1c1e24);
    background-size: 200% 200%;
    animation: gradientShift 12s ease infinite;
    color: #e2e4e9 !important;
}

.hero-section {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    padding: 35px 30px;
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.35);
    animation: fadeIn 0.6s ease-in-out;
}

.hero-title {
    font-size: 42px;
    color: white;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 20px;
    color: #e3e9ff;
    margin-top: -5px;
}

.metric-card {
    padding-left:38px;
    margin: 2px;
    background: #1a1d24;
    border: 4px solid #dc2626;
    border-radius:14px
    padding:20px;
    border-radius: 14px;
    box-shadow: 0px 0px 18px rgba(220, 38, 38, 0.35);
    transition: 0.25s ease-in-out;
    color: white;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 8px 24px rgba(0,0,0,0.35);
}

.node-card {
    
    background: #161a22;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.25);
    transition: 0.25s ease-in-out;
}

.node-card:hover {
    transform: translateY(-3px);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.35);
}

.dataframe tbody tr {
    background-color: #1a1d24 !important;
    color: #e5e7eb !important;
}

.dataframe thead {
    background-color: #0f172a !important;
    color: white !important;
}

h1, h2, h3, h4 {
    color: #f3f4f6 !important;
}

hr {
    border: 1px solid #1f2937;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    border: none;
    transition: 0.25s ease-in-out;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    transform: translateY(-2px);
}

.stCheckbox label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

ORCHESTRATOR_URL = "http://localhost:8000/api"

@st.cache_data(ttl=10)
def fetch_task_history(limit=200):
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/task-history?limit={limit}", timeout=5)
        if r.status_code == 200:
            return r.json()["tasks"]
        return []
    except:
        return []

@st.cache_data(ttl=5)
def fetch_node_status():
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/node-status", timeout=5)
        if r.status_code == 200:
            return r.json()["nodes"]
        return {}
    except:
        return {}

@st.cache_data(ttl=10)
def fetch_statistics():
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/statistics", timeout=5)
        if r.status_code == 200:
            return r.json()
        return {}
    except:
        return {}

st.markdown("""
<div class="hero-section">
    <div class="hero-title">📊 AI Orchestrator Admin Dashboard</div>
    <div class="hero-subtitle">Enterprise-Grade Monitoring • Real-Time Analytics • System Intelligence</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col2:
    auto_refresh = st.checkbox("Auto-refresh (10s)", value=False)
    if st.button("🔄 Refresh Now"):
        st.rerun()

if auto_refresh:
    time.sleep(10)
    st.rerun()

task_history = fetch_task_history()
node_status = fetch_node_status()
statistics = fetch_statistics()

st.markdown("## 📈 Key Metrics")

if statistics:
    overall = statistics.get("overall", {})
    node_stats = statistics.get("node_statistics", [])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div class='metric-card'><h3>Total Tasks</h3><h2>{overall.get('total_tasks', 0)}</h2></div>", unsafe_allow_html=True)

    with col2:
        success = overall.get("success_rate", 0) * 100
        st.markdown(f"<div class='metric-card'><h3>Success Rate</h3><h2>{success:.1f}%</h2></div>", unsafe_allow_html=True)

    with col3:
        if task_history:
            avg_time = sum(t["execution_time"] for t in task_history) / len(task_history)
            st.markdown(f"<div class='metric-card'><h3>Avg Exec Time</h3><h2>{avg_time:.3f}s</h2></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='metric-card'><h3>Avg Exec Time</h3><h2>N/A</h2></div>", unsafe_allow_html=True)

    with col4:
        total_cost = sum(n["total_cost"] for n in node_stats)
        st.markdown(f"<div class='metric-card'><h3>Total Cost</h3><h2>${total_cost:.2f}</h2></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🖥️ Node Health Status")

if node_status:
    col1, col2, col3 = st.columns(3)
    for node_name, col in zip(["EDGE", "CLOUD", "GPU"], [col1, col2, col3]):
        s = node_status.get(node_name, {})
        load = s.get("load", 0)
        latency = s.get("latency", 0)
        cost = s.get("cost_per_task", 0)
        active = s.get("active_tasks", 0)
        health = s.get("health", "unknown")

        color = "green" if health == "healthy" else "orange" if health == "warning" else "red"
        emoji = "🟢" if health == "healthy" else "🟡" if health == "warning" else "🔴"

        with col:
            st.markdown(f"<div class='node-card'><h3>{emoji} {node_name} Node</h3>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=load,
                title={'text': "Load %", 'font': {'color': 'white'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': 'white'},
                    'bar': {'color': color},
                    'bgcolor': "#111827"
                }
            ))
            fig.update_layout(height=180, margin=dict(l=5, r=5, t=40, b=0), paper_bgcolor="#161a22", font_color="white")
            st.plotly_chart(fig, use_container_width=True)

            st.metric("Latency", f"{latency} ms")
            st.metric("Cost/Task", f"${cost}")
            st.metric("Active Tasks", active)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Unable to fetch node status")

st.markdown("---")
st.markdown("## 📊 Workload Distribution")

if task_history:
    df = pd.DataFrame(task_history)

    col1, col2 = st.columns(2)

    with col1:
        node_counts = df["chosen_node"].value_counts()
        fig = px.pie(
            values=node_counts.values,
            names=node_counts.index,
            title="Tasks by Node"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        type_counts = df["task_type"].value_counts()
        fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Tasks by Type"
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("## 💰 Cost & Performance Analysis")

if task_history:
    col1, col2 = st.columns(2)

    with col1:
        cost_by_node = df.groupby("chosen_node")["cost"].sum().reset_index()
        fig = px.bar(cost_by_node, x="chosen_node", y="cost", title="Total Cost by Node")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        time_by_node = df.groupby("chosen_node")["execution_time"].mean().reset_index()
        fig = px.bar(time_by_node, x="chosen_node", y="execution_time", title="Average Execution Time by Node")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("## 📋 Task Execution History")

if task_history:
    df = pd.DataFrame(task_history)

    col1, col2, col3 = st.columns(3)

    with col1:
        filter_node = st.selectbox("Filter by Node", ["All"] + list(df["chosen_node"].unique()))

    with col2:
        filter_status = st.selectbox("Filter by Status", ["All"] + list(df["status"].unique()))

    with col3:
        limit = st.slider("Rows to Display", 10, 200, 50)

    filtered_df = df.copy()
    if filter_node != "All":
        filtered_df = filtered_df[filtered_df["chosen_node"] == filter_node]
    if filter_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == filter_status]

    st.dataframe(filtered_df.head(limit), use_container_width=True, hide_index=True)

    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"task_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
else:
    st.info("No task history available yet.")

st.markdown("---")
st.caption("AI Workload Orchestrator Admin Dashboard • Auto-updates every 10s when enabled")
