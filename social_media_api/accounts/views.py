from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)

            return Response({
                "user": serializer.data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "followers_count": user.followers.count(),
            "following_count": user.following.count(),
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        return Response({"message": "Successfully followed user"})

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        request.user.following.remove(user_to_unfollow)
        return Response({"message": "Successfully unfollowed user"})
    
    
class UserListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    if user_to_follow == request.user:
        return Response(
            {"error": "You cannot follow yourself"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.user.following.filter(id=user_to_follow.id).exists():
        return Response(
            {"error": "You are already following this user"},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.following.add(user_to_follow)

    # Create notification
    Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb="started following you"
    )

    return Response({"message": "User followed successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

    if not request.user.following.filter(id=user_to_unfollow.id).exists():
        return Response(
            {"error": "You are not following this user"},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.following.remove(user_to_unfollow)

    return Response({"message": "User unfollowed successfully"})