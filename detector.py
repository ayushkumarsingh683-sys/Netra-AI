import cv2
from ultralytics import YOLO

class PerimeterDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """Initialize the YOLO model for intrusion detection."""
        self.model = YOLO(model_path)

    def detect_objects(self, frame, conf=0.35):
        """
        Runs YOLO inference on a single frame.
        Detects classes: 'person' (ID 0) and vehicles ('car', 'truck', etc.)
        """
        # Run inference
        results = self.model(frame, conf=conf, verbose=False)
        
        # Extract plotted frame with bounding boxes automatically drawn by YOLO
        annotated_frame = results[0].plot()
        
        # Extract raw boxes data cleanly as a list
        boxes_data = []
        
        try:
            for box in results[0].boxes:
                # If box is already a tuple or list/tensor sequence
                if isinstance(box, (tuple, list)):
                    if len(box) >= 4:
                        boxes_data.append([int(box[0]), int(box[1]), int(box[2]), int(box[3]), 1.0, 0])
                    continue
                
                # Standard Ultralytics box object
                if hasattr(box, 'xyxy') and len(box.xyxy) > 0:
                    coords = box.xyxy[0].tolist()
                    confidence = float(box.conf[0]) if hasattr(box, 'conf') else 1.0
                    cls_id = int(box.cls[0]) if hasattr(box, 'cls') else 0
                    
                    boxes_data.append([
                        int(coords[0]), 
                        int(coords[1]), 
                        int(coords[2]), 
                        int(coords[3]), 
                        confidence, 
                        cls_id
                    ])
        except Exception as e:
            print(f"Detector loop error: {e}")
        
        return annotated_frame, boxes_data