import streamlit as st
import requests
import json
import time
from typing import Dict, Any

st.set_page_config(
    page_title="AI Workload Orchestrator",
    page_icon="🚀",
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

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 50px 40px;
    border-radius: 15px;
    margin-bottom: 30px;
    animation: fadeIn 0.8s ease-in-out;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    margin: 0;
}

.hero-subtitle {
    font-size: 22px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    margin-top: 10px;
}

.workload-section {
    animation: slideIn 0.6s ease-in-out;
}

.result-card, .metric-box {
    animation: fadeIn 0.5s ease-in-out;
}

.stButton>button {
    width: 100%;
    height: 60px;
    font-size: 16px;
    border-radius: 12px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.3s ease-in-out;
    border: none;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.stButton>button:active {
    transform: scale(0.97);
}

.pulse-btn {
    animation: pulse 1.5s infinite ease-in-out;
}

.metric-box {
    padding: 22px;
    border-radius: 12px;
    background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    border: 1px solid #e0e0e0;
    margin-bottom: 12px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.metric-box:hover {
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
    transform: translateY(-4px);
    border-color: #667eea;
}

.result-card {
    padding: 22px;
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease-in-out;
    animation: fadeIn 0.5s ease-in-out;
}

.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    border-color: #667eea;
}

.sidebar-section {
    padding: 12px 0;
    border-bottom: 1px solid #e0e0e0;
    animation: slideIn 0.6s ease-in-out;
}

.node-status-healthy {
    padding: 15px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 10px;
    color: white;
    margin: 8px 0;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.node-status-warning {
    padding: 15px;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    border-radius: 10px;
    color: white;
    margin: 8px 0;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.node-status-critical {
    padding: 15px;
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border-radius: 10px;
    color: white;
    margin: 8px 0;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

h2, h3 {
    animation: slideIn 0.6s ease-in-out;
}

/* Admin link button styling */
.stLinkButton > a {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    transition: all 0.3s ease-in-out !important;
}

.stLinkButton > a:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
}

</style>
""", unsafe_allow_html=True)

ORCHESTRATOR_URL = "http://localhost:8000/api"

if "results" not in st.session_state:
    st.session_state.results = []


def submit_task(task_type, priority, latency, requires_gpu, description):
    with st.spinner(f"Routing {description}..."):
        try:
            payload = {
                "taskType": task_type,
                "priority": priority,
                "latency": latency,
                "requiresGPU": requires_gpu,
                "payload": {"description": description, "timestamp": time.time()},
                "cost_sensitivity": 10 - priority
            }

            response = requests.post(f"{ORCHESTRATOR_URL}/submit-task", json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                st.session_state.results.insert(0, {
                    "description": description,
                    "result": result,
                    "timestamp": time.time()
                })

                st.success("Task routed successfully!")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Chosen Node", result["chosen_node"])
                col2.metric("Confidence", f"{result['confidence']:.1%}")
                col3.metric("Execution Time", f"{result['execution_time']:.3f}s")
                col4.metric("Cost", f"${result['cost']:.4f}")

                st.info(f"Explanation: {result['explanation']}")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to orchestrator. Ensure backend is running.")
        except Exception as e:
            st.error(f"Unexpected Error: {str(e)}")


st.markdown("""
<div class="hero-section">
    <div class="hero-title"><span class="rocket-icon">🚀</span> AI Workload Orchestrator</div>
    <div class="hero-subtitle">Real-Time Intelligent Task Routing Demo</div>
</div>
""", unsafe_allow_html=True)


st.markdown("## 🎯 Trigger Workloads")
st.markdown("**Select a workload to route through the AI Orchestrator**")

left, right = st.columns(2)

with left:
    st.markdown("### ⚡ Real-Time Workloads")
    st.markdown("*Low-latency, high-priority tasks*")
    if st.button("🔍 Fraud Detection", key="fraud"):
        submit_task("fraud_detection", 9, 10, False, "Real-time fraud detection")
    if st.button("📡 Sensor Alert", key="sensor"):
        submit_task("sensor_alert", 10, 10, False, "Critical sensor alert")
    if st.button("🖼️ Image Classification", key="image"):
        submit_task("image_classification", 7, 6, True, "Run CNN image classification")

with right:
    st.markdown("### 📊 Batch Workloads")
    st.markdown("*High-latency tolerance tasks*")
    if st.button("📈 Daily Report Generation", key="report"):
        submit_task("daily_report", 3, 2, False, "Generate daily analytics")
    if st.button("🤖 ML Training Job", key="training"):
        submit_task("ml_training", 5, 3, True, "Deep learning training workload")
    if st.button("🔄 Data Pipeline Execution", key="pipeline"):
        submit_task("data_processing", 4, 3, False, "Process data pipeline")

st.markdown("---")


# How It Works Section
st.markdown("## 🔄 How It Works")
st.markdown("**See the AI Orchestrator in action - from task submission to intelligent routing**")

# Initialize selected step in session state
if "selected_step" not in st.session_state:
    st.session_state.selected_step = 1

# Step selector buttons
st.markdown("""
<style>
.screenshot-container {
    transition: all 0.3s ease;
    border: 3px solid transparent;
    border-radius: 10px;
    padding: 5px;
    cursor: pointer;
}
.screenshot-selected {
    border: 3px solid #667eea !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    transform: translateY(-5px);
}
.screenshot-container:hover {
    border: 3px solid #764ba2;
    box-shadow: 0 6px 20px rgba(118, 75, 162, 0.3);
    transform: translateY(-3px);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="result-card" style="padding: 20px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
    <h3 style="color: white; margin-bottom: 15px; font-weight: 600;">📸 Workflow Demo</h3>
    <p style="font-size: 13px; color: rgba(255, 255, 255, 0.9); margin-bottom: 20px;">
        Click on a step number to see the complete workflow in action
    </p>
</div>
""", unsafe_allow_html=True)

# Step selector buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("1️⃣ Submit Task", key="step1_btn", use_container_width=True):
        st.session_state.selected_step = 1

with col2:
    if st.button("2️⃣ View Result", key="step2_btn", use_container_width=True):
        st.session_state.selected_step = 2

with col3:
    if st.button("3️⃣ Admin Login", key="step3_btn", use_container_width=True):
        st.session_state.selected_step = 3

with col4:
    if st.button("4️⃣ Dashboard", key="step4_btn", use_container_width=True):
        st.session_state.selected_step = 4

st.markdown("<br>", unsafe_allow_html=True)

# Display all screenshots in a row
col1, col2, col3, col4 = st.columns(4)

screenshots = [
    {
        "path": "C:/Users/sumsr/.gemini/antigravity/brain/47b67666-525d-475e-9e4c-ca68187374ac/step1_demo_ui_1765571611127.png",
        "caption": "1. Submit Task"
    },
    {
        "path": "C:/Users/sumsr/.gemini/antigravity/brain/47b67666-525d-475e-9e4c-ca68187374ac/step2_task_result_1765571630913.png",
        "caption": "2. View Result"
    },
    {
        "path": "C:/Users/sumsr/.gemini/antigravity/brain/47b67666-525d-475e-9e4c-ca68187374ac/step3_admin_login_1765571652856.png",
        "caption": "3. Admin Login"
    },
    {
        "path": "C:/Users/sumsr/.gemini/antigravity/brain/47b67666-525d-475e-9e4c-ca68187374ac/step4_admin_dashboard_1765571675305.png",
        "caption": "4. Dashboard"
    }
]

for idx, (col, screenshot) in enumerate(zip([col1, col2, col3, col4], screenshots), 1):
    with col:
        # Add selected class if this is the selected step
        class_name = "screenshot-selected" if st.session_state.selected_step == idx else ""
        
        st.markdown(f'<div class="screenshot-container {class_name}">', unsafe_allow_html=True)
        st.image(screenshot["path"], caption=screenshot["caption"], use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


if st.session_state.results:
    st.markdown("## 📋 Recent Executions")
    st.markdown("**Latest orchestration decisions and routing results**")
    
    for idx, item in enumerate(st.session_state.results[:5]):
        result = item["result"]

        with st.expander(f"{'✅' if result['status'] == 'completed' else '⏳'} {item['description']} → {result['chosen_node']}", expanded=(idx == 0)):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**🔹 Explanation:** {result['explanation']}")
            with col2:
                st.markdown(f"**🔹 Task ID:** `{result['task_id']}`")
            with col3:
                st.markdown(f"**🔹 Status:** `{result['status'].upper()}`")

            st.divider()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📍 Node", result["chosen_node"])
            col2.metric("⏱️ Execution Time", f"{result['execution_time']:.3f}s")
            col3.metric("💰 Cost", f"${result['cost']:.4f}")
            col4.metric("🎯 Confidence", f"{result['confidence']:.1%}")

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.results = []
            st.rerun()
else:
    st.info("📌 Submit a task to view routing insights.")


with st.sidebar:
    # Admin access button at the top
    st.link_button(
        "🔐 Sign in as admin",
        "http://localhost:8502",
        use_container_width=True
    )
    
    st.markdown("---")
    st.header("📊 System Overview")

    if st.button("🔄 Refresh System Status", use_container_width=True):
        st.rerun()

    try:
        status_response = requests.get(f"{ORCHESTRATOR_URL}/node-status", timeout=5)

        if status_response.status_code == 200:
            data = status_response.json()["nodes"]

            for node in ["EDGE", "CLOUD", "GPU"]:
                s = data.get(node, {})
                health = s.get("health", "unknown")
                load = s.get("load", 0)
                latency = s.get("latency", 0)

                emoji = "🟢" if health == "healthy" else "🟡" if health == "warning" else "🔴"
                
                st.markdown(f"### {emoji} {node}")
                
                col1, col2 = st.columns(2)
                col1.metric("Load", f"{load:.1f}%")
                col2.metric("Latency", f"{latency:.0f}ms")
                
                st.progress(load / 100)
                
                st.markdown("---")
        else:
            st.warning("⚠️ Unable to load node status.")

    except:
        st.error("🔴 Orchestrator is offline.")

    st.markdown("---")
    st.caption("🚀 AI Workload Orchestrator Demo UI v1.0")
