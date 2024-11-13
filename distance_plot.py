import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_output_path = 'output/without_nback.csv'
data = pd.read_csv(csv_output_path)

# Extract relevant columns
time = data['seconds']
distance_from_lane_line = pd.to_numeric(data['cm_from_lane_line'], errors='coerce')  # Convert to numeric, preserving NaNs

# Interpolate missing values for smooth plotting (optional, based on your preference)
distance_from_lane_line_interpolated = distance_from_lane_line.interpolate()

# Plotting the distance from lane line over time
plt.figure(figsize=(12, 6))

# Plot distance from lane line in blue
plt.plot(time, distance_from_lane_line_interpolated, label='Distance from Lane Line (cm)', color='blue')

# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Distance from Lane Line (cm)')
plt.title('Distance from Lane Line Over Time')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()