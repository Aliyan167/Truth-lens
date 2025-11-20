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
from src.ml_model.detect import predict_image
from src.api.auth.serializer import ImageUploadSerializer
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
from rest_framework.permissions import IsAuthenticated
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
        user = self.serializer.instance.user  # Correct way to get the logged-in user

        return Response({
            "token": response.data.get("key"),  # token from dj-rest-auth
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
    # Accept both session and token authentication
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Use PUT instead of POST for updating user
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
