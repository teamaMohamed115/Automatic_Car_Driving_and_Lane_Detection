import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

import cv2
import numpy as np
import time

try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False
    print("Warning: ultralytics (YOLOv8) not installed. Object detection will mock out.")

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        
        # Publishers
        self.image_pub = self.create_publisher(Image, '/camera/lane_frames', 10)
        self.detect_pub = self.create_publisher(String, '/camera/detections', 10)
        
        # Utils
        self.bridge = CvBridge()
        
        # Camera
        # Using 0 for general USB or /dev/video0 which Pi Camera can map to via V4L2
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Could not open camera interface.")
            
        # Object Detection Model
        self.model = None
        if HAS_YOLO:
            # We load the nano model (it downloads automatically if not present)
            self.model = YOLO("yolov8n.pt") 

        # Timer setup - roughly 30 FPS (0.033) or maybe slower for Pi limits (0.1 = 10fps)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def draw_lane_lines(self, frame):
        """Basic lane line drawing using Canny and Hough."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        
        # ROI
        height, width = edges.shape
        mask = np.zeros_like(edges)
        
        # Define a basic triangular/trapezoid polygon for a road looking forward
        polygon = np.array([[
            (0, height),
            (width, height),
            (int(width / 2), int(height / 2))
        ]], np.int32)
        
        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)
        
        # Hough Lines
        lines = cv2.HoughLinesP(cropped_edges, 1, np.pi / 180, 50, maxLineGap=20, minLineLength=50)
        
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
                
        # Combine
        combined = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return combined

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 1. Pipeline: Lane Detection
        processed_frame = self.draw_lane_lines(frame)
        
        # 2. Pipeline: Object Detection
        detection_string = "No object detected"
        
        if self.model is not None:
            # Run inference
            results = self.model(frame, verbose=False)
            
            detected_classes = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Get class name
                    cls_id = int(box.cls[0].item())
                    cls_name = self.model.names[cls_id]
                    detected_classes.append(cls_name)
                    
            if len(detected_classes) > 0:
                detection_string = f"Detected: {', '.join(set(detected_classes))}"
        
        # 3. Publish
        # Publish frame
        msg_image = self.bridge.cv2_to_imgmsg(processed_frame, "bgr8")
        self.image_pub.publish(msg_image)
        
        # Publish detection text
        msg_detect = String()
        msg_detect.data = detection_string
        self.detect_pub.publish(msg_detect)
        
        # Logging (optional, but good for debugging)
        # self.get_logger().info(f"Published frame and text: {detection_string}")

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.cap.release()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
