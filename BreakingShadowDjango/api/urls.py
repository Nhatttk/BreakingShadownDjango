from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
# Đổi basename để tránh trùng lặp
router.register(r"user-profiles", UserProfileViewSet, basename="user-profile")
router.register(r"categories", CategoryViewSet)
router.register(r"experts", ExpertViewSet)
router.register(r"emergency-help", EmergencyHelpViewSer)
router.register(r"knowledge", KnowledgeViewSet)
# GET /profiles/: lấy danh sách tất cả profile.
# POST /profiles/: tạo một profile mới.
# GET /profiles/{id}/: lấy thông tin chi tiết của một profile theo ID.
# PUT /profiles/{id}/: cập nhật một profile theo ID.
# DELETE /profiles/{id}/: xóa một profile theo ID.

from . import consumers

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("get-user/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("get-expert-user/", ExpertUserViewSet.as_view(), name="expert_user"),
    path("send-email/", SendEmailView.as_view(), name="send-email"),
    path('chats/<str:username>/', PrivateChatView.as_view(), name='private_chat'),
    path('chats/<int:chat_id>/messages/', MessageView.as_view(), name='chat_messages'),
]

websocket_urlpatterns = [
    path('ws/private-chat/<int:chat_id>/', consumers.PrivateChatConsumer.as_asgi()),
]