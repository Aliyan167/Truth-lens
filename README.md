Truth-Lens – AI-Powered Media Authenticity Verification

Truth-Lens is an AI-powered platform for web and mobile that detects whether an image or video is real or fake.
Using advanced deep-learning models, the system identifies deepfakes, manipulated media, and synthetic content—helping users verify authenticity quickly and reliably.

🚀 Features

🔍 Real vs Fake Detection for images and videos

🤖 Deep Learning Models trained for media forensics

🧠 Analysis of faces, textures, motion artifacts, and noise patterns

📱 Web & Mobile App Support

⚡ Fast Predictions with confidence scores

🎥 Support for video frame extraction and analysis

🔐 Secure Upload Handling

📡 REST API for external integrations

💾 History & Result Logs (if implemented in your version)

🧰 Tech Stack
Backend / AI

Python

Django / Flask (depending on your backend)

TensorFlow / PyTorch deepfake detection models

OpenCV for video and image processing

Frontend

HTML, CSS, JavaScript

(Optional) React / Next.js

Mobile App (React Native / Flutter if used)

Database

PostgreSQL / MySQL / SQLite

📸 How It Works

User uploads an image or video

The system preprocesses the media

AI model runs authenticity analysis

The platform returns:

Real / Fake prediction

Confidence score

Optional: heatmaps / face detection info

Results displayed instantly on the dashboard

📦 Installation (Backend)
git clone https://github.com/<your-username>/Truth-lens.git
cd Truth-lens
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
