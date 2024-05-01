from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # Import the views for authentication

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
]