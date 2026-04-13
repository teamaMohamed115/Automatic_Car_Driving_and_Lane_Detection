import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

import cv2

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        
        # Subscriptions
        self.image_sub = self.create_subscription(
            Image,
            '/camera/lane_frames',
            self.image_callback,
            10)
            
        self.detect_sub = self.create_subscription(
            String,
            '/camera/detections',
            self.detect_callback,
            10)
            
        self.bridge = CvBridge()
        self.latest_detection = "No object detected"

    def detect_callback(self, msg):
        # Update the stored text state whenever a new detection arrives
        self.latest_detection = msg.data

    def image_callback(self, msg):
        try:
            # Convert ROS Image back to OpenCV format
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Overlay the text
        font = cv2.FONT_HERSHEY_SIMPLEX
        placement = (30, 50)
        font_scale = 1
        
        # Draw a black shadow/bg for readability
        cv2.putText(frame, self.latest_detection, placement, font, font_scale, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(frame, self.latest_detection, placement, font, font_scale, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Display the result
        cv2.imshow("Raspberry Pi Viewer - Lane & Object Detection", frame)
        cv2.waitKey(1) 

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
