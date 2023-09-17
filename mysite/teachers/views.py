from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MyClassForm
from .models import MyClass
# Create your views here.
def home(request):
    form = MyClassForm()

    if request.method == 'POST':
        form = MyClassForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
    classes = MyClass.objects.filter(teacher=request.user)
    context = {'form':form, 'classes': classes}
    return render(request, "teachers/home.html", context)

def course(request, course_id):
    context = {'courseId': course_id}
    return render(request, "teachers/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('teachers:home')
    