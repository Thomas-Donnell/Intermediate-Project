from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MyClassForm, EnrollForm
from .models import MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade
from django.contrib.auth.models import User
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
    my_class = MyClass.objects.get(id=course_id)
    if request.method == 'POST':
        enrolled_user_ids = request.POST.getlist('enrolled_users')  # Get a list of selected user IDs
        enrolled_users = User.objects.filter(id__in=enrolled_user_ids)
        for user in enrolled_users:
            EnrolledUser.objects.create(user=user, course=my_class)
    users = User.objects.all()
    context = {'courseId': course_id, 'users': users, 'my_class': my_class}
    return render(request, "teachers/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('teachers:home')
    
def discussion(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    messages = Discussion.objects.filter(course=my_class).order_by('-created_at')
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('upload')
        Discussion.objects.create(
            course=my_class, 
            author=request.user, 
            subject=subject, 
            message=message,
            file=uploaded_file 
        )
        return redirect(reverse('teachers:discussion', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'messages': messages}
    return render(request, "teachers/discussion.html", context)

def post(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    fileName = ""
    if(post.file):
        fileName = post.file.name.split("/")[-1]
    replies = Reply.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        message = request.POST.get('message')
        Reply.objects.create(post=post, author=request.user, message=message)
        return redirect(reverse('teachers:post', args=[id, course_id]))
    context = {'post':post, 'replies':replies, 'courseId':course_id, 'fileName':fileName}
    return render(request, "teachers/post.html", context)


def deletePost(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    post.delete()
    return redirect(reverse('teachers:discussion', args=[course_id]))

def quizHub(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    quizes = Quiz.objects.filter(course=my_class).order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(
            title = title,
            course=my_class, 
            author=request.user
        )
        return redirect(reverse('teachers:quizHub', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'quizes': quizes}
    return render(request, "teachers/quizhub.html", context)

def quiz(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    grades = Grade.objects.filter(quiz=quiz)
    context = {"quiz":quiz, "courseId":course_id, "grades":grades}
    return render(request, "teachers/quiz.html", context)

def quizView(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')
        Question.objects.create(
            quiz = quiz,
            question_text=question, 
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer= correct_answer
        )
        return redirect(reverse('teachers:quizView', args=[id, course_id]))
    context = {"questions":questions, "quiz":quiz, "courseId":course_id}
    return render(request, "teachers/quizview.html", context)

def deleteQuiz(requßest, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return redirect(reverse('teachers:quizHub', args=[course_id]))