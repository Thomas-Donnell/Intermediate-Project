from django.urls import path

from . import views

app_name = 'students'  # Set the app namespace
urlpatterns = [
    path("", views.home, name="home"),
]