import os
import cv2
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from detector import PerimeterDetector
from tracker import IntrusionTracker

app = FastAPI(title="Netra-AI Multi-Cam Command Center")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    detector = PerimeterDetector(model_path='yolov8n.pt')
except Exception as e:
    detector = None

tracker = IntrusionTracker(line_y_coordinate=300)
system_status = {"status": "Online", "intrusion": False}

current_video_path = "cctv.mp4"

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Video nahi khul rahi: {video_path}")
        return

    global system_status
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            # SPEED OPTIMIZATION: Frame ko resize karein taaki YOLOv8 bina lag ke super-fast chale
            original_height, original_width, _ = frame.shape
            process_width = 640
            aspect_ratio = original_height / original_width
            process_height = int(process_width * aspect_ratio)
            
            small_frame = cv2.resize(frame, (process_width, process_height))
            
            # 1. YOLOv8 Detection on resized frame
            if detector is not None:
                annotated_small, boxes_small = detector.detect_objects(small_frame, conf=0.35)
            else:
                annotated_small, boxes_small = small_frame, []
            
            # Coordinates ko original size par scale back karein
            scale_x = original_width / process_width
            scale_y = original_height / process_height
            
            scaled_boxes = []
            for (x1, y1, x2, y2, conf) in boxes_small:
                scaled_boxes.append((int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y), conf))
            
            # 2. Intrusion Check
            intrusion, alert_boxes = tracker.check_intrusion(scaled_boxes, original_width, original_height)
            
            # 3. Draw Perimeter Line on original frame
            annotated_frame = tracker.draw_perimeter(frame)
            
            # 4. Highlight Breaches
            for (x1, y1, x2, y2, conf_score) in alert_boxes:
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(annotated_frame, f"TACTICAL ALERT! {conf_score:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            if intrusion:
                system_status["status"] = "ALERT: Breach Detected!"
                system_status["intrusion"] = True
            else:
                system_status["status"] = "Secure / Perimeter Clear"
                system_status["intrusion"] = False

            # JPEG compression quality optimize ki hai taaki stream fast ho
            ret, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print(f"Stream error: {e}")
    finally:
        cap.release()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    global current_video_path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, file.filename)
    
    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)
        
    current_video_path = save_path
    return {"message": "Video uploaded successfully", "filename": file.filename}

@app.get('/video_feed/active')
def video_feed_active():
    return StreamingResponse(generate_frames(current_video_path), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/video_feed/room')
def video_feed_room():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return StreamingResponse(generate_frames(os.path.join(base_dir, "cctv.mp4")), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/video_feed/fog')
def video_feed_fog():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return StreamingResponse(generate_frames(os.path.join(base_dir, "gemini_generated_video_35755847.mp4")), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/status')
def get_status():
    return system_status