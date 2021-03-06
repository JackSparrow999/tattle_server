from django.urls import path
from users_app import views

urlpatterns = [
    path('user/', views.UserAPI.as_view()),
    path('room/', views.RoomAPI.as_view()),
    path('add_user/', views.AddUsersToRoomAPI.as_view()),
    path('login/', views.Login.as_view()),
]