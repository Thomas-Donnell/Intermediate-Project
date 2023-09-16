from django.urls import path

from . import views
app_name = 'teachers'
urlpatterns = [
    path("", views.home, name="home"),
]