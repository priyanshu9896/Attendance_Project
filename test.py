import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
import pyttsx3

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Configuration
DATA_DIR = "data"
ATTENDANCE_DIR = "Attendance"
STATIC_DIR = "static"  # Changed directory to 'static' for storing photos
PHOTO_DIR = os.path.join(STATIC_DIR, "Photos")  # Updated path to the 'static' folder
BACKGROUND_IMG = 'background img.png'  # Updated path to the root directory
HAAR_CASCADE = os.path.join(DATA_DIR, 'haarcascade_frontalface_default.xml')
COL_NAMES = ['ROLL NO', 'NAME', 'TIME', 'PHOTO']  # Updated column names to include 'ROLL NO'

# Utility function for directory creation
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)  # Ensure static folder exists
os.makedirs(PHOTO_DIR, exist_ok=True)  # Ensure Photos folder exists inside 'static'

# Ask user for name and theme
target_name = input("Enter the name to announce: ")
roll_no = input("Enter your roll number: ")  # Ask for roll number
theme = input("Select theme (business): ").strip().lower()
if theme not in ["business"]:
    print("Invalid theme. Defaulting to business mode.")
    theme = "business"
    engine.say("Invalid theme. Defaulting to business mode.")
    engine.runAndWait()

# Theme-specific settings
if theme == "business":
    box_color = (0, 0, 255)  # Blue
    text_color = (255, 255, 255)  # White
    overlay_color = (0, 0, 150)  # Semi-transparent blue

engine.say(f"{theme.capitalize()} theme selected.")
engine.runAndWait()

# Load the background image
background = cv2.imread(BACKGROUND_IMG)
if background is None:
    print("Error: Background image not found.")
    engine.say("Error: Background image not found.")
    engine.runAndWait()
    exit()

# Initialize video capture
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Unable to access webcam.")
    engine.say("Error: Unable to access webcam.")
    engine.runAndWait()
    exit()

# Load the Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)

# Utility function for HUD
def draw_transparent_rect(image, start_point, end_point, color, transparency):
    overlay = image.copy()
    cv2.rectangle(overlay, start_point, end_point, color, -1)
    cv2.addWeighted(overlay, transparency, image, 1 - transparency, 0, image)

# Resize background to fit the screen
def resize_background(background, frame_shape):
    return cv2.resize(background, (frame_shape[1], frame_shape[0]))

# Announcements and attendance tracking
announced_names = set()
recorded_attendance = set()

# Main loop
while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Resize the background dynamically to match the webcam resolution
    background_resized = resize_background(background, frame.shape)

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw bounding box around detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
        draw_transparent_rect(frame, (x, y - 30), (x + w, y), overlay_color, 0.6)
        cv2.putText(frame, target_name, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

        # Add timestamp
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        draw_transparent_rect(frame, (x, y + h + 5), (x + w, y + h + 30), overlay_color, 0.4)
        cv2.putText(frame, timestamp, (x + 10, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

        # Announce name if not already announced
        if target_name not in announced_names:
            engine.say(f"Hello, {target_name}. Welcome.")
            engine.runAndWait()
            announced_names.add(target_name)

    # Overlay frame on the background
    left_box_x, left_box_y = 50, 50  # Define placement of webcam feed
    frame_resized = cv2.resize(frame, (400, 300))
    background_resized[left_box_y:left_box_y + 300, left_box_x:left_box_x + 400] = frame_resized

    # Show the final overlay
    cv2.imshow("Face Recognition - Business Mode", background_resized)

    # Key handling
    k = cv2.waitKey(1)
    if k == ord('a'):  # Mark attendance and capture photo
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        # Save photo
        photo_filename = f"{target_name}_{timestamp.replace(':', '-')}.jpg"
        photo_path = os.path.join(PHOTO_DIR, photo_filename)  # Photo saved in 'static/Photos'
        cv2.imwrite(photo_path, frame)

        # Mark attendance with roll number
        attendance = [roll_no, target_name, timestamp, photo_filename]
        recorded_attendance.add(target_name)
        csv_path = os.path.join(ATTENDANCE_DIR, f"Attendance_{date}.csv")
        is_new_file = not os.path.exists(csv_path)
        with open(csv_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if is_new_file:
                writer.writerow(COL_NAMES)
            writer.writerow(attendance)
        
        engine.say(f"Attendance recorded for {target_name}, and photo saved.")
        engine.runAndWait()
    elif k == ord('o'):  # Exit
        break

# Cleanup
video.release()
cv2.destroyAllWindows()
