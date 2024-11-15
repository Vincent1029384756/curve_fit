import cv2

# Load the image
image_path = "/home/wen-gu/Documents/439_lab/frames/frame_0227.jpg"
image = cv2.imread(image_path)
clone = image.copy()

# Initialize the list of ROI coordinates
roi_coordinates = []

# Define the mouse callback function
def select_roi(event, x, y, flags, param):
    global roi_coordinates
    if event == cv2.EVENT_LBUTTONDOWN:  # On left mouse button press
        roi_coordinates = [(x, y)]  # Start point
    elif event == cv2.EVENT_LBUTTONUP:  # On left mouse button release
        roi_coordinates.append((x, y))  # End point
        # Draw the rectangle on the image
        cv2.rectangle(clone, roi_coordinates[0], roi_coordinates[1], (0, 255, 0), 2)
        cv2.imshow("ROI Selector", clone)

# Display the image and set the mouse callback
cv2.imshow("ROI Selector", image)
cv2.setMouseCallback("ROI Selector", select_roi)

print("Select the ROI by clicking and dragging. Press 'c' to confirm or 'r' to reset.")

while True:
    # Display the image
    cv2.imshow("ROI Selector", clone)
    key = cv2.waitKey(1) & 0xFF

    # Press 'r' to reset the ROI selection
    if key == ord("r"):
        clone = image.copy()
        roi_coordinates = []

    # Press 'c' to confirm the ROI selection
    elif key == ord("c"):
        break

cv2.destroyAllWindows()

# Extract the vertical region coordinates
if len(roi_coordinates) == 2:
    x_start, y_start = roi_coordinates[0]
    x_end, y_end = roi_coordinates[1]
    print(f"Selected ROI: Start = ({x_start}, {y_start}), End = ({x_end}, {y_end})")

    # Optional: Crop the ROI and display it
    cropped_roi = image[y_start:y_end, :]
    cv2.imshow("Cropped ROI", cropped_roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No ROI selected.")
