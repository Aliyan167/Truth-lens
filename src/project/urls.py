from django.urls import path
from . views import (
    IndexView, ProjectDetailView
)

app_name = "project"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("detail/<int:pk>/", ProjectDetailView.as_view(), name="detail")
]