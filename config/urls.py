from django.contrib import admin
from django.urls import path
import users.views
import comment.views
import board.views

urlpatterns = [
    path('base', board.views.list), # 메인 페이지
    path('', board.views.list),     # 이것도 메인페이지로 한다.

    # 게시글
    path('board/register', board.views.register),
    path('board/list', board.views.list),
    path('board/read/<int:bid>', board.views.read),
    path('board/delete/<int:bid>', board.views.delete),
    path('board/update/<int:bid>', board.views.update),
    path('board/like/<int:bid>', board.views.like),

    # 댓글
    path('comment/register/<int:bid>', comment.views.register), # bid로 게시글의 인덱스를 받음
    path('comment/list', comment.views.list),
    path('comment/read/<int:cid>', comment.views.read),
    path('comment/delete/<int:cid>', comment.views.delete),
    path('comment/update/<int:cid>', comment.views.update),
    path('comment/like/<int:cid>', comment.views.like),

    #유저
    path('users/pchange', users.views.pchange),
    path('users/signup', users.views.signup),
    path('users/delete', users.views.userDelete),
    path('users/login', users.views.userlogin),
    path('users/logout', users.views.userlogout),
]
