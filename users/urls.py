from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.user_list, name='users_list'),
    path("users/<int:user_id>/", views.user_detail, name='user_detail'),

]