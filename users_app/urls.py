from django.urls import path
from users_app import views

urlpatterns = [
    path('user/', views.UserAPI.as_view()),
    path('room/', views.RoomAPI.as_view()),
    path('super/', views.SuperUsersAPI.as_view()),
]