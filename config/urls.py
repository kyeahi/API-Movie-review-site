"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import users.views
import comment.views

urlpatterns = [
    path('base', users.views.base),
    path('users/pchange', users.views.pchange),
    path('users/signup', users.views.signup),
    path('users/delete', users.views.userDelete),
    path('users/login', users.views.userlogin),
    path('users/logout', users.views.userlogout),

    path('comment/register', comment.views.register),
    path('comment/list', comment.views.posts),
    path('comment/read/<int:bid>', comment.views.read),  # 뒤에 int타입의 변수를 받아 bid에 저장
    path('comment/delete/<int:bid>', comment.views.delete),
    path('comment/update/<int:bid>', comment.views.update),
    path('comment/like/<int:bid>', comment.views.like),
]
