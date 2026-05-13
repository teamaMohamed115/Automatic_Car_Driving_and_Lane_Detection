import os
import numpy as np
import cv2


class NCNNInference:
    def __init__(self, param_path, bin_path, input_size=(256, 256),
                 mean=None, std=None, input_layer='in0', output_layer='out0'):
        self.input_w, self.input_h = input_size
        self.mean = mean if mean is not None else [127.5, 127.5, 127.5]
        self.std = std if std is not None else [1 / 127.5, 1 / 127.5, 1 / 127.5]
        self.input_layer = input_layer
        self.output_layer = output_layer

        import ncnn
        self.net = ncnn.Net()
        ret_p = self.net.load_param(param_path)
        ret_m = self.net.load_model(bin_path)
        if ret_p != 0 or ret_m != 0:
            raise RuntimeError(f"Failed to load NCNN model: param={ret_p} bin={ret_m}")

    def infer(self, frame_bgr):
        h, w = frame_bgr.shape[:2]

        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        mat_in = ncnn.Mat.from_pixels_resize(
            rgb, ncnn.Mat.PIXEL_RGB, w, h, self.input_w, self.input_h
        )
        mat_in.substract_mean_normalize(self.mean, self.std)

        ext = self.net.create_extractor()
        ext.input(self.input_layer, mat_in)

        out = ncnn.Mat()
        ext.extract(self.output_layer, out)

        mask = np.array(out)
        if mask.ndim == 3:
            mask = mask.squeeze()
        mask = (mask > 0).astype(np.uint8) * 255

        mask_resized = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
        return mask_resized


class MockNCNNInference:
    def __init__(self, param_path=None, bin_path=None, input_size=(256, 256),
                 mean=None, std=None, input_layer='in0', output_layer='out0'):
        self.input_w, self.input_h = input_size

    def infer(self, frame_bgr):
        h, w = frame_bgr.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.rectangle(mask, (w // 2 - 10, h // 2), (w // 2 + 10, h), 255, -1)
        return mask


def create_inference(param_path, bin_path, input_size=(256, 256),
                     mean=None, std=None, input_layer='in0', output_layer='out0'):
    for p in (param_path, bin_path):
        if not os.path.exists(p):
            raise FileNotFoundError(f"Model file not found: {p}")
    try:
        return NCNNInference(param_path, bin_path, input_size, mean, std,
                             input_layer, output_layer)
    except ImportError:
        print("Warning: ncnn Python package not available. Using mock inference.")
        return MockNCNNInference(param_path, bin_path, input_size, mean, std,
                                 input_layer, output_layer)
