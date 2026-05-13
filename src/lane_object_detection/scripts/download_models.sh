#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="$(cd "$(dirname "$0")/.." && pwd)/models"
mkdir -p "$MODEL_DIR"

BASE_URL="https://huggingface.co/nickpai/lane-detection-unet-ncnn/resolve/main/unet_depthwise_nano"

echo "Downloading UNetDepthwiseNano NCNN model files..."
echo "  -> $MODEL_DIR"

curl -L -o "$MODEL_DIR/unet_depthwise_nano_jit.ncnn.param" \
    "$BASE_URL/unet_depthwise_nano_jit.ncnn.param"

curl -L -o "$MODEL_DIR/unet_depthwise_nano_jit.ncnn.bin" \
    "$BASE_URL/unet_depthwise_nano_jit.ncnn.bin"

echo "Done. Files in $MODEL_DIR:"
ls -lh "$MODEL_DIR"
