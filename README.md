# 📷 Face Recognition-Based Smart Attendance System

## 🚀 Overview
This project is an AI-powered attendance system that leverages Face Recognition technology to automate the process of marking attendance. The system captures live video feed, detects faces, recognizes registered individuals, and logs attendance automatically. It is designed to enhance accuracy, security, and efficiency in attendance management for workplaces, institutions, and events.

## 🎯 Features
✅ Face Detection & Recognition – Uses OpenCV and a trained model for recognizing faces.
📸 Live Camera Feed – Captures video feed in real-time for face recognition.
📂 Attendance Logging – Stores attendance data in CSV format with timestamps.
🗂️ Photo Capture – Saves recognized face snapshots in a designated folder.
🔊 Text-to-Speech Alerts – Announces attendance confirmation using pyttsx3.
📊 GUI Overlay – Displays real-time attendance details with an interactive interface.
🔐 Secure & Efficient – Prevents proxy attendance by ensuring unique face matches.

## 🏗️ Tech Stack
🔹 Python – Core development language
🔹 OpenCV – Image processing & face detection
🔹 NumPy – Efficient numerical operations
🔹 Haar Cascades – Face detection model
🔹 Pyttsx3 – Text-to-speech for voice alerts
🔹 CSV – Data storage for attendance logs

## 📦 Installation
Clone the repository and install dependencies:
<img width="735" alt="Screenshot 2025-02-18 at 7 55 38 PM" src="https://github.com/user-attachments/assets/947ce85d-a1e6-409b-8847-60b583a05bd2" />

bash
Copy
Edit
git clone https://github.com/sourav-sudow/face-recognition-attendance.git
cd face-recognition-attendance
pip install -r requirements.txt
▶️ Running the App
To start the face recognition-based attendance system, run:

bash
Copy
Edit
python test.py

## 📸 Screenshots
![1](https://github.com/user-attachments/assets/32b3a866-792c-499d-9b38-dc9ff9bb2090)
![2](https://github.com/user-attachments/assets/3d0a79af-4f01-4bd4-a74c-899cb734f4bf)
![3](https://github.com/user-attachments/assets/c4663915-4e14-4844-acb2-7f38429b9eb5)
![4](https://github.com/user-attachments/assets/b1d767fc-5877-47aa-8627-e41d25eff43b)


## 📑 File Structure
<img width="735" alt="Screenshot 2025-02-18 at 7 56 55 PM" src="https://github.com/user-attachments/assets/0c47de3c-15fd-4d3a-9661-5646580c6071" />

## 🏆 How It Works
Start the system – Runs the live webcam feed.
Face Detection & Recognition – Identifies faces from the feed.
Mark Attendance – If a recognized face is detected, attendance is logged.
Capture & Store Photo – Saves the captured face in the static/Photos folder.
Audio Confirmation – Announces the user’s name upon successful recognition.
CSV Logging – Attendance details (Name, Roll No, Time, and Photo) are saved.
🚀 Future Enhancements
📌 Web-Based Dashboard – A user-friendly interface for managing attendance data.
🔍 Multiple Camera Support – Expanding recognition to multiple devices.
📊 Analytics & Reports – Advanced statistics on attendance trends.
🔐 Database Integration – Storing data in a relational database (SQL).

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository, create a new branch, and submit a pull request.

## 🔗 License
MIT License – Free to use and modify.

