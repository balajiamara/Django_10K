from django.urls import path
from . import views

urlpatterns=[
    path('get_info/',view=views.get_info),
    path('reg_info/',view=views.reg_info),
    path('update_info/<int:id>',view=views.update_info),
    path('delete_info/<int:id>',view=views.delete_info)
]