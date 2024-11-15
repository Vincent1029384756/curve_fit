import cv2
import numpy as np

# Load the image
image_path = "/home/wen-gu/Documents/439_lab/masked/frame_0351.jpg"
image = cv2.imread(image_path)

# List to store selected points
points = []

def select_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        points.append((x, y))
        print(f"Point selected: ({x}, {y})")
        # Draw the point on the image
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select Points", image)
        # If two points are selected, calculate the distance
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            pixel_distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            print(f"Pixel Distance: {pixel_distance:.2f} pixels")
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.imshow("Select Points", image)

# Display the image and set the callback function
cv2.imshow("Select Points", image)
cv2.setMouseCallback("Select Points", select_points)

print("Click on two points to measure the distance.")
cv2.waitKey(0)
cv2.destroyAllWindows()
