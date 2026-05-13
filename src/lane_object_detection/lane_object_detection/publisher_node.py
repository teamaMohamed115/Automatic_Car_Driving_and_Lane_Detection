import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

import cv2

from .camera_manager import CameraManager
from .ncnn_inference import create_inference
from .lane_steering import LaneSteering
from .motor_controller import MotorController


def _find_model_dir():
    pkg_dir = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    )
    candidate = os.path.join(pkg_dir, 'models')
    if os.path.isdir(candidate):
        return candidate
    try:
        from ament_index_python.packages import get_package_share_directory
        share = get_package_share_directory('lane_object_detection')
        candidate = os.path.join(share, 'models')
        if os.path.isdir(candidate):
            return candidate
    except (ImportError, LookupError):
        pass
    return candidate


class LaneFollowingNode(Node):
    def __init__(self):
        super().__init__('lane_following_node')

        self.image_pub = self.create_publisher(Image, '/camera/lane_frames', 10)
        self.steer_pub = self.create_publisher(String, '/camera/steering', 10)

        self.bridge = CvBridge()

        self.declare_parameter('camera_src', 0)
        self.declare_parameter('use_gstreamer', False)
        self.declare_parameter('model_dir', _find_model_dir())
        self.declare_parameter('kp', 0.5)
        self.declare_parameter('base_speed', 0.3)
        self.declare_parameter('input_width', 256)
        self.declare_parameter('input_height', 256)

        src = self.get_parameter('camera_src').value
        use_gst = self.get_parameter('use_gstreamer').value
        model_dir = self.get_parameter('model_dir').value
        kp = self.get_parameter('kp').value
        base_speed = self.get_parameter('base_speed').value
        in_w = self.get_parameter('input_width').value
        in_h = self.get_parameter('input_height').value

        self.get_logger().info(f"Camera: src={src}, gstreamer={use_gst}")
        self.get_logger().info(f"Model dir: {model_dir}")
        self.get_logger().info(f"Steering: kp={kp}, base_speed={base_speed}")

        self.cam = CameraManager(src=src, use_gstreamer=use_gst)

        param_path = os.path.join(model_dir, 'unet_depthwise_nano_jit.ncnn.param')
        bin_path = os.path.join(model_dir, 'unet_depthwise_nano_jit.ncnn.bin')
        self.model = create_inference(param_path, bin_path, input_size=(in_w, in_h))

        self.steering = LaneSteering(kp=kp, base_speed=base_speed)
        self.motors = MotorController()

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        frame = self.cam.read()
        if frame is None:
            self.get_logger().warn('Failed to capture frame')
            return

        mask = self.model.infer(frame)

        steer, left_speed, right_speed = self.steering.compute(mask)
        self.motors.set_speeds(left_speed, right_speed)

        overlay = frame.copy()
        overlay[mask > 0] = (0, 255, 0)
        vis = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

        h, w = vis.shape[:2]
        cv2.putText(vis, f"Steering: {steer:+.3f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        msg = self.bridge.cv2_to_imgmsg(vis, 'bgr8')
        self.image_pub.publish(msg)

        steer_msg = String()
        steer_msg.data = f"steering={steer:.3f},L={left_speed:.3f},R={right_speed:.3f}"
        self.steer_pub.publish(steer_msg)

    def destroy(self):
        self.motors.stop()
        self.cam.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LaneFollowingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
