# utils.py or detect.py
import cv2
import numpy as np


def has_face(image_file) -> bool:
    """
    Checks if the uploaded image has at least one detectable face.
    image_file: Django InMemoryUploadedFile
    Returns True if face detected, False otherwise
    """
    # Convert InMemoryUploadedFile to numpy array
    img_array = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Reset file pointer after reading
    image_file.seek(0)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load Haar cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    return len(faces) > 0


import cv2
import os

# Load OpenCV face detector
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(CASCADE_PATH)


def frame_has_face(frame):
    """Return True if at least one face is detected."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.2, 5)
    return len(faces) > 0
