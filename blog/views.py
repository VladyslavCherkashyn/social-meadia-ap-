from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Post, Profile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    PostSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="update-profile")
    def update_profile(self, request, pk=None):
        user = self.get_object()
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="search")
    def search_users(self, request):
        username = request.query_params.get("username")
        users = User.objects.filter(username__icontains=username)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        following_users = self.request.user.profile.following.all()
        queryset = queryset.filter(user__profile__in=following_users)
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_profile = self.get_object()
        follow_user = User.objects.get(username=request.data.get("username"))
        user_profile.following.add(follow_user.profile)
        return Response({"detail": "User followed successfully"})

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user_profile = self.get_object()
        unfollow_user = User.objects.get(username=request.data.get("username"))
        user_profile.following.remove(unfollow_user.profile)
        return Response({"detail": "User unfollowed successfully"})

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        user_profile = self.get_object()
        following_users = user_profile.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)
