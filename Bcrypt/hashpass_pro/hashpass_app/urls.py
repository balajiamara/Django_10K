from django.urls import path
from . import views


urlpatterns=[
    path('reg_user/',view=views.reg_user),
    path('get_user/',view=views.get_user),
    path('login_user/',view=views.login_user)
]