from django import forms
from .models import ImageUpload
import cv2
import numpy as np
import os
from django.core.exceptions import ValidationError
from django import forms
from .models import VideoUpload


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise ValidationError("Only .jpg, .jpeg, .png files are allowed.")

        # Convert InMemoryUploadedFile to numpy array for OpenCV
        img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Use OpenCV's built-in face detector
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            raise ValidationError("face is not clear. Please upload a clear photo with a visible face.")

        # Reset image file pointer for saving
        image.seek(0)
        return image


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_video(self):
        v = self.cleaned_data['video']
        # Validate content type & size
        if v.size > 200 * 1024 * 1024:  # 200MB limit example
            raise forms.ValidationError("File too large (limit 200MB).")
        if not v.content_type.startswith('video/'):
            raise forms.ValidationError("Please upload a video file.")
        return v
