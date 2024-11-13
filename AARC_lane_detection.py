import cv2
import numpy as np
import csv

# Define the pixel-to-centimeter conversion factor
PIXEL_TO_CM = 0.365  # cm per pixel

# Load calibration data
calibration_data = np.load('calibration_data.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

# Set wheel position directly
WHEEL_POSITION_X = 605
WHEEL_POSITION_Y = 444

def calculate_angle(line):
    """Calculate the angle of the line in degrees."""
    x1, y1, x2, y2 = line
    return np.degrees(np.arctan2(y2 - y1, x2 - x1))

def is_lane_line(line, slope_range=(0.05, 0.3)):
    """Filter lines based on the slope range to isolate lane lines."""
    x1, y1, x2, y2 = line
    if x2 == x1:  # avoid division by zero for vertical lines
        return False
    slope = abs((y2 - y1) / (x2 - x1))
    return slope_range[0] <= slope <= slope_range[1]

def detect_lane_lines(frame):
    """Detect white horizontal lane lines in a frame."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200]) 
    upper_white = np.array([180, 50, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
    
    # Apply Gaussian blur before edge detection
    edges = cv2.GaussianBlur(mask_white, (9, 9), 0)
    edges = cv2.Canny(edges, 50, 150)

    # Detect lines using Hough Transform with adjusted parameters
    lines = cv2.HoughLinesP(edges, 
                            rho=1, 
                            theta=np.pi / 360,  
                            threshold=80,       
                            minLineLength=100,  
                            maxLineGap=50)     
    
    filtered_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if is_lane_line((x1, y1, x2, y2)):  # Filter based on slope range
                filtered_lines.append((x1, y1, x2, y2))
    
    return filtered_lines

def crop_bottom_left_quarter(frame):
    """Crop the bottom-left quarter of the frame."""
    height, width = frame.shape[:2]
    return frame[height // 2:, :width // 2]  # Crop to bottom-left quarter

def process_frame(frame):
    """Process a cropped frame, detect lane lines, and measure distance from the wheel point with sub-pixel accuracy."""
    # Step 1: Crop the frame first
    cropped_frame = crop_bottom_left_quarter(frame)
    
    # Step 2: Apply undistortion only to the cropped frame
    undistorted_cropped_frame = cv2.undistort(cropped_frame, camera_matrix, dist_coeffs)
    
    # Define the reference point (wheel position in the cropped frame)
    reference_x = WHEEL_POSITION_X
    reference_y = WHEEL_POSITION_Y

    filtered_lines = detect_lane_lines(undistorted_cropped_frame)
    frame_with_lines = undistorted_cropped_frame.copy()

    # Draw the detected horizontal lane lines
    for line in filtered_lines:
        x1, y1, x2, y2 = line
        cv2.line(frame_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw the reference vertical line from the wheel position upwards
    cv2.line(frame_with_lines, (reference_x, reference_y), (reference_x, 0), (255, 0, 0), 1)

    # Initialize the closest intersection point
    closest_distance_px = None
    closest_intersection_y = None

    # Calculate precise intersections with each horizontal line
    for x1, y1, x2, y2 in filtered_lines:
        if min(x1, x2) <= reference_x <= max(x1, x2):  # Check if line crosses vertical at reference_x
            # Calculate precise intersection with sub-pixel accuracy
            y_intersect = y1 + (reference_x - x1) * (y2 - y1) / (x2 - x1)
            if y_intersect < reference_y:
                distance_px = reference_y - y_intersect  # Vertical distance in pixels
                if closest_distance_px is None or distance_px < closest_distance_px:
                    closest_distance_px = distance_px
                    closest_intersection_y = y_intersect

    # Convert closest distance to centimeters
    vertical_distance_cm = None
    if closest_distance_px is not None:
        vertical_distance_cm = closest_distance_px * PIXEL_TO_CM
        # Draw the precise measurement line in red
        cv2.line(frame_with_lines, (reference_x, reference_y), (reference_x, int(closest_intersection_y)), (0, 0, 255), 2)

    return frame_with_lines, vertical_distance_cm

# Load video
video_input_path = 'videos/without_nback.mkv'
video_output_path = 'output/without_nback_processed.mp4'
csv_output_path = 'output/without_nback.csv'

video_capture = cv2.VideoCapture(video_input_path)

fps = video_capture.get(cv2.CAP_PROP_FPS)
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_output_path, fourcc, fps, (frame_width, frame_height))

with open(csv_output_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['frame', 'seconds', 'cm_from_lane_line'])

    frame_number = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Process frame (crop and undistort within process_frame function)
        frame_with_lines, vertical_distance_cm = process_frame(frame)
        
        # Resize frame if dimensions don't match VideoWriter dimensions
        if frame_with_lines.shape[1] != frame_width or frame_with_lines.shape[0] != frame_height:
            frame_with_lines = cv2.resize(frame_with_lines, (frame_width, frame_height))

        # Write data to CSV
        timestamp = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Timestamp in seconds
        if vertical_distance_cm is not None:
            csv_writer.writerow([frame_number, timestamp, vertical_distance_cm])
        else:
            csv_writer.writerow([frame_number, timestamp, 'NaN'])

        # Write processed frame to output video
        video_writer.write(frame_with_lines)
        frame_number += 1

# Release resources
video_capture.release()
video_writer.release()
cv2.destroyAllWindows()