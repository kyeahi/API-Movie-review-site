from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
def watcha(request):
    return render(request, 'layout/watcha.html')



def signup(request):
    if request.method == "GET":
        signupForm = UserCreationForm()
        return render(request, 'users/signup.html',
                      {'signupForm':signupForm})
    elif request.method == "POST":
        signupForm = UserCreationForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('/users/signup')

def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
        return render(request, 'users/login.html',
                {'loginForm':loginForm})
    elif request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/board/list')
        else:
            return redirect('/users/login')

def userlogout(request):
    logout(request)
    return redirect('/users/login')


def change_password(request):
    return render(request, 'users/change_password.html')