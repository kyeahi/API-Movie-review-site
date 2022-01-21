
from django.contrib import admin
from django.urls import path



import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup', users.views.signup),
    path('users/login', users.views.userlogin),
    path('users/logout', users.views.userlogout),
    path('base', users.views.base),
    path('users/change_password', users.views.change_password),
    path('users/user_delete', users.views.user_delete),
]