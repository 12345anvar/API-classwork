from django.contrib.auth.models import User
from django.utils import timezone
import re
from rest_framework import serializers
from posts.models import Post

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    member_since_days = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'full_name', 'member_since_days']
        read_only_fields = ['username', 'email']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_member_since_days(self, obj):
        delta = timezone.now() - obj.date_joined
        return delta.days


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email band.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        if len(data['password']) < 8 or not re.search(r"\d", data['password']):
            raise serializers.ValidationError("The password must consist of 8 characters and 1 number.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']

    def validate(self, data):
        user = self.context['request'].user
        if Post.objects.filter(author=user, title=data['title']).exists():
            raise serializers.ValidationError("You have a post with a title like this.")
        return data