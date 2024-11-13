import pandas as pd

# Load the CSV data
csv_output_path = 'output/with_nback.csv'
data = pd.read_csv(csv_output_path)

# Convert the 'cm_from_lane_line' column to numeric, preserving NaNs
distance_from_lane_line = pd.to_numeric(data['cm_from_lane_line'], errors='coerce')

# Calculate summary statistics
mean_distance = distance_from_lane_line.mean()
min_distance = distance_from_lane_line.min()
max_distance = distance_from_lane_line.max()
median_distance = distance_from_lane_line.median()
std_dev_distance = distance_from_lane_line.std()

# Print results
print("Distance from Lane Line Summary Statistics:")
print(f"Mean: {mean_distance:.2f} cm")
print(f"Minimum: {min_distance:.2f} cm")
print(f"Maximum: {max_distance:.2f} cm")
print(f"Median: {median_distance:.2f} cm")
print(f"Standard Deviation: {std_dev_distance:.2f} cm")