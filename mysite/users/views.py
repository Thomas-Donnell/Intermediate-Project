from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Account
# Create your views here.
from .forms import CreateUserForm, AccountForm


def register(request):
    form = CreateUserForm()
    account_form = AccountForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        account_form = AccountForm(request.POST)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            return redirect('users:loginPage')

    context = {'form':form, 'account_form':account_form}
    return render(request, "users/registration.html", context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            account = Account.objects.get(user=user)
            is_teacher = account.is_teacher
            login(request, user)
            if is_teacher:
                return redirect('teachers:home')
            else:
                return redirect('students:home')
    context = {}
    return render(request, "users/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('users:loginPage') 

