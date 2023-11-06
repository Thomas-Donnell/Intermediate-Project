from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse
from teachers.forms import MyClassForm
from teachers.models import MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade, Alert
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
def home(request):
    classes = []
    form = MyClassForm()

    if request.method == 'POST':
        form = MyClassForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
    enrolled_courses = EnrolledUser.objects.filter(user=request.user)
    for course in enrolled_courses:
        classes.append(course.course)
    context = {'form':form, 'classes': classes}
    return render(request, "students/home.html", context)

def course(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    alerts = Alert.objects.filter(student=request.user, course=my_class).count()
    if request.method == 'POST':
        enrolled_user_ids = request.POST.getlist('enrolled_users')  # Get a list of selected user IDs
        enrolled_users = User.objects.filter(id__in=enrolled_user_ids)
        for user in enrolled_users:
            EnrolledUser.objects.create(user=user, course=my_class)
    users = User.objects.all()
    context = {'courseId': course_id, 'users': users, 'my_class': my_class, 'alerts':alerts}
    return render(request, "students/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('students:home')
    
def discussion(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    messages = Discussion.objects.filter(course=my_class).order_by('-created_at')
    enrolled_users = EnrolledUser.objects.filter(course=my_class)
    alerts = Alert.objects.filter(student=request.user, course=my_class)
    alerts.delete()
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
        return redirect(reverse('students:discussion', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'messages': messages}
    return render(request, "students/discussion.html", context)

def post(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    fileName = post.file.name.split("/")[-1]
    replies = Reply.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        message = request.POST.get('message')
        Reply.objects.create(post=post, author=request.user, message=message)
        return redirect(reverse('students:post', args=[id, course_id]))
    context = {'post':post, 'replies':replies, 'courseId':course_id, 'fileName':fileName}
    return render(request, "students/post.html", context)


def deletePost(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    post.delete()
    return redirect(reverse('students:discussion', args=[course_id]))

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
        return redirect(reverse('students:quizHub', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'quizes': quizes}
    return render(request, "students/quizhub.html", context)

def quiz(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    context = {"quiz":quiz, "courseId":course_id}
    return render(request, "students/quiz.html", context)

def quizView(request, id, course_id):
    #Get quiz, questions, and grade model objects
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)
    attempt = 0 
    try:
        grades = Grade.objects.filter(quiz=quiz, student=request.user)
        attempt = len(grades)
        # Annotate the query with the maximum grade
        grades = grades.annotate(max_grade=Max('grade'))
        # Order the results in descending order by the maximum grade
        highest_grade = grades.order_by('-max_grade').first()
    except ObjectDoesNotExist:
        grades = None
    
    if request.method == 'POST':
        total_questions = len(questions)
        correct = 0
        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            if selected_answer == question.correct_answer:
                correct += 1
        total = correct/total_questions * 100
        Grade.objects.create(
            grade = total,
            quiz=quiz, 
            student=request.user,
            attempt = attempt + 1
        )
        return redirect(reverse('students:quizView', args=[id, course_id]))
    
    context = {"questions":questions, "quiz":quiz, "courseId":course_id, "attempt":attempt, "grade":highest_grade}
    return render(request, "students/quizview.html", context)

def settings(request, url):
    context = {"url":url}
    return render(request, "students/settings.html", context)

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
            
        return redirect(reverse('students:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page

def changePassword(request, url):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logging the user out
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Could Not change password, Please Check length')
            return redirect(reverse('students:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page
