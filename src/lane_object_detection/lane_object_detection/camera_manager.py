import cv2

GSTREAMER_PIPELINE = (
    "libcamerasrc ! "
    "video/x-raw, width={width}, height={height}, framerate={fps}/1 ! "
    "videoconvert ! video/x-raw, format=BGR ! appsink"
)


class CameraManager:
    def __init__(self, src=0, width=640, height=480, fps=30, use_gstreamer=False):
        self.width = width
        self.height = height

        if use_gstreamer:
            pipeline = GSTREAMER_PIPELINE.format(width=width, height=height, fps=fps)
            self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(src)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open camera (src={src}, gstreamer={use_gstreamer})"
            )

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
