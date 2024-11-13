import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
csv_output_path = 'output/without_nback.csv'
data = pd.read_csv(csv_output_path)

# Set the sampling rate (e.g., 30 samples per second for 30 Hz)
sampling_rate = 30  # Adjust this to match your data's actual sampling rate

# Extract relevant columns
time = data['seconds']
distance_from_lane_line = pd.to_numeric(data['cm_from_lane_line'], errors='coerce')  # Convert to numeric, preserving NaNs

# Interpolate missing values for smoother analysis
distance_from_lane_line_interpolated = distance_from_lane_line.interpolate()

# Calculate the difference between consecutive rows to measure changes
change_magnitude = distance_from_lane_line_interpolated.diff().abs()

# Define window size (in seconds) and convert to rows
window_duration = 1  # Duration for calculating frequency in seconds (e.g., 1-second windows)
window_size = window_duration * sampling_rate  # Convert duration to rows based on sampling rate

# Count changes above a threshold within each rolling window
threshold = 5  # Define a threshold for "significant" change in cm
significant_changes = (change_magnitude > threshold).rolling(window=window_size).sum()

# Convert counts of significant changes to frequency in Hz
change_frequency_hz = significant_changes / window_duration

# Plotting only the frequency of significant changes
plt.figure(figsize=(12, 6))

# Plot the frequency of significant changes (in Hz) in red
plt.plot(time, change_frequency_hz, label='Frequency of Significant Changes (Hz)', color='red')

# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency of Significant Changes (Hz)')
plt.title('Frequency of Significant Lane Position Changes Over Time')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()