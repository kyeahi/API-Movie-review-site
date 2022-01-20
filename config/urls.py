from django.contrib import admin
from django.urls import path
import user.views
import comment.views
import board.views
import user.views

urlpatterns = [

    #유저
    path('user/pchange', user.views.pchange),
    path('user/signup', user.views.usersignup),
    path('user/login', user.views.userlogout),
    path('user/logout', user.views.userlogout),
    path('users/delete', user.views.userDelete),

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
    path('comment/register', comment.views.register),
    path('comment/list', comment.views.posts),
    path('comment/read/<int:bid>', comment.views.read),  # 뒤에 int타입의 변수를 받아 bid에 저장
    path('comment/delete/<int:bid>', comment.views.delete),
    path('comment/update/<int:bid>', comment.views.update),
    path('comment/like/<int:bid>', comment.views.like),



]
