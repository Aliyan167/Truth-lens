import cv2
import numpy as np
import tensorflow as tf
import os
import cv2
import numpy as np
import tensorflow as tf
import os

# Load model once (adjust path)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "deepfake_vedio_detection_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)



def preprocess_frames(frames):
    """Resize & normalize a sequence of frames for the model input."""
    processed = []
    for frame in frames:
        img = cv2.resize(frame, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype("float32") / 255.0
        processed.append(img)
    return np.expand_dims(np.array(processed), axis=0)  # shape (1, 8, 224, 224, 3)


def classify_video_segment(frames):
    """Takes 8 frames and returns label + score."""
    processed = preprocess_frames(frames)
    preds = model.predict(processed, verbose=0)

    score = float(preds[0][0])  # probability value
    label = "fake" if score > 0.5 else "real"

    print(f"[DEBUG] Score: {score:.6f} | Label: {label.title()}")  # for console logs
    return label, score


def detect_frame(frame_bgr: np.ndarray) -> np.ndarray:
    try:
        # Instead of preprocess_frame (wrong input shape), use a dummy segment of 8 copies of the frame
        frames = [frame_bgr] * 8
        processed = preprocess_frames(frames)
        preds = model.predict(processed, verbose=0)

        label = "Fake" if preds[0][0] > 0.5 else "Real"

        annotated = frame_bgr.copy()
        cv2.putText(
            annotated, f"Prediction: {label}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255) if label == "Fake" else (0, 255, 0),
            2,
        )
        return annotated
    except Exception as e:
        print(f"[ERROR] detect_frame failed: {e}")
        return frame_bgr
