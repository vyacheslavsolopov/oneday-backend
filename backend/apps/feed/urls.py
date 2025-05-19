from django.urls import path
from .views import LikePostView, FollowUserView, FollowersListView, FollowingListView, MyFeedView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='followers'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='following'),
    path('my-feed/', MyFeedView.as_view(), name='my-feed'),
]
