import streamlit as st
import requests

st.set_page_config(
    page_title="Netra-AI Command Center",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for high-tech graphics, dark theme and modern UI styling
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #111827;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation & Video Upload Feature
st.sidebar.title("🛡️ Netra-AI Tactical Panel")
st.sidebar.markdown("---")

st.sidebar.subheader("📤 Upload Custom Video")
uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try:
        res = requests.post("http://127.0.0.1:8000/upload", files=files)
        if res.status_code == 200:
            st.sidebar.success("✅ Video uploaded successfully!")
    except Exception as e:
        st.sidebar.error("❌ Failed to connect backend for upload.")

st.sidebar.markdown("---")
feed_option = st.sidebar.radio(
    "Select Camera Feed:",
    ("Room / CCTV Feed", "Foggy Recon Feed", "Custom Uploaded Feed")
)

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")

# Fetch status from FastAPI backend
try:
    response = requests.get("http://127.0.0.1:8000/status", timeout=2)
    if response.status_code == 200:
        status_data = response.json()
        current_status = status_data.get("status", "Online")
        is_intrusion = status_data.get("intrusion", False)
        
        if is_intrusion:
            st.sidebar.error(f"🚨 {current_status}")
        else:
            st.sidebar.success(f"🟢 {current_status}")
    else:
        st.sidebar.warning("⚠️ Status unknown.")
except Exception:
    st.sidebar.error("❌ Backend Offline (Run FastAPI)")

# Main Dashboard UI with Enhanced Graphics
st.title("🚀 Netra-AI Perimeter Defense & Traffic Monitoring")
st.markdown(f"**Active Tactical Stream:** `{feed_option}`")

# Determine URL based on selection
if feed_option == "Room / CCTV Feed":
    stream_url = "http://127.0.0.1:8000/video_feed/room"
elif feed_option == "Foggy Recon Feed":
    stream_url = "http://127.0.0.1:8000/video_feed/fog"
else:
    stream_url = "http://127.0.0.1:8000/video_feed/active"

# Display Stream with high-tech glowing border container
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; border: 2px solid #38bdf8; border-radius: 14px; overflow: hidden; background-color: #0f172a; box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.3);">
        <img src="{stream_url}" width="100%" />
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Analytics / Info Metric Cards below the video stream
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="AI Detector Engine", value="YOLOv8n", delta="Optimized")
with col2:
    st.metric(label="Stream Protocol", value="MJPEG / FastAPI", delta="Real-Time")
with col3:
    st.metric(label="Perimeter Status", value="Armed & Monitoring", delta="Active")

st.markdown("---")
st.caption("Netra-AI Edge Surveillance Pipeline | Powered by FastAPI, YOLOv8 & Streamlit")