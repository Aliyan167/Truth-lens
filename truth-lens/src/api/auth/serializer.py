from rest_framework import serializers

from src.services.accounts.models import User
from src.web.website.models import ImageUpload


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'pk', 'email', 'username', 'first_name', 'last_name', 'profile_image'
        ]
        read_only_fields = ['pk', 'email']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)


from rest_framework import serializers


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'image', 'prediction', 'score', 'uploaded_at']
        read_only_fields = ['id', 'prediction', 'score', 'uploaded_at']
