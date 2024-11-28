from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    # user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["address", "phone", "avatar", "user"]

    def create(self, validated_data):
        # Lấy dữ liệu user từ validated_data
        user_data = validated_data.pop("user_id")

        # Tạo hoặc lấy user
        user, created = User.objects.get_or_create(**user_data)

        # Tạo profile với user đã tạo
        profile = Profile.objects.create(user=user, **validated_data)

        return profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        group = Group.objects.get(name="user")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.groups.set([group])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title", "create_at", "update_at", "imgUrl", "navigationPath"]


class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Expert
        fields = [
            "jobTitle",
            "avatar",
            "address",
            "rating",
            "reviews",
            "user"
        ]


class EmergencyHelpSerializer(serializers.ModelSerializer): 
    class Meta:
        model = EmergencyHelp
        fields = '__all__'


class KnowledgeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Knowledge
        fields = [
            "title",
            "image",
            "short_description",
            "content",
            "created_at",
            "updated_at",
            "user"
        ]


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    ip = serializers.CharField()
    recipient_email = serializers.ListField(
        child=serializers.EmailField(),  # Each item in the list must be a valid email
        allow_empty=False,
    )


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer()
    class Meta:
        model = Message
        fields = ['chat', 'sender', 'content', 'timestamp']

class PrivateChatSerializer(serializers.ModelSerializer):
    user1 = UserProfileSerializer()
    user2 = UserProfileSerializer()
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = PrivateChat
        fields = ['id', 'user1', 'user2', 'messages']