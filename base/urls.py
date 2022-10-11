from django.urls import path

from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'), #ok
    path('logout/', CustomLogoutView.as_view(), name='logout'), #ok
    path('register/', RegisterPage.as_view(), name='register'), #ok

    path('', HomeView.as_view(), name='home'), #ok
    path('room/<str:slug>/', RoomPage.as_view(), name='room'), #ok
    path('profile/<str:pk>/', UserProfile.as_view(), name='user_profile'), #ok

    path('create-room/', CreateRoom.as_view(), name='create-room'), #ok
    path('update-room/<str:slug>/', UpdateRoom.as_view(), name='update-room'), #ok
    path('delete-room/<str:slug>/', DeleteRoomPage.as_view(), name='delete-room'), #ok
    path('delete-message/<str:pk>/', DeleteMessageRoom.as_view(), name='delete-message'), #ok

    path('update-user/', UpdateUser.as_view(), name='update-user'), #ok

    path('topics/', TopicsPage.as_view(), name='topics'), #ok
    path('activity/', ActivitiesPage.as_view(), name='activity'), #ok

]