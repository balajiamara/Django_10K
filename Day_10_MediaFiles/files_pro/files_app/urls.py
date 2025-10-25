from django.urls import path
from . import views


urlpatterns=[
    path('reg_user/',view=views.reg_user)
]