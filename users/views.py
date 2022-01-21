from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect


def base(request):
    return render(request, 'layout/base.html')

def signup(request):
    if request.method == "GET":
        signupForm = UserCreationForm(request.GET)
        return render(request, 'users/signup.html', {'signupForm': signupForm})

    elif request.method == "POST":
        signupForm = UserCreationForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('/base')
        else:
            messages.info(request, '아이디와 비밀번호가 일치하지 않습니다.')
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
            return redirect('/base')
        else:
            messages.info(request, '아이디와 비밀번호가 올바르지 않습니다.')
            return redirect('/users/login')

def userlogout(request):
    logout(request)
    return redirect('/users/login')


@login_required(login_url='/users/login')
def change_password(request):
    if request.method == "GET":
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'users/change_password.html',
                {'password_change_form':password_change_form})

    elif request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('/base')
        else:
            messages.info(request, '새 비밀번호가 올바르지 않습니다.')
            return redirect('/users/change_password')

@login_required(login_url='/users/login')
def user_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/base')
    return render(request, 'users/user_delete.html')
