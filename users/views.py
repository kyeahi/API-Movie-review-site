<<<<<<< HEAD
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
=======
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages


def base(request):
    return render(request, 'layout/base.html')

def signup(request):
    if request.method == "GET":
        signupForm = UserCreationForm(request.GET)
        return render(request, 'users/signup.html', {'signupForm': signupForm})
>>>>>>> origin/ksm
    elif request.method == "POST":
        signupForm = UserCreationForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
<<<<<<< HEAD
            return redirect('/users/signup')
=======
            return redirect('/base')
>>>>>>> origin/ksm

def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
<<<<<<< HEAD
        return render(request, 'users/login.html',
                {'loginForm':loginForm})
=======
        return render(request, 'users/login.html', {'loginForm':loginForm})
>>>>>>> origin/ksm
    elif request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
<<<<<<< HEAD
            return redirect('/board/list')
=======
            return redirect('/base')
>>>>>>> origin/ksm
        else:
            return redirect('/users/login')

def userlogout(request):
    logout(request)
<<<<<<< HEAD
    return redirect('/users/login')


def change_password(request):
    return render(request, 'users/change_password.html')
=======
    return redirect('/base')

def pchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '패스워드 변경 완료!')
            return redirect('/base')
        else:
            messages.error(request, 'base.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/pchange.html', {
        'form': form
    })

def userDelete(request):
    user = request.user
    user.delete()
    logout(request)
    return render(request, 'layout/base.html')
>>>>>>> origin/ksm
