import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import face_recognition
import numpy as np
import pickle
import os

# Create a Tkinter window
window = tk.Tk()
window.title("Face Recognition")

# Set the background image
background_image = ImageTk.PhotoImage(Image.open("back6.jpg"))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load known face encodings and names from the "encodings.pickle" file
data = pickle.loads(open("D:\FaceRecognitionD\encodings.pickle", "rb").read())
video_capture = cv2.VideoCapture(0)

frame_count = 0
skip_frames = 5
# Set the threshold value for confidence
threshold = 0.5

# Create a login frame
login_frame = tk.Frame(window)

# Login labels and entry fields
username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 14))
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=("Helvetica", 14))
username_entry.pack(pady=10)

password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 14))
password_label.pack(pady=10)
password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 14))
password_entry.pack(pady=10)

# Login button
login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 14),
                         command=lambda: login(username_entry.get(), password_entry.get()))
login_button.pack(pady=10)

# Create a label for status messages
status_label = tk.Label(window, text="Ready", fg="green", font=("Helvetica", 14))
status_label.pack(pady=10)

# Create a label for displaying the video stream
video_label = tk.Label(window)
video_label.pack()

# Function to process login
def login(username, password):
    if username == "admin" and password == "password":
        status_label.config(text="Login Successful!")
        # Enable face recognition buttons and hide login frame
        train_button.pack()
        video_button.pack()
        login_frame.pack_forget()
        background_label.pack_forget()  # Remove the background image
    else:
        status_label.config(text="Login Failed!")

def encode_faces(frame):
    # Resize the frame to improve face detection speed (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the frame from BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = small_frame[:, :, ::-1]

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame, model='hog')

    # Encode the faces in the frame
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    return face_locations, face_encodings

def train_faces():
    global data  # Add global declaration

    status_label.config(text="Processing... Training faces. It may take 2-3 minutes")
    window.update_idletasks()  # Update the GUI immediately
    path = filedialog.askdirectory()
    if path:
        known_encodings = []
        known_names = []
        count = 0

        for folder in os.listdir(path):
            image_folder = os.path.join(path, folder)
            count += 1
            for file in os.listdir(image_folder):
                full_file_path = os.path.join(image_folder, file)
                image = cv2.imread(full_file_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                boxes = face_recognition.face_locations(gray)
                encodings = face_recognition.face_encodings(image, boxes)

                for encoding in encodings:
                    known_encodings.append(encoding)
                    known_names.append(folder)

        # Create a data dictionary to store encodings and names
        data = {"encodings": known_encodings, "names": known_names}

        # Save the data to a pickle file
        with open("encodings.pickle", "wb") as f:
            pickle.dump(data, f)

        status_label.config(text="Training completed. {} faces trained".format(count))
    else:
        status_label.config(text="Training canceled")

def toggle_video_capture():
    if video_button.config('text')[-1] == 'Start Video Capture':
        start_video_capture()
    else:
        stop_video_capture()

def start_video_capture():
    global video_capture
    video_capture = cv2.VideoCapture(0)
    status_label.config(text="Video Capture Started!")
    video_button.config(text='Stop Video Capture')
    process_frames()

def stop_video_capture():
    global video_capture
    video_capture.release()
    status_label.config(text="Video Capture Stopped!")
    video_button.config(text='Start Video Capture')

def process_frames():
    ret, frame = video_capture.read()

    global frame_count
    frame_count += 1

    if frame_count % skip_frames != 0:
        window.after(10, process_frames)
        return

    # Encode faces in a batch
    face_locations_batch, face_encodings_batch = encode_faces(frame)

    face_names_batch = []

    for face_encoding in face_encodings_batch:
        # Compare face encodings with known encodings
        matches = face_recognition.compare_faces(data["encodings"], face_encoding, tolerance=0.6)

        face_distances = face_recognition.face_distance(data["encodings"], face_encoding)

        # Find the closest match (minimum distance)
        min_distance = min(face_distances)

        # Check if the closest match is below the threshold
        if min_distance <= threshold:
            name = data["names"][np.argmin(face_distances)]
        else:
            name = "Unknown"

        # Add the recognized name to the list of face names
        face_names_batch.append(name)

    # Display the recognized faces
    for (top, right, bottom, left), face_names in zip(face_locations_batch, face_names_batch):
        # Scale the coordinates back to the original frame size
        top = top * 4
        right = right * 4
        bottom = bottom * 4
        left = left * 4

        # Set the color of the bounding box based on face recognition result
        color = (0, 255, 0) if face_names != "Unknown" else (0, 0, 255)

        # Draw rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Display name on screen
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    # Convert the frame to RGB for displaying in Tkinter window
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(image=img)

    # Update the video frame in the GUI
    video_label.config(image=img_tk)
    video_label.image = img_tk

    # Continue processing frames
    window.after(10, process_frames)

# Adjusted button size and placement
button_width = 25
button_height = 3

# Hide face recognition buttons initially
train_button = tk.Button(window, text="Train Faces", command=train_faces, bg="#0078D7", fg="white",
                         width=button_width, height=button_height)
video_button = tk.Button(window, text="Start Video Capture", command=toggle_video_capture, bg="#0078D7", fg="white",
                         width=button_width, height=button_height)

# Pack the login frame
login_frame.pack(pady=50)

# Start the Tkinter event loop
window.mainloop()
