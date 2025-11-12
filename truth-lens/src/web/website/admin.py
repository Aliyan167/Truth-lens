from django.contrib import admin
from .models import ImageUpload
from django.contrib import admin
from .models import VideoUpload

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at', 'prediction')
    readonly_fields = ('uploaded_at',)





@admin.register(VideoUpload)
class VideoUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "video", "prediction", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("id", "user__username")
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("user", "video", "prediction", "created_at")
        }),
    )
