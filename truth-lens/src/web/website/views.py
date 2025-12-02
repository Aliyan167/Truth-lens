from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import ImageUpload
from django.shortcuts import render
from .forms import VideoUploadForm
from ...ml_model import detect_adapter
import cv2

from ...ml_model.detect import predict_image
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from src.apps.whisper.main import NotificationService
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files import File
from django.urls import reverse
from .forms import VideoUploadForm
from .models import VideoUpload
from ...ml_model.video_processing import process_video
import cv2
from django.shortcuts import render
from .forms import VideoUploadForm
from .models import VideoUpload
from src.ml_model import detect_adapter
import cv2

User = get_user_model()


def upload_image(request):
    image_obj = None
    prediction_score = None
    form = ImageForm()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_obj = form.save()

            # ML prediction → now returns (label, score)
            label, score = predict_image(image_obj.image.path)
            normalized_prediction = str(label).lower().strip()

            if normalized_prediction in ['real', 'fake']:
                image_obj.prediction = normalized_prediction
                image_obj.save()
                prediction_score = score  # pass to template

                # Send email
                user = request.user
                if user.email:
                    subject = "Your Image Has Been Processed"
                    message = f"""
Hi {user.username},

✅ Your image has been successfully processed.

🧠 Result: {normalized_prediction.upper()}
📊 Confidence Score: {score:.4f}

Thank you for using our service!
"""
                    try:
                        NotificationService.send_email(
                            to_email=user.email,
                            subject=subject.strip(),
                            message=message.strip()
                        )
                    except Exception as e:
                        print(f"❌ Failed to send email: {e}")

    return render(request, 'website/feature.html', {
        'form': form,
        'image': image_obj,
        'score': prediction_score,  # 🔥 pass score to template
    })


def home(request):
    return render(request, 'website/home.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('website:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('website:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('website:signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Authenticate again with email and password
        authenticated_user = authenticate(request, email=email, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)  # safe because backend is set
            return redirect('website:home')
        else:
            messages.error(request, "There was a problem logging you in after signup.")
            return redirect('website:home')

    return render(request, 'website/home.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # ✅ using email instead of username
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # ✅ match USERNAME_FIELD
        if user:
            login(request, user)
            return redirect('website:home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('website:home')

    return render(request, 'website/home.html')


def logout_view(request):
    logout(request)
    return redirect("website:home")


def home(request):
    return render(request, "website/home.html")


def upload_video_view(request):
    video_instance = None
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()

            cap = cv2.VideoCapture(instance.video.path)
            frames = []
            # face_detected = False   # ❌ commented out

            while len(frames) < 8:
                ret, frame = cap.read()
                if not ret:
                    break

                # --- Face detection check (commented out) ---
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                # if len(faces) > 0:
                #     face_detected = True

                frames.append(frame)

            cap.release()

            # if not face_detected:
            #     instance.prediction = "No clear face detected in video"
            #     instance.save()
            if len(frames) == 8:
                label, score = detect_adapter.classify_video_segment(frames)
                instance.prediction = f"{label.title()} ({score * 100:.1f}%)"
                instance.save()
            else:
                instance.prediction = "Could not extract enough frames"
                instance.save()

            video_instance = instance
    else:
        form = VideoUploadForm()

    return render(request, "website/upload_video.html", {"form": form, "video": video_instance})


def about(request):
    return render(request, 'website/about.html')


def contact(request):
    return render(request, 'website/contact.html')
