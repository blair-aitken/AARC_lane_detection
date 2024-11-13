## Overview

This project detects lane lines in video footage captured from a GoPro HERO11 mounted on the outside of a vehicle. This setup allows for consistent lane tracking and accurate measurement of lane position relative to the vehicle’s center.

## Dependencies

This project requires the following dependencies:
* Python
* OpenCV
* NumPy
* Matplotlib (for data visualization)

## Camera Calibration

Given the GoPro HERO11’s wide-angle lens, calibration is essential to correct lens distortion and ensure accurate lane measurements. The following calibration steps use a chessboard pattern to generate the necessary camera parameters.

### Calibration process

1.	**Load calibration video:** The calibration script (`camera_calibration.py`) loads a video of a chessboard pattern (calibration_video.mkv), where each frame displays the chessboard in various positions to capture lens distortion from multiple angles.
   
3. **Capture snapshots:** While playing the video, press **'s'** to save frames with the chessboard visible in different locations. Aim to take between 10 to 20 snapshots, as these will be used for calculating calibration parameters. Each snapshot is saved automatically in the `calibration_images` folder.

4. **Compute camera matrix and distortion coefficients:** The script then loads the saved snapshots, detects chessboard corners, and calculates the camera matrix and distortion coefficients using `cv2.calibrateCamera()`. These calibration parameters allow for correcting distortion in subsequent frames.

5. **Save calibration data:** The camera matrix and distortion coefficients are saved to a file (`calibration_data.npz`) for later use in undistorting the video frames.

### Example usage

Run `camera_calibration.py` to perform camera calibration. Ensure `calibration_video.mkv` is located in the project directory. The script will guide you through capturing the snapshots needed for calibration.

**Distortion correction:** The calibration data is applied to each frame using cv2.undistort() to correct distortion, providing a consistent and clear view of the lane lines.

### Distortion correction example

The resulting calibration data can then be applied to correct lens distortion in your main video footage, ensuring accurate lane position measurements.

![calibration_process](https://github.com/user-attachments/assets/64fdae40-233c-4939-81a7-23d8e52bf212)

## Lane Line Detection

### Detecting lane lines in single frames

Lane lines are detected in each frame using OpenCV’s image processing tools:

1. **Color filtering:** The `cv2.inRange()` function is used to create a mask that isolates white lane lines within a specified HSV color range. By setting lower and upper HSV thresholds, the mask can capture white areas even under shadows or changing light conditions. This step helps separate lane lines from the background:
    - Lower and upper HSV thresholds are adjusted to include a wider brightness range, accommodating varying lighting conditions.
    - This enables consistent detection of lane lines despite lighting variations on the road.

2. **Morphological operations:** The `cv2.morphologyEx()` function is applied with morphological transformations, such as closing (to fill small gaps) and opening (to remove small noise) within the mask. A rectangular kernel is used to control the extent of these operations:
    - **Closing** fills small gaps in the lane lines, making them more continuous and easier to detect as single lines.
    - **Opening** removes small specks of noise that may interfere with edge detection, ensuring a cleaner mask for further processing.

3. **Canny edge detection:** The `cv2.Canny()` function is used to detect edges within the cleaned-up mask. By applying a Gaussian blur to the mask before edge detection, the `Canny()` function can better identify strong edges (such as lane lines) while reducing noise from less prominent edges:
    - The function takes two thresholds (50 and 150) to filter edges based on intensity, making the lane lines stand out more clearly.

4. **Line detection:** The `cv2.HoughLinesP()` function is used to detect straight line segments within the edge-detected image. This function uses a probabilistic Hough Transform to find line segments that match specified parameters:
    - **rho**: The distance resolution of the accumulator, set to 1 pixel.
    - **theta**: The angle resolution, set to a small value to capture horizontal lines.
    - **threshold**: The minimum number of intersections needed to detect a line.
    - **minLineLength**: The minimum length of a detected line segment, set to 100 pixels to avoid detecting short, irrelevant lines.
    - **maxLineGap**: The maximum gap between points on a line for them to be connected, set to 50 pixels to ensure that continuous lane lines are detected.

![lane_detection_process](https://github.com/user-attachments/assets/65d571fa-4062-4bad-a922-2d8235820cfc)

### Tracking lane lines across the entire video

This detection process is applied to each frame of the video one-by-one, allowing accurate tracking of lane positions across the entire duration of the footage.

Lane position is measured relative to a defined reference point (i.e., the edge of the wheel) directly vertically to the closest detected lane line, ensuring measurements are taken from a consistent position in each frame. These measurements are initially captured in pixels and later converted to centimeters, providing accurate real-world distance measurements.

![sample](https://github.com/user-attachments/assets/9024a65a-7a28-4fcd-acde-4697698979b4)

## False Readings

Occasionally, due to varying lighting conditions, the lane detection system may pick up false readings. For example, shadows, reflections, or direct sunlight can cause sudden changes in detected lane positions, leading to temporary false detections. (Screenshot here to illustrate the effect.)

![false_readings](https://github.com/user-attachments/assets/415d3da4-2196-4e5c-bcd0-460cce0b3701)

To address this, a **frequency threshold in Hz** has been implemented. This threshold identifies and removes data segments where the frequency of lane position changes exceeds a natural range, indicating likely false readings rather than genuine lane shifts. Here’s how this process works:

1. **Frequency Analysis of Lane Position Changes**: The system calculates the frequency of significant lane position changes over time, using a sliding window (e.g., every 50 frames). High frequencies often correspond to erratic fluctuations caused by lighting artifacts rather than actual vehicle movement.

2. **Setting the Frequency Threshold**: A frequency threshold is defined based on expected lane stability. If the frequency of changes in lane position exceeds this threshold (e.g., 15 Hz), it is flagged as a potential false reading. This threshold allows the system to differentiate between normal lane variations and rapid fluctuations likely due to environmental interference.

3. **Filtering Out High-Frequency Segments**: Any segment with a frequency above the threshold is:
   - **Excluded from Further Analysis**: These flagged sections are not included in the primary analysis to ensure they don’t impact lane tracking accuracy.
   - **Visually Highlighted**: High-frequency segments are plotted in a different color (e.g., red) on visualizations, allowing for easy identification and further inspection if needed.

By applying this frequency-based filtering, the system can reduce the impact of lighting-induced false readings and maintain reliable lane detection. This approach helps ensure that only genuine lane position data is analyzed, improving the robustness of the system even in challenging lighting conditions.

## Vehicle Position Measurement

The distance from the vehicle to the lane line is measured in pixels and converted to centimeters using a pixel-to-centimeter conversion factor.


## Converting Pixels to Real-World Measurement


## Pilot Data


## Precision Test
