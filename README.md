Truth-Lens – AI-Powered Media Authenticity Verification

Truth-Lens is an AI-powered platform for web and mobile that detects whether an image or video is real or fake.
Using advanced deep-learning models, the system identifies deepfakes, manipulated media, and synthetic content—helping users verify authenticity quickly and reliably.

🚀 Features

🔍 Real vs Fake Detection for images and videos

🤖 Deep Learning Models trained for media forensics

🧠 Analysis of faces, textures, motion artifacts, and noise patterns

📱 Web & Mobile App Support

⚡ Fast Predictions with confidence scores

🎥 Video frame extraction and analysis

🔐 Secure upload handling

📡 REST API for integrations

💾 History & results logs (if implemented)

🧰 Tech Stack
Backend / AI

Python

Django 

TensorFlow / PyTorch

OpenCV

Frontend

HTML, CSS, JavaScript



Mobile

 Flutter

Database

 SQLite

📸 How It Works

User uploads an image or video

The system preprocesses the media

The AI model analyzes frames, textures, artifacts, and patterns

The platform returns:

✅ Real / Fake prediction

📊 Confidence score

🔥 Optional: heatmaps or detected faces

Results are displayed instantly on the dashboard

📦 Installation (Backend)
git clone https://github.com/<your-username>/Truth-lens.git
cd Truth-lens

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
