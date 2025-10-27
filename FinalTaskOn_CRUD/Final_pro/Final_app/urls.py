from django.urls import path
from . import views

urlpatterns = [
    path('get_Insta_Acc/' ,view= views.get_Insta_Acc),
    path('reg_Insta_Acc/' ,view= views.reg_Insta_Acc),
    path('update_Insta_Acc/<str:id>/' ,view= views.update_Insta_Acc),
    path('delete_Insta_Acc/<str:id>/' ,view= views.delete_Insta_Acc),
]