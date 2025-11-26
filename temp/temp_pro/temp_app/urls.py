from django.urls import path
from . import views

urlpatterns=[
    path('get_company/', view=views.get_info),
    path('reg_company/', view=views.reg_info),
    path('update_company/<str:id>', view=views.update_info),
    path('del_company/<str:id>', view=views.del_info)
]