from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Like, Subscription
from apps.posts.models import Post
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserShortSerializer
from apps.posts.serializers import PostSerializer


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({'status': 'лайк поставлен'}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        Like.objects.filter(user=request.user, post_id=post_id).delete()
        return Response({'status': 'лайк удалён'}, status=status.HTTP_204_NO_CONTENT)


User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target = User.objects.get(pk=user_id)
        if target == request.user:
            return Response({'detail': 'Нельзя подписаться на себя'}, status=400)
        Subscription.objects.get_or_create(follower=request.user, following=target)
        return Response({'status': f'Вы подписались на {target.username}'})

    def delete(self, request, user_id):
        Subscription.objects.filter(follower=request.user, following_id=user_id).delete()
        return Response({'status': 'Подписка удалена'})

class FollowersListView(generics.ListAPIView):
    serializer_class = UserShortSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(following__following_id=user_id)

    def get_serializer_context(self):
        return {'request': self.request}

class FollowingListView(generics.ListAPIView):
    serializer_class = UserShortSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(followers__follower_id=user_id)

    def get_serializer_context(self):
        return {'request': self.request}

class MyFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list('following_id', flat=True)
        return Post.objects.filter(author_id__in=following_ids).order_by('-created_at')