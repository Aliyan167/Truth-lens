from django.urls import path, include

urlpatterns = [
    path('', include('src.website.urls')),
    path('projects/', include('src.project.urls')),
    path('services/', include('src.service.urls')),
    path('team/', include('src.team.urls')),
]
