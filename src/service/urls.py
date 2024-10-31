from django.urls import path
from . views import (
    IndexView, ServiceDetailView
)

app_name = "service"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("detail/<int:pk>/", ServiceDetailView.as_view(), name="detail")
]