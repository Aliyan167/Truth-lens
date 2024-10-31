from django.db import models

# Create your models here.

class Rank(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CEO(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')
    phonenumber = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Check if a CEO instance already exists
        if CEO.objects.exists() and not self.pk:
            # If one exists and we're trying to create another, update the existing one
            existing_ceo = CEO.objects.first()
            existing_ceo.name = self.name
            existing_ceo.description = self.description
            existing_ceo.image = self.image
            existing_ceo.phonenumber = self.phonenumber
            existing_ceo.email = self.email
            existing_ceo.location = self.location
            existing_ceo.save()
        else:
            # Save normally if this is the first instance or an update to the current instance
            super(CEO, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "CEO"
        verbose_name_plural = "CEO"



