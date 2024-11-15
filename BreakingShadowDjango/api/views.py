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
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # Kiểm tra tính hợp lệ của token
        token = request.data.get("token", None)
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            # Truy vấn thông tin người dùng
            user = User.objects.get(id=user_id)
            user_data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
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
