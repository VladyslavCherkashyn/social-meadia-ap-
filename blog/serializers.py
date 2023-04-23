from rest_framework import serializers
from .models import User, Post, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ["username", "email", "profile_picture", "bio"]


class UserFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    media = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["id", "user", "content", "media", "hashtags", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
