from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

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
    context = {'form':form, 'account_form':account_form}
    return render(request, "users/registration.html", context)

def login(request):
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
    context = {'form':form, 'account_form':account_form}
    return render(request, "users/login.html", context)
