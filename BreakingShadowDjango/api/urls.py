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

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("get-user/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("send-email/", SendEmailView.as_view(), name="send-email"),
]
