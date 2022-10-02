from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import RoomsView, RoomDetailView, TopicListView, TopicDetailView, UserListView, UserDetailView

urlpatterns = [
    path('rooms/', RoomsView.as_view()),
    path('rooms/<int:pk>/', RoomDetailView.as_view()),
    path('topics/', TopicListView.as_view()),
    path('topics/<int:pk>/', TopicDetailView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)