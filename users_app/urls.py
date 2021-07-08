from django.urls import path
from users_app import views

url_patterns = [
    path('user/', views.UserAPI.as_view()),
    path('room/', views.RoomAPI.as_view()),
]