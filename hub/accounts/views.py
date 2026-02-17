from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomLogin, CustomSignUp


def login_view(request):
    if request.method == 'POST':
        form= CustomLogin(request.POST)
        if form.is_valid():
            user= form.get_user
            login(request, user)
            return redirect('index')
    else:
        form= CustomLogin()
        context= {'form':form}
    return render(request, 'accounts/login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form= CustomSignUp(request.POST)
        if form.is_valid:
            user= form.save()
            login(request, user)
            return redirect('index')
    form= CustomSignUp()
    context= {'form':form}
    return render(request, 'accounts/signup.html', context)