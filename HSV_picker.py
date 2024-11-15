import cv2
import numpy as np

def nothing(x):
    pass

# Load the image you want to analyze
image_path = "/home/wen-gu/Documents/439_lab/frames/frame_0227.jpg"
image = cv2.imread(image_path)

# Convert to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window and trackbars for adjusting HSV ranges
cv2.namedWindow("Trackbars")
cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

while True:
    # Get current positions of the trackbars
    lh = cv2.getTrackbarPos("Lower H", "Trackbars")
    ls = cv2.getTrackbarPos("Lower S", "Trackbars")
    lv = cv2.getTrackbarPos("Lower V", "Trackbars")
    uh = cv2.getTrackbarPos("Upper H", "Trackbars")
    us = cv2.getTrackbarPos("Upper S", "Trackbars")
    uv = cv2.getTrackbarPos("Upper V", "Trackbars")

    # Create a mask based on the current trackbar positions
    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the mask and the result
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
