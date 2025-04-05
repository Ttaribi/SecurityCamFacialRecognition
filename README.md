📌 About the Project

This application captures webcam footage, detects faces, and identifies individuals using a machine learning-powered LBPH (Local Binary Patterns Histograms) algorithm. It logs both recognized and unknown visitors with timestamps and displays them live on-screen in a sidebar panel.

The project is designed as a lightweight security camera system with basic tracking, database storage, and training functionality — all from scratch.


🚀 Features

✅ Real-time facial detection and recognition via webcam with 85% accuracy

✅ Automatic logging of recognized and unknown individuals with timestamps  

✅ Training pipeline that lets users register by capturing face images  

✅ SQLite database integration** to store student profiles (ID, Name, Age)  

✅ On-screen countdown before photo capture during training  


---

 📹 Demo Walkthrough




🛠 Technologies Used

Backend / Core Logic

Python – Main programming language

OpenCV (cv2) – Real-time computer vision and facial recognition

NumPy – For image array manipulation and model training

SQLite – Lightweight embedded database for storing user data (ID, Name, Age)

PIL (Pillow) – For image preprocessing before training



🧠 Machine Learning

LBPH Face Recognizer (Local Binary Patterns Histogram) – Machine learning model for facial classification

Haar Cascade Classifier – Pretrained model used to detect frontal faces in frames



📦 Data Handling

YAML model file (.yml) – Stores trained recognition data
