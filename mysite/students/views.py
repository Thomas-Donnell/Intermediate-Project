from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from teachers.forms import MyClassForm, EnrollForm
from teachers.models import MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade
from django.contrib.auth.models import User
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
    if request.method == 'POST':
        enrolled_user_ids = request.POST.getlist('enrolled_users')  # Get a list of selected user IDs
        enrolled_users = User.objects.filter(id__in=enrolled_user_ids)
        for user in enrolled_users:
            EnrolledUser.objects.create(user=user, course=my_class)
    users = User.objects.all()
    context = {'courseId': course_id, 'users': users, 'my_class': my_class}
    return render(request, "students/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('students:home')
    
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
    try:
        grade = Grade.objects.get(quiz=quiz, student=request.user)
    except ObjectDoesNotExist:
        grade = None
    
    if request.method == 'POST':
        total_questions = len(questions)
        correct = 0
        for question in questions:
            selected_answer = int(request.POST.get(f'question_{question.id}'))
            if selected_answer == question.correct_answer:
                correct += 1
        total = correct/total_questions * 100
        Grade.objects.create(
            grade = total,
            quiz=quiz, 
            student=request.user
        )
        return redirect(reverse('students:quizView', args=[id, course_id]))
    
    context = {"questions":questions, "quiz":quiz, "courseId":course_id, "grade":grade}
    return render(request, "students/quizview.html", context)
