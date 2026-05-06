Use the "https://huggingface.co/nickpai/lane-detection-unet-ncnn" model if your robot is driving on a real road. To use it without any additional training, you must design your "road" to mimic the BDD100K dataset (https://datasetninja.com/bdd100k   &   https://www.kaggle.com/datasets/solesensei/solesensei_bdd100k), which this model was specifically trained on.

## Designing Your "Zero-Shot" Road Track
The BDD100K dataset consists of real-world urban and highway scenes. Your goal is to recreate a high-contrast, realistic environment that the model already recognizes.

* The Surface (Road Base): Use a dark gray or black matte material (like specialized black photography paper or dark gray industrial carpet).
* Avoid shiny surfaces; the model expects the diffuse light reflection typical of asphalt.
* The Lane Markings:
* Colors: Use strictly white or yellow tape.
   * Style: Create a standard two-lane road. Use a dashed white line in the center and solid lines (either white or yellow) on the outer edges.
   * Width: Ensure the tape is wide enough to be visible. In the BDD100K scale, lane markings are approximately 8 pixels wide in training; for your robot, a tape width of 2.5 to 5 cm (1 to 2 inches) is ideal for a standard wide-angle camera.
* The Camera Angle (Perspective):
* The model expects a front-facing, slightly downward-tilted perspective typical of a dashcam.
   * Mount your camera at the front of the robot, roughly 15–20 cm above the ground, tilted down about 20-30 degrees. If the camera is too low or pointing straight down, the model will fail to recognize the perspective as a "road."

## Practical Setup Checklist for Demonstrations

* Lighting: Use diffuse, overhead indoor lighting. Avoid harsh spotlights or being near a window, as the model may struggle with strong sun-glare or deep shadows it wasn't specifically fine-tuned for.
* Avoid Clutter: Keep the area around the track clear. The model might misclassify "vertical" objects like chair legs as lane boundaries if they are too close to the track.
* Track Scale: Make the track wide enough so the robot sees a clear path. A lane width of 60–80 cm.
* Ensure every curve on your track has a radius of at least 1 meter.

## Summary of "Road" Dimensions for 4WD

| Feature | Dimension for 4WD |
|---|---|
| Lane Width | 60 cm to 80 cm |
| Tape Width | 5 cm (2-inch wide tape) |
| Turn Radius | > 100 cm |
| Surface | Dark Matte (Non-reflective) |