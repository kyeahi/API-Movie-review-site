from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from board.forms import BoardForm
from board.models import Board
from comment.models import Comment
from comment.forms import CommentForm
"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
            ids='ga:259141337',  # 바꿔야댐
            start_date='7daysAgo',
            end_date='today',
            metrics='ga:sessions').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        res = results.get('rows')[0][0]
        print('View (Profile):', results.get('profileInfo').get('profileName'))
        print('Total Sessions:', res)
        return res
    else:
        print('No results found')


def main(a):
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = 'C:/PythonProject/movie/my-project-the-team-one-b6af10fb94a9.json'  #바꿔야댐

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    sessions = print_results(get_results(service, profile_id))
    return render(a, 'board/info.html', {'sessions' : sessions})

if __name__ == '__main__':
    main()

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
            board.writer=request.user
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
    commentForm = CommentForm()                      # 코멘트 작성 폼을 저장해서 HTML에 보내줌
    return render(request, 'board/read.html', {'post': post, 'comments': comments, 'commentForm': commentForm})

# 게시글 삭제 함수
@login_required(login_url='/users/login')
def delete(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user.is_staff != True:
        return render(request, 'users/urNotRightUser.html')
    post.delete()
    return redirect('/board/list')

# 게시글 수정 함수
@login_required(login_url='/users/login')
def update(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user.is_staff != True:                       # 로그인한 유저가 관리자가 아니라면
        return render(request, 'users/urNotRightUser.html') # 로그인한 유저가 아니라는 HTML을 보여줌
    else:                                                   # 로그인한 유저가 관리자라면
        if request.method == "GET":                         # GET 방식일 경우
            boardForm = BoardForm(instance=post)            # 기존게시글의 내용을 저장해서
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
                return redirect('/board/list')

#게시글 좋아요 함수.
@login_required(login_url='/users/login')
def like(request, bid):
    post = Board.objects.get(Q(id=bid))
    user = request.user
    if post.like.filter(id=user.id).exists():   # 게시글 좋아요 이미 눌렀을 때 좋아요 누르면
        post.like.remove(user)                  # 게시글 좋아요 제거
        message = 'del'
    else:                                       # 게시글 좋아요 안 눌렀을 때 좋아요 누르면
        post.like.add(user)                     # 게시글 좋아요 추가
        message = 'add'
    return JsonResponse({'message': message, 'like_cnt': post.like.count()})    # 좋아요 추가/제거 메시지와 좋아요 갯수 전송
