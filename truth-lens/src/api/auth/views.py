from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView

from src.ml_model import detect_adapter
from src.ml_model.detect import predict_image
from src.api.auth.serializer import ImageUploadSerializer, ImageResultSerializer
from root.settings import GOOGLE_CALLBACK_ADDRESS, APPLE_CALLBACK_ADDRESS
from src.api.auth.serializer import PasswordSerializer, UserSerializer
from src.web.website.models import ImageUpload
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
import os
import tempfile
import time
from src.ml_model.utils import has_face
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_ADDRESS
    client_class = OAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_ADDRESS
    client_class = OAuth2Client


class CustomGoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer.instance.user

        return Response({
            "token": response.data.get("key"),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    callback_url = APPLE_CALLBACK_ADDRESS
    client_class = OAuth2Client


class AppleConnect(SocialConnectView):
    adapter_class = AppleOAuth2Adapter
    callback_url = APPLE_CALLBACK_ADDRESS
    client_class = OAuth2Client


class CustomLoginView(LoginView):
    serializer_class = LoginSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if request.user.is_authenticated:
            user = request.user
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            response.data['key'] = new_token.key
        return response


class UserRetrieveChangeAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class DeactivateUserAPIView(APIView):
    """ Deactivate user account """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        user = request.user

        # Validate the password
        user = authenticate(email=user.email, password=password)
        if user is None:
            return Response(
                data={'error': 'Enter a Valid Password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deactivate the user account
        user.is_active = False
        user.save()

        return Response(
            data={'message': 'User account has been deactivated'},
            status=status.HTTP_200_OK
        )


class DeleteUserAPIView(APIView):
    """ Delete user account """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        user = request.user

        # Validate the password
        user = authenticate(email=user.email, password=password)
        if user is None:
            return Response(
                data={'error': 'Enter a Valid Password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()

        return Response(
            data={'message': 'User account has been deactivated'},
            status=status.HTTP_200_OK
        )


class ImagePredictionAPIView(APIView):
    """
    Accepts an image upload, checks if a face is present,
    runs ML prediction if valid, saves the result in DB,
    and returns JSON response.
    """
    serializer_class = ImageUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['image']

        try:
            # ✅ Step 1: Face detection
            if not has_face(image):
                return Response(
                    {"error": "No face detected in the uploaded image."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Step 2: Temporarily save image for model processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # ✅ Step 3: Run AI prediction
            start_time = time.time()
            label, score = predict_image(temp_file_path)
            end_time = time.time()
            processing_time = round(end_time - start_time, 3)

            # Clean up temp file
            os.remove(temp_file_path)

            # ✅ Step 4: Save prediction to DB
            upload_instance = ImageUpload.objects.create(
                image=image,
                prediction=label.lower(),
                score=score,
            )

            # ✅ Step 5: Return JSON response
            return Response({
                "id": upload_instance.id,
                "image_url": upload_instance.image.url if upload_instance.image else None,
                "prediction": upload_instance.prediction,
                "score": upload_instance.score,
                "time_taken": processing_time,
                "uploaded_at": upload_instance.uploaded_at,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from src.api.auth.serializer import UserSerializer


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from src.web.website.models import ImageUpload


class ScannedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all saved data
        results = ImageUpload.objects.all()
        serializer = ImageResultSerializer(results, many=True)
        return Response({
            "total_results": results.count(),
            "results": serializer.data
        })


# video_detection/views.py

import cv2
import os
import numpy as np
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status
from src.web.website.models import VideoUpload
from src.ml_model.detect_adapter import classify_video_segment
from src.api.auth.serializer import VideoUploadSerializer
from src.ml_model.video_processing import process_video

# Optional: force CPU if MKL/GPU issues
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class VideoPredictionAPIView(APIView):
    """
    Upload a video, detect face, predict real/fake using your model,
    save video and prediction in DB, return JSON response.
    """
    serializer_class = VideoUploadSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_file = serializer.validated_data['video']

        try:
            # Step 1: Save video temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_video_path = temp_file.name

            # Step 2: Open video and collect frames
            cap = cv2.VideoCapture(temp_video_path)
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            frames_for_prediction = []
            face_detected = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert to gray for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)

                if len(faces) > 0:
                    face_detected = True

                # Collect first 8 frames for model
                if len(frames_for_prediction) < 8:
                    frames_for_prediction.append(frame)

            cap.release()

            # Step 2b: ensure exactly 8 frames
            if len(frames_for_prediction) == 0:
                os.remove(temp_video_path)
                return Response({"error": "Could not read frames from video."}, status=status.HTTP_400_BAD_REQUEST)

            while len(frames_for_prediction) < 8:
                frames_for_prediction.append(frames_for_prediction[-1])

            # Step 3: Run model
            start_time = time.time()
            label, score = detect_adapter.classify_video_segment(frames_for_prediction)
            end_time = time.time()
            processing_time = round(end_time - start_time, 3)

            # Step 4: Save video + prediction
            upload_instance = VideoUpload.objects.create(
                user=None,
                video=video_file,
                prediction=label.lower(),
                score=score,
            )

            # Step 5: Clean up temp file
            os.remove(temp_video_path)

            # Step 6: Return JSON response
            return Response({
                "id": upload_instance.id,
                "video_url": upload_instance.video.url,
                "face_detected": face_detected,
                "prediction": upload_instance.prediction,
                "score": upload_instance.score,
                "time_taken": processing_time,
                "created_at": upload_instance.created_at,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
