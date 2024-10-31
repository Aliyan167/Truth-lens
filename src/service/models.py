from django.db import models
from tinymce.models import HTMLField
from src. website.models import Technology, Skill


# Create your models here.

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = HTMLField(blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, related_name='services',
                                 on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='service_thumbnails/', blank=True, null=True)
    icon = models.ImageField(upload_to='service_thumbnails/icons/', blank=True, null=True, help_text="A small icon: avaiable at FontAwesome")
    is_active = models.BooleanField(default=True)
    skills = models.ManyToManyField(Skill, related_name='services', blank=True)
    technologies = models.ManyToManyField(Technology, related_name='services',
                                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


