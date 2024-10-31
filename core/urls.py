from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from core.settings import MEDIA_ROOT, STATIC_ROOT


urlpatterns = [
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('src.website.urls')),
]


""" STATIC AND MEDIA FILES ----------------------------------------------------------------------------------------- """
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]