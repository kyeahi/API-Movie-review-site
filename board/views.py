import string

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from board.forms import BoardForm
from board.models import Board
from comment.models import Comment
from comment.forms import CommentForm
from django.core.mail import EmailMessage
import requests
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from email.message import EmailMessage
import base64
import smtplib
from email.mime.text import MIMEText
import random


#
# # 공공데이터 api / 인증키 수정해야함
# def request_api(request):
#     res=requests.get('http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=hztiKuQHWROYlgyETY%2FfahobNtI8DSrh2EKGXDyOAdqW0xsxsj8eYKyDBr2EYzAEuZv7u8wW3sg2rDzbATFvIQ%3D%3D&numOfRows=10&pageNo=1&dataType=json&base_date=20220124&base_time=0600&nx=58&ny=125%27)
#     print(str(res.status_code))
#     result = json.loads(res.text)
#     print(result['response']['body']['items']['item'][0]['obsrValue'])
#     return render(request, 'users/text.html')
#
# 카카오 인가코드 / 인증키 수정해야함
# def request_api2(request):
#     return redirect('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=7ada8e5a1760a314ddb4e3d101ce930c&redirect_uri=http://127.0.0.1:8000/oauth%27)
#
# def request_api3(request):
#     print(request.GET.get('code'))
#
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     data = {'grant_type':'authorization_code',
#             'client_id':'7ada8e5a1760a314ddb4e3d101ce930c',
#             'redirect_uri':'http://127.0.0.1:8000/oauth',
#             'code':request.GET.get('code')}
#     res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
#     print(res.text)
#
#     return redirect('/')


def request_api4(request):
    return redirect(
        'https://accounts.google.com/o/oauth2/auth?client_id=777210514810-nu0e94sr27f7bh7liqreor1ul654ne3l.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/test2&scope=https://mail.google.com/&response_type=code&access_type=offline')


# def request_api5(request):
#     email = EmailMessage(
#         'Hello',                # 제목
#         'Body goes here',       # 내용
#         'from@example.com',     # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
#         to=['to1@example.com', 'to2@example.com'],)  # 받는 이메일 리스트
#     email.send()




def gmail_authenticate():
    SCOPES = ['https://mail.google.com/']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)


# 이메일 인증
def sendEmail(request):

    # 랜덤 숫자 생성
    pw = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])  # 소문자 10개

    sendEmail = "kyeeah9@gmail.com"
    recvEmail = "{kyb11220@gmail.com}"
    password = "dPqlsdl55!"

    smtpName = "smtp.gmail.com"  # smtp 서버 주소
    smtpPort = 587  # smtp 포트 번호

    text = pw
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





    return render(request, 'send_email.html')




# 게시글 등록 함수
@login_required(login_url='/users/login')
def register(request):
    if request.method == "GET":
        boardForm = BoardForm()
        return render(request, 'board/register.html', {'boardForm': boardForm})
    elif request.method == "POST":
        boardForm = BoardForm(request.POST)
        if boardForm.is_valid():
            board = boardForm.save(commit=False)
            board.writer = request.user
            board.save()
            return redirect('/board/register')


# 게시글 전부 출력하는 함수.
def list(request):
    posts = Board.objects.all()
    return render(request, 'board/list.html', {'posts': posts})


# 게시글 하나만 읽는 함수.
def read(request, bid):
    post = Board.objects.get(Q(id=bid))
    comments = Comment.objects.filter(board_id=bid)  # 게시글에 달린 코멘트들만 불러와서 comment라는 변수에 저장함
    commentForm = CommentForm()  # 코멘트 작성 폼을 저장해서 HTML에 보내줌
    return render(request, 'board/read.html', {'post': post, 'comments': comments, 'commentForm': commentForm})


# 게시글 삭제 함수
@login_required(login_url='/users/login')
def delete(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user != post.writer:
        return render(request, 'users/urNotRightUser.html')
    post.delete()
    return redirect('/board/list')


# 게시글 수정 함수
@login_required(login_url='/users/login')
def update(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user != post.writer:  # 로그인한 유저랑 작성자랑 같지 않으면
        return render(request, 'users/urNotRightUser.html')  # 로그인한 유저가 아니라는 HTML을 보여줌
    else:  # 로그인한 유저가 맞으면
        if request.method == "GET":  # GET 방식일 경우
            boardForm = BoardForm(instance=post)  # 기존게시글의 내용을 저장해서
            return render(request, 'board/update.html', {'boardForm': boardForm})  # 수정창에 보이게 함
        elif request.method == "POST":
            boardForm = BoardForm(request.POST)
            if boardForm.is_valid():
                post.title = boardForm.cleaned_data['title']
                post.contents = boardForm.cleaned_data['contents']
                post.director = boardForm.cleaned_data['director']
                post.cast = boardForm.cleaned_data['cast']
                post.cast2 = boardForm.cleaned_data['cast2']
                post.cast3 = boardForm.cleaned_data['cast3']
                post.cast4 = boardForm.cleaned_data['cast4']
                post.poster = boardForm.cleaned_data['poster']
                post.opening_date = boardForm.cleaned_data['opening_date']
                post.save()
                return redirect('/board/read/' + str(bid))


# 게시글 좋아요 함수.
@login_required(login_url='/users/login')
def like(request, bid):
    post = Board.objects.get(Q(id=bid))
    user = request.user
    if post.like.filter(id=user.id).exists():  # 게시글 좋아요 이미 눌렀을 때 좋아요 누르면
        post.like.remove(user)  # 게시글 좋아요 제거
        message = 'del'
    else:  # 게시글 좋아요 안 눌렀을 때 좋아요 누르면
        post.like.add(user)  # 게시글 좋아요 추가
        message = 'add'
    return JsonResponse({'message': message, 'like_cnt': post.like.count()})  # 좋아요 추가/제거 메시지와 좋아요 갯수 전송
