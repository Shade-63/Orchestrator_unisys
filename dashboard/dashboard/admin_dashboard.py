import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="AI Workload Orchestrator - Admin",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
    0% { opacity: 0; transform: translateX(-20px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.9; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.3); }
    50% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.3); }
}
@keyframes rocketFly {
    0% {
        transform: translateX(-100px) translateY(100px) rotate(-45deg);
        opacity: 0;
    }
    50% {
        transform: translateX(-30px) translateY(30px) rotate(-20deg);
        opacity: 1;
    }
    100% {
        transform: translateX(0) translateY(0) rotate(0deg);
        opacity: 1;
    }
}
.rocket-icon {
    display: inline-block;
    animation: rocketFly 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    font-size: 1.5em;
}
body, .stApp {
    background: linear-gradient(145deg, #0f1724 0%, #081027 60%, #081027 100%);
    color: #e6eef8 !important;
}
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 44px 36px;
    border-radius: 14px;
    margin-bottom: 28px;
    animation: fadeIn 0.8s ease-in-out;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.hero-title {
    font-size: 44px;
    font-weight: 800;
    color: white;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.25);
    margin: 0;
}
.hero-subtitle {
    font-size: 18px;
    font-weight: 500;
    color: rgba(255,255,255,0.92);
    margin-top: 8px;
}
.metric-box {
    padding: 18px;
    border-radius: 12px;
   
    border: 1px solid #e6eef8;
    margin-bottom: 12px;
    transition: all 0.28s ease-in-out;
    box-shadow: 0 6px 18px rgba(2,6,23,0.12);
    color:#000000;
}
.metric-box:hover {
    box-shadow: 0 10px 30px rgba(102,126,234,0.12);
    transform: translateY(-4px);
    border-color: #667eea;
}
.node-card {
    padding: 18px;
    background: linear-gradient(180deg, #0f1724 0%, #091027 100%);
    border-radius: 12px;
    color: #e6eef8;
    box-shadow: 0 6px 18px rgba(2,6,23,0.35);
    border: 1px solid rgba(255,255,255,0.03);
    margin-bottom: 14px;
}
.node-card .small {
    font-size: 13px;
    color: rgba(230,238,248,0.8);
}
.stButton>button {
    width: 100%;
    height: 56px;
    font-size: 15px;
    border-radius: 12px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.28s ease-in-out;
    border: none;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.18);
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.28);
}
.result-card {
    padding: 18px;
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
    border-radius: 12px;
    border: 1px solid #e6eef8;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(2,6,23,0.06);
    color: #061126;
}
.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(102,126,234,0.08);
    border-color: #667eea;
}
.sidebar-section {
    padding: 12px 0;
    border-bottom: 1px solid rgba(230,238,248,0.04);
    animation: slideIn 0.6s ease-in-out;
    color: #e6eef8;
}
.dataframe thead th {
    background-color: rgba(102,126,234,0.12) !important;
    color: #e6eef8 !important;
}
.dataframe tbody tr {
    background-color: rgba(255,255,255,0.02) !important;
    color: #e6eef8 !important;
}
.stCheckbox label, .stSelectbox>div, label {
    color: #e6eef8 !important;
}
h2, h3 {
    animation: slideIn 0.6s ease-in-out;
    color: #e6eef8 !important;
}
small {
    color: rgba(230,238,248,0.75);
}

/* ---------------------- PREMIUM CLEAN TABLE ---------------------- */

.table-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.12);
    margin-top: 20px;
    animation: fadeIn 0.8s ease-in-out;
    border: 1px solid rgba(230, 230, 230, 0.65);
}

/* DataFrame wrapper */
[data-testid="stDataFrame"] div {
    border-radius: 12px !important;
}

/* Table Header Styling */
div[data-testid="stDataFrame"] thead th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 10px !important;
}

/* Table Body */
div[data-testid="stDataFrame"] tbody tr {
    background-color: rgba(255,255,255,0.95) !important;
    color: #000000 !important;
    font-size: 14px !important;
    border-bottom: 1px solid #e6e6e6 !important;
}

/* Hover effect */
div[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #f5f1ff !important;
}

/* Table Cells */
div[data-testid="stDataFrame"] tbody td {
    padding: 12px !important;
}

/* Scrollbar for wide tables */
div[data-testid="stDataFrame"]::-webkit-scrollbar {
    height: 10px;
}
div[data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
    background: #b7a4ff;
    border-radius: 12px;
}



</style>
""", unsafe_allow_html=True)

ORCHESTRATOR_URL = "http://localhost:8000/api"

# Authentication credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    """Validate credentials and update session state"""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def logout():
    """Clear session state and logout"""
    st.session_state.authenticated = False
    st.session_state.username = ""

# Login Page
if not st.session_state.authenticated:
    st.markdown("""
    <div class="hero-section" style="text-align: center; max-width: 500px; margin: 100px auto;">
        <div class="hero-title">🔐 Admin Login</div>
        <div class="hero-subtitle">Login to access dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(180deg, #0f1724 0%, #091027 100%);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        ">
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            st.markdown("<h3 style='color: #e6eef8; margin-bottom: 20px;'>Enter Credentials</h3>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="admin", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if login(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.stop()

# Logout button in sidebar (only shown when authenticated)
with st.sidebar:
    st.markdown(f"### 👤 Logged in as: **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()
    st.markdown("---")

@st.cache_data(ttl=8)
def fetch_task_history(limit=200):
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/task-history?limit={limit}", timeout=5)
        if r.status_code == 200:
            return r.json().get("tasks", [])
        return []
    except:
        return []

@st.cache_data(ttl=5)
def fetch_node_status():
    try:
        r = requests.get(f"{ORCHESTRATOR_URL}/node-status", timeout=5)
        if r.status_code == 200:
            return r.json().get("nodes", {})
        return {}
    except:
        return {}

@st.cache_data(ttl=8)
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
    <div class="hero-title"><span class="rocket-icon">🚀</span> AI Workload Orchestrator - Admin</div>
    <div class="hero-subtitle">Enterprise Monitoring · Real-Time Analytics · System Intelligence</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col2:
    auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)
    if st.button("🔄 Refresh Now"):
        st.rerun()

if auto_refresh:
    time.sleep(10)
    st.rerun()

task_history = fetch_task_history(limit=300)
node_status = fetch_node_status()
statistics = fetch_statistics()

st.markdown("## 📈 Key Metrics")
if statistics:
    overall = statistics.get("overall", {})
    node_stats = statistics.get("node_statistics", [])

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"<div class='metric-box'><h4 style='margin:0;'>Total Tasks</h4><h2 style='margin:6px 0 0 0;'>{overall.get('total_tasks', 0)}</h2><small>since tracking</small></div>", unsafe_allow_html=True)

    with m2:
        success = overall.get("success_rate", 0) * 100
        st.markdown(f"<div class='metric-box'><h4 style='margin:0;'>Success Rate</h4><h2 style='margin:6px 0 0 0;'>{success:.1f}%</h2><small>recent</small></div>", unsafe_allow_html=True)

    with m3:
        if task_history:
            avg_time = sum(t.get("execution_time", 0) for t in task_history) / max(len(task_history),1)
            st.markdown(f"<div class='metric-box'><h4 style='margin:0;'>Avg Exec Time</h4><h2 style='margin:6px 0 0 0;'>{avg_time:.3f}s</h2><small>per task</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='metric-box'><h4 style='margin:0;'>Avg Exec Time</h4><h2 style='margin:6px 0 0 0;'>N/A</h2></div>", unsafe_allow_html=True)

    with m4:
        total_cost = sum(n.get("total_cost", 0) for n in node_stats)
        st.markdown(f"<div class='metric-box'><h4 style='margin:0;'>Total Cost</h4><h2 style='margin:6px 0 0 0;'>${total_cost:.2f}</h2><small>aggregated</small></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🖥️ Node Health")

if node_status:
    n1, n2, n3 = st.columns(3)
    for name, col in zip(["EDGE","CLOUD","GPU"], [n1,n2,n3]):
        s = node_status.get(name, {})
        load = s.get("load", 0)
        latency = s.get("latency", 0)
        cost = s.get("cost_per_task", 0)
        active = s.get("active_tasks", 0)
        health = s.get("health", "unknown")

        emoji = "🟢" if health=="healthy" else "🟡" if health=="warning" else "🔴"
        with col:
            st.markdown(f"<div class='node-card'><h4 style='margin:0;'>{emoji} {name} Node</h4><div class='small'>status: {health}</div>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=load,
                title={'text': "Load %", 'font': {'color': '#ffffff'}},
                gauge={
                    'axis': {'range':[0,100], 'tickcolor':'#ffffff'},
                    'bar': {'color': "#667eea"},
                    'steps': [
                        {'range':[0,60], 'color':'#18304a'},
                        {'range':[60,85], 'color':'#2b3550'},
                        {'range':[85,100], 'color':'#3b2b3b'}
                    ]
                }
            ))
            fig.update_layout(height=180, margin=dict(l=5,r=5,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', font_color='#e6eef8')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"<div style='display:flex; gap:12px; margin-top:8px;'><div><strong>Latency</strong><div class='small'>{latency} ms</div></div><div><strong>Cost</strong><div class='small'>${cost}</div></div><div><strong>Active</strong><div class='small'>{active}</div></div></div></div>", unsafe_allow_html=True)
else:
    st.warning("Unable to fetch node status")

st.markdown("---")
st.markdown("## 📊 Workload Distribution")

if task_history:
    df = pd.DataFrame(task_history)
    c1, c2 = st.columns(2)
    with c1:
        node_counts = df.get("chosen_node", pd.Series()).value_counts()
        if len(node_counts) == 0:
            st.info("No tasks recorded yet.")
        else:
            fig = px.pie(values=node_counts.values, names=node_counts.index, title="Tasks by Node", hole=0.35)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        type_counts = df.get("task_type", pd.Series()).value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values, title="Tasks by Type")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("## 💰 Cost & Performance")

if task_history:
    c1, c2 = st.columns(2)
    with c1:
        if "cost" in df.columns:
            cost_by_node = df.groupby("chosen_node")["cost"].sum().reset_index()
            fig = px.bar(cost_by_node, x="chosen_node", y="cost", title="Total Cost by Node")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cost data not available in task history.")
    with c2:
        if "execution_time" in df.columns:
            time_by_node = df.groupby("chosen_node")["execution_time"].mean().reset_index()
            fig = px.bar(time_by_node, x="chosen_node", y="execution_time", title="Avg Execution Time by Node")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Execution time data not available.")

st.markdown("---")
st.markdown("## 📋 Task Execution History")

if task_history:
    df = pd.DataFrame(task_history)
    f1, f2, f3 = st.columns(3)
    with f1:
        filter_node = st.selectbox("Filter by Node", ["All"] + list(df.get("chosen_node", pd.Series()).unique()))
    with f2:
        filter_status = st.selectbox("Filter by Status", ["All"] + list(df.get("status", pd.Series()).unique()))
    with f3:
        limit = st.slider("Rows to Display", 10, 200, 50)

    filtered = df.copy()
    if filter_node != "All":
        filtered = filtered[filtered["chosen_node"] == filter_node]
    if filter_status != "All":
        filtered = filtered[filtered["status"] == filter_status]

    # ---------------------- BEAUTIFUL TABLE WRAPPER ----------------------
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)

    st.dataframe(
        filtered.head(limit),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
    # ---------------------------------------------------------------------

    csv = filtered.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name=f"task_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.info("No task history available. Use the Demo UI to create tasks.")

st.markdown("---")
st.caption("AI Workload Orchestrator · Admin Dashboard · UI matched to Demo")

