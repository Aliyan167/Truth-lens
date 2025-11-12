import os
import tensorflow as tf
from keras.preprocessing import image as keras_image
import numpy as np

# ───────────────────────────────────────────────────────────
# 1) Load model once
# ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml_model', 'best_model.h5')

# Load the trained model
model = tf.keras.models.load_model(MODEL_PATH)
input_shape = model.input_shape[1:4]  # e.g., (160, 160, 3)
IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS = input_shape

# ───────────────────────────────────────────────────────────
# 2) Predict function
# ───────────────────────────────────────────────────────────
def predict_image(img_path: str):
    try:
        img = keras_image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = keras_image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array, verbose=0)
        score = float(prediction[0][0])

        # Label: 0 = real, 1 = fake
        label = "Fake" if score < 0.53539 else "Real"

        return label, score
    except Exception as e:
        print(f"[ERROR] Failed to predict image {img_path}: {str(e)}")
        return "Error", 0.0


