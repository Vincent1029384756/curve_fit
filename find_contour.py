import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define input and output directories
input_path = "/home/wen-gu/Documents/439_lab/masked"
out_folder = "/home/wen-gu/Documents/439_lab/contours"
csv_dir = "/home/wen-gu/Documents/439_lab/csv"
csv_file = 'sample2.csv'

# Ensure the output folder and CSV directory exist
os.makedirs(out_folder, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

# Define the full ROI (x_start, y_start, x_end, y_end)
x_start, y_start, x_end, y_end = 153, 66, 311, 649

# Scaling factor for pixel to mm conversion
pixel_length = 70  # Length in pixels
#pixel_length = 75
real_world_length_mm = 10  # Corresponding length in mm
scaling_factor = real_world_length_mm / pixel_length

# Initialize headers for the CSV file
csv_path = os.path.join(csv_dir, csv_file)
if not os.path.exists(csv_path):
    with open(csv_path, 'w') as f:
        f.write(','.join(['frame_num', 'time [s]', 'cx [mm]', 'cy [mm]']) + '\n')

# Sort files numerically
files = sorted(os.listdir(input_path), key=lambda x: int(x.split('_')[-1].split('.')[0]))

# Process each frame
frame_num = 0
frame_list = []
cx_list = []
cy_list = []
time_list = []

for file in files[62: ]:
    if file.endswith(".jpg"):
        # Load the masked image
        file_path = os.path.join(input_path, file)
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Crop to the ROI
        cropped_image = image[y_start:y_end, x_start:x_end]

        # Find contours in the cropped region
        contours, _ = cv2.findContours(cropped_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour by area
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate moments to find the center
            moments = cv2.moments(largest_contour)

            if moments["m00"] > 0:  # Avoid division by zero
                cx = int(moments["m10"] / moments["m00"]) + x_start  # Adjust x-coordinate
                cy = int(moments["m01"] / moments["m00"]) + y_start  # Adjust y-coordinate
                cx_mm = cx * scaling_factor
                cy_mm = -cy * scaling_factor

                cx_list.append(cx_mm)
                cy_list.append(cy_mm)
                frame_list.append(frame_num)
                time = frame_num / 240  # Time in seconds based on FPS
                time_list.append(time)

                # Append to CSV
                df_to_append = pd.DataFrame([[frame_num, time, cx_mm, cy_mm]], columns=['frame_num', 'time [s]', 'cx [mm]', 'cy [mm]'])
                df_to_append.to_csv(csv_path, mode='a', index=False, header=False)

                # Print the center's coordinates
                print(f"{file}: Center = ({cx_mm:.2f} mm, {cy_mm:.2f} mm)")

                # Optional: Draw the contour and center on the image for visualization
                output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(output_image[y_start:y_end, x_start:x_end], [largest_contour], -1, (0, 255, 0), 2)  # Green contour
                cv2.circle(output_image, (cx, cy), 5, (255, 0, 0), -1)  # Blue center point

                # Save the visualization
                output_path = os.path.join(out_folder, f"output_{file}")
                cv2.imwrite(output_path, output_image)
                print(f"Saved visualization: {output_path}")
            else:
                print(f"{file}: Largest contour has zero area.")
        else:
            print(f"{file}: No contours found.")
        frame_num += 1

# Plot results
plt.figure()
plt.plot(time_list, cy_list, label="y-coordinate of center [mm]")
plt.xlabel("Time [s]")
plt.ylabel("y-Coordinate [mm]")
plt.title('00-50')
#plt.title('00-30')
plt.grid()
plt.legend()
plt.show()
