from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from comment.forms import CommentForm
from comment.models import Comment
from board.models import Board


# 댓글 등록 함수
# 입력 : 사용자, 게시글번호
# 기능 : HTML로 부터 댓글양식을 POST로 받고 저장한다.
# 출력 : 기존의 게시글 URL경로
@login_required(login_url='/users/login')
def register(request, bid):
    post = Board.objects.get(Q(id=bid))             # 게시글번호를 post 변수에 저장함
    if request.method == "GET":
        commentForm = CommentForm()
        return render(request, 'comment/register.html', {'commentForm': commentForm})
    elif request.method == "POST":                  # POST 방식으로 입력받으면
        commentForm = CommentForm(request.POST)     # 입력받은 댓글양식을 commentForm이라는 변수에 저장함
        if commentForm.is_valid():                  # 양식이 올바르면
            comment = commentForm.save(commit=False)# comment라는 변수에 댓글양식을 저장한다.
            comment.writer = request.user           # 댓글작성자를 현재사용자로 저장한다.
            comment.board_id = post.id              # 댓글이 달린 게시글번호를 현재게시글의 번호로 저장한다.
            comment.save()                          # 댓글을 DB에 저장한다.
            return redirect('/board/read/'+str(bid))# 기존 게시글로 돌아간다.

# 댓글 목록 전체를 보는 함수. 댓글을 게시글별로 보여주기 때문에 사용하지 않을 함수이다.
# 입력 : 사용자
# 기능 : 댓글 전부 출력
# 출력 : 댓글을 출력하는 HTML파일, 댓글 전부를 담은 변수
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments': comments})

# 댓글 하나를 읽는 함수
# 입력 : 사용자, 댓글번호
# 기능 : 댓글 하나 출력
# 출력 : 댓글 하나를 출력하는 HTML파일, 댓글 하나를 담은 변수
def read(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    return render(request, 'comment/read.html', {'comment': comment})

# 댓글 삭제 함수
# 입력 : 사용자, 댓글번호
# 기능 : 작성자와 사용자가 동일하면 삭제, 동일하지 않으면 삭제안하고 '적절한 사용자가 아닙니다.'라는 HTML 실행.
# 출력 : 댓글이 지워질 게시글 목록으로 돌아감
@login_required(login_url='/users/login')
def delete(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    bid = comment.board_id
    if request.user != comment.writer:
        return render(request, 'users/urNotRightUser.html')
    comment.delete()
    return redirect('/board/read/'+str(bid))

# 댓글 수정 함수
# 입력 : 사용자, 댓글번호
# 기능 : 작성자와 사용자가 동일하면 댓글수정HTML을 보여줌, 댓글을 입력받으면 다시 DB에 저장함.
# 출력 : 댓글이 수정될 게시글 목록으로 돌아감.
@login_required(login_url='/users/login')
def update(request, cid):
    comment = Comment.objects.get(Q(id=cid))
    if request.user != comment.writer:                      # 로그인한 유저랑 작성자랑 같지 않으면
        return render(request, 'users/urNotRightUser.html') # 적절한 유저가 아니라는 HTML을 보여줌
    else:                                                   # 로그인한 유저가 맞으면
        if request.method == "GET":                         # 아래 코드 실행
            commentForm = CommentForm(instance=comment)     # 이번엔 비어있게 주는게 아님. 기존코멘트를 다시 보내줘야함. 수정창이 뜸
            return render(request, 'comment/update.html', {'commentForm':commentForm})
        elif request.method == "POST":
            commentForm = CommentForm(request.POST)
            if commentForm.is_valid():
                comment.title = commentForm.cleaned_data['title']
                comment.contents = commentForm.cleaned_data['contents']
                comment.save()
                return redirect('/board/read/'+str(comment.board_id))     # 수정하고 기존 게시글로 돌아감

# 댓글 좋아요 함수
# 입력 : 사용자, 댓글번호
# 기능 : 좋아요를 이미 누른 사용자인지 확인, 이미 눌렀으면 좋아요 감소, 안눌렀으면 좋아요 증가
# 출력 : Json으로 add, del 중 하나의 메시지와 like_cnt를 보내줌.
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