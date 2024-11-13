# AARC Lane Detection

## Overview

This project detects lane lines in video footage captured from a GoPro HERO11 mounted on the outside of a vehicle. This setup allows for consistent lane tracking and accurate measurement of lane position relative to the vehicle’s center. 

## Dependencies

This project requires the following dependencies:

* Python
* OpenCV
* NumPy
* Matplotlib (for data visualisation)

## Camera Calibration

Given the GoPro HERO11’s wide-angle lens, calibration is essential to correct lens distortion and ensure accurate lane measurements. The following calibration steps use a chessboard pattern to generate the necessary camera parameters.

### Calibration Process

1. **Load Calibration Video:** The calibration script (`camera_calibration.py`) loads a video of a chessboard pattern (`calibration_video.mkv`), where each frame displays the chessboard in various positions to capture lens distortion from multiple angles.
   
2. **Capture Snapshots:** While playing the video, press **'s'** to save frames with the chessboard visible in different locations. Aim to take between 10 to 20 snapshots, as these will be used for calculating calibration parameters. Each snapshot is saved automatically in the `calibration_images` folder.

3. **Compute Camera Matrix and Distortion Coefficients:** The script then loads the saved snapshots, detects chessboard corners, and calculates the camera matrix and distortion coefficients using `cv2.calibrateCamera()`. These calibration parameters allow for correcting distortion in subsequent frames.

4. **Save Calibration Data:** The camera matrix and distortion coefficients are saved to a file (`calibration_data.npz`) for later use in undistorting the video frames.

### Example Usage

Run `camera_calibration.py` to perform camera calibration. Ensure `calibration_video.mkv` is located in the project directory. The script will guide you through capturing the snapshots needed for calibration.

**Distortion correction:** The calibration data is applied to each frame using cv2.undistort() to correct distortion, providing a consistent and clear view of the lane lines.

### Distortion Correction Example

The resulting calibration data can then be applied to correct lens distortion in your main video footage, ensuring accurate lane position measurements.

![calibration_process](https://github.com/user-attachments/assets/64fdae40-233c-4939-81a7-23d8e52bf212)

## Lane Line Detection

Lane lines are detected in each frame using OpenCV’s image processing tools:

1.	**Color filtering:** A color mask is applied to isolate the white lane lines in the HSV color space, while reducing background noise. Shadows and lighting variations are accounted for by setting a wider range in brightness levels. Specifically:
   - Lower and upper HSV thresholds are adjusted to capture white even under shadows.
   - This allows for consistent detection of lane lines under varying lighting conditions.
2. **Morphological operations:** Cleans up the color mask by removing small noise and closing gaps in the lane lines for more consistent detection.
3. **Canny edge detection:** Identifies edges within the cleaned-up mask, making lane lines stand out.
4. **Line detection (hough transform):** Detects straight lines in the edge-detected image, filtering for horizontal lines that likely correspond to lane lines.

![lane_detection_process](https://github.com/user-attachments/assets/65d571fa-4062-4bad-a922-2d8235820cfc)

## Vehicle Position Measurement


## Converting Pixels to Real-World Measurement


## Pilot Data


## Precision Test

