from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from comment.forms import CommentForm
from comment.models import Comment


#코멘트 등록 함수
@login_required(login_url='/users/login')
def register(request):
    if request.method == "GET":
        commentForm = CommentForm()
        return render(request, 'comment/register.html', {'commentForm': commentForm})
    elif request.method == "POST":
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.writer = request.user
            comment.save()
            return redirect('/comment/register')

# 코멘트 목록을 뿌려주는 함수
def posts(request):
    posts = Comment.objects.all()
    return render(request, 'comment/list.html', {'posts': posts})

# 코멘트 하나를 읽는 함수
def read(request, bid):
    post = Comment.objects.get(Q(id=bid))
    return render(request, 'comment/read.html', {'post': post})

# 코멘트 삭제 함수
@login_required(login_url='/users/login')
def delete(request, bid):
    post = Comment.objects.get(Q(id=bid))
    if request.user != post.writer:
        return render(request, 'users/urNotLoginUser.html')
    post.delete()
    return redirect('/comment/list')

# 코멘트 수정 함수
@login_required(login_url='/users/login')
def update(request, bid):
    post = Comment.objects.get(Q(id=bid))
    if request.method == "GET":     # GET 방식, commentUpdate/9 방식으로 접속하면
        commentForm = CommentForm(instance=post) # 이번엔 비어있게 주는게 아님. 기존코멘트를 다시 보내줘야함. 수정창이 뜸
        return render(request, 'comment/update.html', {'commentForm':commentForm})    #
    elif request.method == "POST":
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            post.title = commentForm.cleaned_data['title']
            post.contents = commentForm.cleaned_data['contents']
            post.save()
            return redirect('/comment/read/' + str(bid))

# 코멘트 좋아요 함수
@login_required(login_url='/users/login')
def like(request, bid):
    post = Comment.objects.get(Q(id=bid))
    user = request.user
    if post.like.filter(id=user.id).exists():   # 게시글 좋아요 이미 눌렀을 때 좋아요 누르면
        post.like.remove(user)                  # 게시글 좋아요 제거
        message = 'del'
    else:                                       # 게시글 좋아요 안 눌렀을 때 좋아요 누르면
        post.like.add(user)                     # 게시글 좋아요 추가
        message = 'add'
    return JsonResponse({'message': message, 'like_cnt': post.like.count()})    # 좋아요 추가/제거 메시지와 좋아요 갯수 전송