from django.db import models
from src. website.models import Technology
from tinymce.models import HTMLField


# Create your models here.

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster_image = models.ImageField(upload_to='project_posters/', blank=True, null=True, help_text="Larger for detail View")
    thumbnail_image = models.ImageField(upload_to='project_thumbnails/', blank=True, null=True)
    content = HTMLField(blank=True, null=True)

    category = models.ForeignKey(ProjectCategory, related_name='projects', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    client = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.title




class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, related_name='technologies', on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, related_name='project_technologies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.title} - {self.technology.name}"