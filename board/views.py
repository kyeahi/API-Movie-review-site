from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from board.forms import BoardForm
from board.models import Board
from comment.models import Comment
from comment.forms import CommentForm

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
    if request.user != post.writer:
        return render(request, 'users/urNotRightUser.html')
    post.delete()
    return redirect('/board/list')

# 게시글 수정 함수
@login_required(login_url='/users/login')
def update(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user != post.writer:                         # 로그인한 유저랑 작성자랑 같지 않으면
        return render(request, 'users/urNotRightUser.html') # 로그인한 유저가 아니라는 HTML을 보여줌
    else:                                                   # 로그인한 유저가 맞으면
        if request.method == "GET":                         # 아래 코드 실행
            boardForm = BoardForm(instance=post) # 이번엔 비어있게 주는게 아님. 기존게시글을 다시 보내줘야함. 수정창이 뜸
            return render(request, 'board/update.html', {'boardForm': boardForm})    #
        elif request.method == "POST":
            boardForm = BoardForm(request.POST)
            if boardForm.is_valid():
                post.title = boardForm.cleaned_data['title']
                post.contents = boardForm.cleaned_data['contents']
                post.save()
                return redirect('/board/read/' + str(bid))

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