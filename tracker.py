import cv2
import numpy as np

class IntrusionTracker:
    def __init__(self, line_y_coordinate=300):
        """
        Initializes the tracker and boundary line for intrusion detection.
        `line_y_coordinate` represents the virtual border/fence line on the frame.
        """
        self.line_y = line_y_coordinate
        self.breached_ids = set()

    def check_intrusion(self, boxes, frame_width, frame_height):
        """
        Checks if any detected bounding box crosses the virtual perimeter line.
        """
        intrusion_detected = False
        
        if boxes is None or len(boxes) == 0:
            return intrusion_detected, []

        alert_boxes = []

        for box in boxes:
            try:
                if len(box) >= 6:
                    x1, y1, x2, y2, conf, cls_id = int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(box[4]), int(box[5])
                elif len(box) == 5:
                    x1, y1, x2, y2, conf = int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(box[4])
                    cls_id = 0
                else:
                    continue
                
                # COCO Class IDs: 
                # 0 = person, 2 = car, 3 = motorcycle, 5 = bus, 7 = truck
                # We include both persons and vehicles for perimeter security
                valid_classes = [0, 2, 3, 5, 7]
                
                if cls_id in valid_classes:
                    # Bottom center / bottom edge of the bounding box acts as the touch point
                    center_y = y2
                    
                    # Check if the object crosses the threshold line (Perimeter Breach)
                    if center_y >= self.line_y:
                        intrusion_detected = True
                        alert_boxes.append((x1, y1, x2, y2, conf))
            except Exception as e:
                pass

        return intrusion_detected, alert_boxes

    def draw_perimeter(self, frame):
        """
        Draws the virtual border line on the video feed.
        """
        height, width, _ = frame.shape
        cv2.line(frame, (0, self.line_y), (width, self.line_y), (0, 0, 255), 3)
        cv2.putText(frame, "RESTRICTED PERIMETER LINE", (20, self.line_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        return frame