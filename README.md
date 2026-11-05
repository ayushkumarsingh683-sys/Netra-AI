# 🛡️ Netra-AI: Edge-AI Perimeter Defense & Traffic Monitoring Command Center

Netra-AI is a real-time smart surveillance and intrusion detection system built using advanced computer vision and deep learning models to monitor restricted perimeters and trigger instant alerts during unauthorized breaches.

---

## 👨‍💻 Author & Developer
* **Name:** Ayush Kumar Singh
* **Degree:** B.Tech in Computer Science and Artificial Intelligence
* **Institution:** ABES Institute of Technology, Ghaziabad (Dr. A.P.J. Abdul Kalam Technical University)
* **University Roll No:** 2402901520088

---

## 🏗️ Architecture & Tech Stack

The project is structured into three core modular layers:

1. **Frontend Layer (Streamlit UI - `dashboard.py`):**
   * Modern, dark-themed tactical command center interface.
   * Real-time MJPEG video stream rendering.
   * Dynamic camera feed switching (Room CCTV, Foggy Recon, and Custom Uploaded Feeds).
   * Live system status indicators and built-in video upload functionality.

2. **Backend Server (FastAPI - `app.py`):**
   * High-performance asynchronous API endpoints (`/video_feed/*`, `/upload`, `/status`).
   * Handles multi-threaded frame processing, video looping, and state management.
   * CORS-enabled middleware for seamless frontend-backend communication.

3. **AI & Inference Engine (YOLOv8 & OpenCV - `detector.py` & `tracker.py`):**
   * **YOLOv8n Model:** Lightweight object detection model optimized for edge devices, configured to detect humans (`cls 0`) and vehicles/military assets (`cls 2, 3, 5, 7`).
   * **Intrusion Tracker:** Virtual boundary line logic (`line_y_coordinate`) that tracks bounding box coordinates and triggers instant tactical breach alerts.

---

## ⚙️ System Workflow

1. **Video Ingestion & Processing:** OpenCV captures frames from local CCTV files or user-uploaded tactical videos (`.mp4`, `.avi`).
2. **Object Detection:** Frames are resized and passed through the YOLOv8 detector to extract bounding boxes with high confidence scores.
3. **Perimeter Breach Logic:** The `IntrusionTracker` evaluates if the bottom edge of any detected person or vehicle crosses the predefined red virtual line.
4. **Alert & Telemetry Generation:** If a breach occurs, the system updates `system_status["intrusion"] = True`, highlights the bounding box in red, and flashes visual warning alerts on the Streamlit dashboard.
5. **UI Streaming:** Processed frames are encoded into JPEG byte streams and continuously streamed to the Streamlit frontend via FastAPI.

---

## 🚀 Getting Started & Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Netra-AI.git](https://github.com/YOUR_USERNAME/Netra-AI.git)
   cd Netra-AI/Smart_Perimeter_System
Install dependencies:

Bash
pip install -r requirements.txt
Run the FastAPI Backend:

Bash
uvicorn app:app --reload
Run the Streamlit Dashboard (in a new terminal):

Bash
streamlit run dashboard.py

### Steps to push this to GitHub:
Open your terminal inside your project folder (`D:\Sentinel-AI\Smart_Perimeter_System`) and run:

```powershell
git init
git add .
git commit -m "Initial commit: Netra-AI Full-Stack Perimeter Defense Command Center"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Netra-AI.git
git push -u origin main
