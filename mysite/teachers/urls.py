from django.urls import path

from . import views
app_name = 'teachers'
urlpatterns = [
    path("", views.home, name="home"),
    path("course/<str:course_id>/", views.course, name="course"),
    path("delete_course/<str:course_id>/", views.deleteCourse, name="deleteCourse"),
    path("discussions/<str:course_id>/", views.discussion, name="discussion"),
    path("post/<str:id>/<str:course_id>/", views.post, name="post"),
    path("delete_post/<str:id>/<str:course_id>/", views.deletePost, name="deletePost"),
]