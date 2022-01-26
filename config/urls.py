from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import users.views
import comment.views
import board.views

urlpatterns = [
                  path('base', board.views.list),  # 메인 페이지에서 게시글을 보여준다.
                  path('', board.views.list),  # 이것도 메인페이지로 한다.
                  # path('oauth2', board.views.request_api2),
                  # path('oauth', board.views.request_api3),

                  path('test2', board.views.request_api4),
                  # path('test3', board.views.request_api5),
                  # path('test4', board.views.main),
                  # 이메일 인증
                  path('users/email', users.views.sendEmail),
                  path('users/match', users.views.match),
                  path('kakao', users.views.kakao_api),
                  path('oauth', users.views.kakao_api1),

                  # 게시글
                  path('board/register', board.views.register),  # 게시글 등록
                  path('board/list', board.views.list),  # 게시글 전부 출력
                  path('board/read/<int:bid>', board.views.read),  # 게시글 하나 출력, 게시글번호 = bid
                  path('board/delete/<int:bid>', board.views.delete),  # 게시글 삭제, 게시글번호 = bid
                  path('board/update/<int:bid>', board.views.update),  # 게시글 수정, 게시글번호 = bid
                  path('board/like/<int:bid>', board.views.like),  # 게시글 좋아요, 게시글번호 = bid

                  # 댓글
                  path('comment/register/<int:bid>', comment.views.register),  # 댓글 등록. 게시글번호 = bid (댓글번호가 아니다!)
                  path('comment/list', comment.views.list),  # 댓글 전부 출력 (안쓸거임)
                  path('comment/read/<int:cid>', comment.views.read),  # 댓글 하나 출력, 댓글번호 = cid
                  path('comment/delete/<int:cid>', comment.views.delete),  # 댓글 하나 삭제, 댓글번호 = cid
                  path('comment/update/<int:cid>', comment.views.update),  # 댓글 하나 수정, 댓글번호 = cid
                  path('comment/like/<int:cid>', comment.views.like),  # 댓글 좋아요. 댓글번호 = cid

                  # 유저
                  path('users/signup/<int:bid>', users.views.signup),  # 유저 회원가입
                  path('users/delete', users.views.userdelete),  # 유저 삭제
                  path('users/login', users.views.userlogin),  # 유저 로그인
                  path('users/logout', users.views.userlogout),  # 유저 로그아웃
                  path('users/change_password', users.views.change_password),  # 유저 패스워드 변경]
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
