import cv2
import pickle
import numpy as np
import os

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Start the video capture
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not open video device.")
    exit()

facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
if facedetect.empty():
    print("Error: Could not load Haar Cascade file.")
    exit()

faces_data = []
i = 0

# Get user's details
roll_no = input("Enter Your Roll Number: ")
name = input("Enter Your Name: ")

# Combine roll number and name for a unique identifier
user_id = f"{roll_no}_{name}"

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (37, 37))  # Resize to 37x37 (1400 features)
        if len(faces_data) < 5 and i % 10 == 0:  # Capture 5 photos instead of 100
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    # Display the frame with faces detected
    cv2.imshow("Frame", frame)

    # Key Press Handling
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 5:  # Stop once 5 photos are captured
        break
    if k == ord('d'):  # Press 'd' to delete all face data and reset attendance
        print("Deleting all face data and resetting attendance...")
        if os.path.exists('data/users.pkl'):
            os.remove('data/users.pkl')  # Delete users pickle file
        if os.path.exists('data/faces_data.pkl'):
            os.remove('data/faces_data.pkl')  # Delete faces pickle file
        print("All data deleted successfully!")
        break

video.release()
cv2.destroyAllWindows()

# Convert the faces_data to numpy array and reshape it to have 1400 features per image
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(5, -1)  # Reshape to (5, 1400)

# Save roll numbers, names, and faces data
# Handle users.pkl (stores user ID and name mappings)
if 'users.pkl' not in os.listdir('data/'):
    users = {user_id: name}
    with open('data/users.pkl', 'wb') as f:
        pickle.dump(users, f)
else:
    with open('data/users.pkl', 'rb') as f:
        try:
            users = pickle.load(f)
            if not isinstance(users, dict):
                raise ValueError("Loaded users data is not a dictionary.")
        except Exception as e:
            print(f"Error loading users data: {e}")
            users = {}  # Reset to an empty dictionary if corrupted
    
    users[user_id] = name
    with open('data/users.pkl', 'wb') as f:
        pickle.dump(users, f)

# Handle faces_data.pkl (stores user IDs and their face data)
if 'faces_data.pkl' not in os.listdir('data/'):
    # If no data exists, initialize a dictionary and save the first entry
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump({user_id: faces_data}, f)
else:
    # Load existing data and ensure it's a dictionary
    with open('data/faces_data.pkl', 'rb') as f:
        try:
            all_faces_data = pickle.load(f)
            if not isinstance(all_faces_data, dict):
                raise ValueError("Loaded faces data is not a dictionary.")
        except Exception as e:
            print(f"Error loading faces data: {e}")
            all_faces_data = {}  # Reset to an empty dictionary if corrupted
    
    # Add the new user's face data
    all_faces_data[user_id] = faces_data
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(all_faces_data, f)

print("Registration complete and data saved successfully!")
