import cv2
import os

# load the video
mp4_path = "/home/wen-gu/Documents/439_lab/mp4/sample1.mp4"
output_path = "/home/wen-gu/Documents/439_lab/frames"

cap = cv2.VideoCapture(mp4_path)

# Check if the video was loaded successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames
duration = frame_count / fps  # Total video duration in seconds

print(f"Video FPS: {fps}, Total Frames: {frame_count}, Duration: {duration:.2f}s")

# Extract frames and save them with framend-based names
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Finished reading video.")
        break

    # Save the frame as an image file
    frame_filename = os.path.join(output_path, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_filename, frame)
    print(f"Saved: {frame_filename}")
    
    frame_count += 1

cap.release()
print("All frames have been extracted and saved.")