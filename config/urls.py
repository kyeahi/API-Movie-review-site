from django.contrib import admin
from django.urls import path

import board.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/list', board.views.list),
    path('read/<int:bid>', board.views.read),
    path('register/', board.views.register),

    path('user/pchange', user.views.pchange),
    path('user/signup', user.views.singup),
    path('user/login', user.views.login),
    path('user/logout', user.views.logout),

]
