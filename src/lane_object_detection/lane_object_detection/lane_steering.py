import numpy as np


class LaneSteering:
    def __init__(self, kp=0.5, base_speed=0.3, deadband=0.05, max_steering=0.5):
        self.kp = kp
        self.base_speed = base_speed
        self.deadband = deadband
        self.max_steering = max_steering

    def compute(self, mask):
        h, w = mask.shape
        bottom_half = mask[h // 2:, :]

        lane_pixels = np.where(bottom_half > 0)
        if len(lane_pixels[1]) == 0:
            return 0.0, 0.0, 0.0

        lane_center_x = np.mean(lane_pixels[1])
        image_center_x = w / 2.0

        error = lane_center_x - image_center_x
        error_normalized = error / (w / 2.0)

        if abs(error_normalized) < self.deadband:
            steering = 0.0
        else:
            steering = np.clip(
                self.kp * error_normalized, -self.max_steering, self.max_steering
            )

        left_speed = self.base_speed - steering
        right_speed = self.base_speed + steering

        left_speed = np.clip(left_speed, -1.0, 1.0)
        right_speed = np.clip(right_speed, -1.0, 1.0)

        return steering, left_speed, right_speed
