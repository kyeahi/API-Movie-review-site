
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup', users.views.signup),
    path('users/login', users.views.userlogin),
    path('users/logout', users.views.userlogout),
    path('base', users.views.base),
    path('users/change_password', users.views.change_password),
    path('users/user_delete', users.views.user_delete),
    path('creat', users.views.create),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)