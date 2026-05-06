# Tips

* Camera: Raspberry Pi Camera Module V2 (or a wide-angle USB webcam).
* Crucial Mod: Mount the camera high (15-20cm) and tilt it down ~25-30 degrees. This perspective is critical for stable lane detection.
* Power Supply:
* For Pi: An official USB-C power bank (minimum 3A). Don't try to power the Pi from the motor batteries; it causes brownouts.
   * For Motors: 2x 18650 Li-ion batteries in a holder. Avoid 9V batteries; they die too fast.

* OS: Raspberry Pi OS (Legacy, 64-bit, Bullseye). Do not use "Bookworm" (the newest OS) yet, as it enforces a virtual environment that complicates camera access for beginners.
* Python: Python 3.9 (default on Bullseye).
* Libraries (Install via pip3):

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install libopencv-dev python3-opencv
pip3 install tensorflow-aarch64  # Optimized for Pi architecture
pip3 install pandas numpy matplotlib scikit-learn
pip3 install RPi.GPIO

## Autonomous Inference Phase (On the Pi)

   1. Transfer: Copy the model file back to the Pi.
   2. Drive Script:
   * Load Model.
      * Loop:
      1. Capture Frame.
         2. Preprocess (Resize to 200x66, Convert to YUV).
         3. steering = model.predict(image).
         4. Send steering to motors. [4] 
      
## Common Pitfalls & Fixes

* "Zig-Zagging" Car: Your inference is too slow.
* Fix: Resize images to 320x240 or smaller before processing.
   * Fix: Don't use cv2.imshow (displaying video) while driving autonomously; it eats up CPU.
* Car drives off track: Lighting changed.
* Fix: Apply "Shadow Augmentation" during training (randomly darken parts of training images) so the model learns to ignore shadows.
* Fragile Wires: Use hot glue on the GPIO connections once you confirm they work. Vibration will loosen them otherwise.