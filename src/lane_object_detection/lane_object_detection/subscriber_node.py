import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

import cv2


class LaneViewerNode(Node):
    def __init__(self):
        super().__init__('lane_viewer_node')

        self.image_sub = self.create_subscription(
            Image, '/camera/lane_frames', self.image_callback, 10)
        self.steer_sub = self.create_subscription(
            String, '/camera/steering', self.steer_callback, 10)

        self.bridge = CvBridge()
        self.latest_steering = 'No steering data'

    def steer_callback(self, msg):
        self.latest_steering = msg.data

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return

        cv2.putText(frame, self.latest_steering, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('Lane Following - UNet NCNN', frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = LaneViewerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
