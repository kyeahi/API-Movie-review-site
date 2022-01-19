from django.contrib import admin
from django.urls import path

import board.views

urlpatterns = [
    path('base', user.views.base),

    path('register/list', board.views.list),
    path('read/<int:bid>', board.views.read),
    path('register/', board.views.register),

<<<<<<< Updated upstream
    path('user/pchange', user.views.pchange),
    path('user/signup', user.views.pchange),
    path('user/delete', user.views.pchange),
    path('user/login', user.views.pchange),
    path('user/logout', user.views.pchange),
=======
    path('user/pchange', user.views.userDelete),
    path('user/signup', user.views.signup),
    path('user/delete', user.views.userDelete),
    path('user/login', user.views.userlogin),
    path('user/logout', user.views.userlogout),

>>>>>>> Stashed changes
]
