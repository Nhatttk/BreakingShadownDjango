from rest_framework import viewsets
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # Lấy token từ request
        token = request.data.get("token", None)
        if not token:
            return Response({"message": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Kiểm tra token
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            # Truy vấn User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Truy vấn Profile
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                return Response({"message": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize Profile
            serializer = ProfileSerializer(profile)
            user_data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile": serializer.data,
            }

            return Response(
                {"message": "Token is valid", "user": user_data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Token is invalid", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer


class EmergencyHelpViewSer(viewsets.ModelViewSet):
    queryset = EmergencyHelp.objects.all()
    serializer_class = EmergencyHelpSerializer


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer

from django.core.mail import send_mail
from django.core.mail import EmailMessage

class SendEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data["subject"]
            message = serializer.validated_data["message"]
            ip = serializer.validated_data["ip"]
            recipient_email = serializer.validated_data["recipient_email"]

            # Định dạng message dưới dạng HTML
            html_message = f"""
            <html>
            <body>
                <h2>{subject}</h2>
                <p>{message}</p>
                <p>My ip: {ip}</p>
                <p>Thank you for using our service!</p>
            </body>
            </html> """

            try:
                email = EmailMessage(
                    subject, html_message, "your-email@gmail.com", recipient_email
                )
                email.content_subtype = "html"  # Đặt định dạng HTML cho nội dung email
                email.send()
                return Response(
                    {"status": "Email sent successfully!"}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"status": "Error sending email", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
class PrivateChatView(APIView):
    def get(self, request, username):
        # Lấy danh sách các cuộc trò chuyện của người dùng
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        chats = PrivateChat.objects.filter(user1=profile) | PrivateChat.objects.filter(user2=profile)
        serializer = PrivateChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        # Tạo cuộc trò chuyện mới nếu chưa tồn tại
        user1 = request.user
        user2_id = request.data.get('user2')
        user2 = get_object_or_404(User, id=user2_id)

        # Kiểm tra xem cuộc trò chuyện đã tồn tại chưa
        chat, created = PrivateChat.objects.get_or_create(
            user1=user1 if user1.id < user2.id else user2,
            user2=user2 if user1.id < user2.id else user1
        )
        serializer = PrivateChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageView(APIView):
    def get(self, request, chat_id):
        # Lấy tất cả tin nhắn trong cuộc trò chuyện
        print(request.user)
        chat = get_object_or_404(PrivateChat, id=chat_id)
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, chat_id):
        # Gửi tin nhắn mới
        chat = get_object_or_404(PrivateChat, id=chat_id)
        sender = request.user
        content = request.data.get('content')

        message = Message.objects.create(chat=chat, sender=sender, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)