from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
import random
import smtplib
import string
from django.db.models import Q
from django.http import request
from email.mime.text import MIMEText

# 이메일 인증
from users.forms import Mail


def getEmail(request):
    global recvEmail
    recvEmail = request.POST.get('mail')
    return render(request, 'users/getEmail.html')

def sendEmail(request):
    global pw, recvEmail
    pw = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])  # 소문자 10개 랜덤생성
    recvEmail = request.POST.get('mail')
    sendEmail = "kyeeah9@gmail.com"


    password = "dPqlsdl55!"
    smtpName = "smtp.gmail.com"  # smtp 서버 주소
    smtpPort = 587  # smtp 포트 번호

    text = '인증번호 : ' + pw
    msg = MIMEText(text)  # MIMEText(text , _charset = "utf8")

    msg['Subject'] = '이메일 인증'
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print(msg.as_string())

    s = smtplib.SMTP(smtpName, smtpPort)  # 메일 서버 연결
    s.starttls()  # TLS 보안 처리
    s.login(sendEmail, password)  # 로그인
    s.sendmail(sendEmail, recvEmail, msg.as_string())  # 메일 전송, 문자열로 변환하여 보냅니다.
    s.close()  # smtp 서버 연결을 종료합니다.

    return redirect('/users/match')

# 번호가 맞으면 회원가입창으로 넘겨주기
def match(request):
    if request.method == 'GET':
        form = Mail()
        return render(request,'users/send_email.html',{'form': form})

    elif request.method == 'POST':
        if pw == request.POST.get('token'): # 입력값이 같으면
            mail = User.objects.post(Q(email=recvEmail))
            mail.save(mail.email)
            return redirect('/users/signup')

        elif pw != request.POST.get('token'):  # 입력값이 다르면
            print('다시입력하시오')
            return redirect('/users/send_email')

def base(request):
    return render(request, 'layout/base.html')

def signup(request):
    if request.method == "GET":
        signupForm = UserCreationForm(request.GET)
        # global recvEmail
        # print(recvEmail)
        # mail = User.objects.get(Q(email=recvEmail))
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