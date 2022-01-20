from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from comment.forms import CommentForm
from comment.models import Comment
from board.models import Board


#코멘트 등록 함수
@login_required(login_url='/users/login')
def register(request, bid):
    post = Board.objects.get(Q(id=bid))             # 게시글의 번호 저장함
    if request.method == "POST":
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.writer = request.user
            comment.board_id = post.id              # 댓글이 어느 게시글에 속하는지 저장함
            comment.save()                          # 댓글을 DB에 저장
            return redirect('/board/read/'+str(bid))     # 기존 게시글로 돌아감

# 코멘트 목록을 뿌려주는 함수
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments': comments})

# 코멘트 하나를 읽는 함수
def read(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    return render(request, 'comment/read.html', {'comment': comment})

# 코멘트 삭제 함수
@login_required(login_url='/users/login')
def delete(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    if request.user != comment.writer:
        return render(request, 'users/urNotLoginUser.html')
    comment.delete()
    return redirect('/comment/list')

# 코멘트 수정 함수
@login_required(login_url='/users/login')
def update(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    if request.user != comment.writer:                         # 로그인한 유저랑 작성자랑 같지 않으면
        return render(request, 'users/urNotLoginUser.html') # 로그인한 유저가 아니라는 HTML을 보여줌
    else:                                                   # 로그인한 유저가 맞으면
        if request.method == "GET":                         # 아래 코드 실행
            commentForm = CommentForm(instance=comment) # 이번엔 비어있게 주는게 아님. 기존코멘트를 다시 보내줘야함. 수정창이 뜸
            return render(request, 'comment/update.html', {'commentForm':commentForm})
        elif request.method == "POST":
            commentForm = CommentForm(request.POST)
            if commentForm.is_valid():
                comment.title = commentForm.cleaned_data['title']
                comment.contents = commentForm.cleaned_data['contents']
                comment.save()
                return redirect('/board/read/'+str(comment.board_id))     # 수정하고 기존 게시글로 돌아감

# 코멘트 좋아요 함수
@login_required(login_url='/users/login')
def like(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    user = request.user
    if comment.like.filter(id=user.id).exists():   # 게시글 좋아요 이미 눌렀을 때 좋아요 누르면
        comment.like.remove(user)                  # 게시글 좋아요 제거
        message = 'del'
    else:                                          # 게시글 좋아요 안 눌렀을 때 좋아요 누르면
        comment.like.add(user)                     # 게시글 좋아요 추가
        message = 'add'
    return JsonResponse({'message': message, 'like_cnt': comment.like.count()})    # 좋아요 추가/제거 메시지와 좋아요 갯수 전송