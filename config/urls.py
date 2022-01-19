from django.contrib import admin
from django.urls import path

import board.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/list', board.views.list),
    path('read/<int:bid>', board.views.read),
    path('register/', board.views.register),

    path('user/pchange', user.views.pchange),
    path('user/signup', user.views.pchange),
    path('user/delete', user.views.pchange),
    path('user/login', user.views.pchange),
    path('user/logout', user.views.pchange),
]
