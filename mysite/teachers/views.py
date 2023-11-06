from django.shortcuts import render, redirect
from django.db.models import Max, Subquery, OuterRef
from django.urls import reverse
from .forms import MyClassForm
from .models import MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade, Alert
from users.models import Account
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.

def search(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        quizzes = Quiz.objects.filter(title__contains = subject)
        classes = (MyClass.objects.filter(class_name__contains=subject) | 
        MyClass.objects.filter(class_descriptor__contains=subject))
        discussions = Discussion.objects.filter(subject__contains = subject)
    context = {'subject':subject, 'quizzes':quizzes, 'classes':classes, 'discussions':discussions}
    return render(request, "teachers/search.html", context)

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
    users = Account.objects.filter(is_teacher=False).exclude(
    user__in=EnrolledUser.objects.filter(course=my_class).values('user')
    )
    context = {'courseId': course_id, 'users': users, 'my_class': my_class}
    return render(request, "teachers/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('teachers:home')
    
def discussion(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    messages = Discussion.objects.filter(course=my_class).order_by('-created_at')
    enrolled_users = EnrolledUser.objects.filter(course=my_class)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('upload')
        post = Discussion.objects.create(
            course=my_class, 
            author=request.user, 
            subject=subject, 
            message=message,
            file=uploaded_file 
        )
        for user in enrolled_users:
            Alert.objects.create(
                course=my_class,
                student=user.user,
                post= post
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
    attempts = Grade.objects.filter(quiz=quiz)
    subquery = Grade.objects.filter(
    student=OuterRef('student'),
    quiz=quiz
    ).order_by('-grade').values('grade')[:1]

    grades = Grade.objects.filter(
    quiz=quiz,
    grade=Subquery(subquery)
    )
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

def attempts(request, id, course_id, student_id):
    quiz = Quiz.objects.get(pk=id)
    student = User.objects.get(pk=student_id)
    grades = Grade.objects.filter(quiz=quiz, student=student)
    context = {"grades":grades, "quiz":quiz, "courseId":course_id}
    return render(request, "teachers/attempts.html", context)

def deleteQuiz(requqest, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return redirect(reverse('teachers:quizHub', args=[course_id]))

def settings(request, url):
    context = {"url":url}
    return render(request, "teachers/settings.html", context)

def changeUsername(request, url):
    if request.method == 'POST':
        new_username = request.POST['new_username']
        user = User.objects.get(username=request.user.username)
        try:
            user.username = new_username
            user.save()
            messages.success(request, 'Username changed successfully.')
        except Exception as e:
            messages.error(request, "This Username is already In use")
            
        return redirect(reverse('teachers:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page

def changePassword(request, url):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logging the user out
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Could Not change password, Please Check length')
            return redirect(reverse('teachers:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page