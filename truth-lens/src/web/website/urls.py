from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path('', views.home, name='home'),
    path('detection/', views.upload_image, name='ho'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("upload/", views.upload_video_view, name="upload_video"),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
]
