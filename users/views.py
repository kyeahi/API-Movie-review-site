from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json


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
            messages.info(request, '올바르지 않습니다.')
            return redirect('/users/signup')

def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
        return render(request, 'users/login.html', {'loginForm':loginForm})
    elif request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/base')
        else:
            messages.info(request, '올바르지 않습니다.')
            return redirect('/users/login')

def userlogout(request):
    logout(request)
    return redirect('/base')

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
            messages.info(request, '올바르지 않습니다.')
            return redirect('/users/change_password')

@login_required(login_url='/users/login')
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('/base')
    return render(request, 'users/delete.html')

def kakao_api(request):
    return redirect('https://kauth.kakao.com/oauth/authorize?client_id=4c028f208adcf6250df90f94b2cdc5a2&redirect_uri=http://127.0.0.1:8000/oauth&response_type=code')
    # 문자열로 하면 안받아옴 client_id = redierct_uri 이거 둘다 중요한것임.


def kakao_api1(request):
    print(request.GET.get('code'))  # 인가코드 받아오는 애
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  # h를
    data = {"grant_type": 'authorization_code',
            'client_id': '4c028f208adcf6250df90f94b2cdc5a2',
            'redirect_uri': 'http://127.0.0.1:8000/oauth',
            'code': request.GET.get('code')}  # 인가코드

    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)

    token_json = res.json()
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me",
                                   headers={"Authorization": f"Bearer {access_token}"}, )
    profile_json = profile_request.json()

    # kakao_account = profile_json.get("kakao_account")
    # email = kakao_account.get("email", None)

    kakao_id = profile_json.get("id")
    # email = profile_json.get("email", None)
    email = profile_json['kakao_account']['email']
    # kakao_id = profile_json['kakao_account']['id']

    if User.objects.filter(username=kakao_id).exists():
        user = User.objects.get(username=kakao_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/base')
    else:
        User(username=kakao_id, email=email, ).save()
        User.objects.filter(username=kakao_id).exists()
        user = User.objects.get(username=kakao_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/base')