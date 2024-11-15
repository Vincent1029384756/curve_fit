import cv2
import os
import numpy as np

# Define input and output directories
input_path = "/home/wen-gu/Documents/439_lab/frames"
output_path = "/home/wen-gu/Documents/439_lab/masked"

# Create the output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Define the lower and upper HSV bounds for the target color
lower_hsv = (0, 0 , 145)
upper_hsv = (179, 255, 255)

# Process each frame and save to the new path
for file in os.listdir(input_path):
    if file.endswith(".jpg"):
        # Load the image
        file_path = os.path.join(input_path, file)
        image = cv2.imread(file_path)

        # Convert to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create the binary mask
        mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

        # Turn masked regions white and everything else black
        output_image = np.zeros_like(image, dtype=np.uint8)  # Start with a black canvas
        output_image[mask > 0] = [255, 255, 255]  # Set masked regions to white

        # Save the processed image to the output path
        output_jpg_path = os.path.join(output_path, file)
        cv2.imwrite(output_jpg_path, output_image)
        print(f"Processed and saved: {output_jpg_path}")
