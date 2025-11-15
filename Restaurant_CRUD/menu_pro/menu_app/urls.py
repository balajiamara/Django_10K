from django.urls import path
from . import views


urlpatterns=[
    path('add_item/',view=views.add_dish),
    path('show_item/',view=views.get_dish),
    path('modify_item/<str:id>/',view=views.update_dish),
    path('remove_item/<str:id>/',view=views.del_dish),
    path("", views.frontend)
]