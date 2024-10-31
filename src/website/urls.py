from django.urls import path

from . views import IndexView, ContactView, AboutView

app_name = "website"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact-us/", ContactView.as_view(), name="contact-us"),
    path("about-us", AboutView.as_view(), name="about-us"),
]
