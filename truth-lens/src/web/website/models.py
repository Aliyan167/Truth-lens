from django.db import models
from django.conf import settings


class ImageUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(
        max_length=10,
        choices=[('real', 'Real'), ('fake', 'Fake')],
        blank=True,
        null=True
    )
    score = models.FloatField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}- {self.prediction}"


class VideoUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to='videos/')
    prediction = models.CharField(
        max_length=10,
        choices=[('real', 'Real'), ('fake', 'Fake')],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"VideoUpload({self.pk})"
