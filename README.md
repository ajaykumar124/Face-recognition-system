# Face Recognition Application - README

## Overview

This is a face recognition application that allows users to:
1. Enroll new faces by capturing images.
2. Train a model using captured images.
3. Load a pre-trained model.
4. Perform real-time face recognition using a webcam.

The application uses OpenCV and the `face_recognition` library for face detection and recognition.

## Prerequisites

Ensure you have the following dependencies installed:

- Python 3.6 or later
- OpenCV
- face_recognition
- numpy
- PIL (Pillow)
- tkinter

You can install these dependencies using `pip`:

```bash
pip install opencv-python-headless face_recognition numpy Pillow
pip install opencv-python-headless
pip install face_recognition
pip install numpy
pip install Pillow
pip install tk

```

## Setting Up

1. **Create Database**: Ensure an SQLite database named `users.db` is created with a `users` table for user authentication.
2. **Background Images**: Place your background images (`back.png` for login/signup windows and `background.jpg` for the main face recognition window) in the same directory as the script.
3. **Encodings Directory**: Create a directory named `encodings` to store the trained model files.

## Usage

1. **Run the Application**:
   ```bash
   python your_script_name.py
   ```

2. **Signup/Login**:
   - On the main screen, you can either sign up for a new account or log in with existing credentials.
   - Passwords must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, and one digit.

3. **Enroll Faces**:
   - After logging in, click the "Enroll Faces" button to capture and save 25 photos of a face.
   - Enter the name of the person when prompted.

4. **Train Faces**:
   - Click the "Train Faces" button to train a face recognition model using the captured images.
   - Select the directory containing the subdirectories of face images.

5. **Load Model**:
   - Click the "Load Model" button to load a pre-trained model from the `encodings` directory.
   - Select a model file from the list.

6. **Start/Stop Face Recognition**:
   - Click the "Start Face Recognition" button to start the real-time face recognition using the webcam.
   - Click "Stop Video Capture" to stop the recognition process.

## Detailed Description

### Database Setup

A SQLite database is used to store user credentials:

```python
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
```

### Sign Up

The `signup` function checks for password strength and ensures the username does not already exist before adding a new user to the database.

### Login

The `authenticate` function verifies user credentials. On successful login, it starts a new thread to run `cap.py` and displays a loading window.

### Main Window

The main window provides buttons for enrolling faces, training faces, loading a model, and starting/stopping face recognition.

### Enroll Faces

Captures 25 images from the webcam and saves them in a directory named after the user's input.

### Train Faces

Trains a face recognition model using images from a selected directory. Saves the trained model in the `encodings` directory with a timestamp.

### Load Model

Loads a pre-trained model from the `encodings` directory. Allows the user to select or delete model files.

### Real-Time Face Recognition

Uses the webcam to capture frames and perform face recognition using the loaded model. Recognized faces are highlighted with a rectangle and name label.

## Notes

- Ensure your webcam is properly set up and accessible by the application.
- The application performs best with clear and well-lit images.
- Training large datasets might take some time; ensure you wait until the process is complete.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

---

Enjoy using the face recognition application! If you have any issues, feel free to reach out for support.
