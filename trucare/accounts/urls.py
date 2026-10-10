from django.urls import path

from .views import (
    JWTLoginView,
    JWTRefreshView,
    MeAPIView,
    PasswordChangeView,
    RegisterAPIView,
    RegisterIntakeAgentAPIView,
    UpdateProfile,
    DashboardAPIView,
)


urlpatterns = [
    # path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", JWTLoginView.as_view(), name="token-obtain-pair"),
    path("refresh/", JWTRefreshView.as_view(), name="token-refresh"),
    path("me/", MeAPIView.as_view(), name="auth-me"),
    path("update-profile/", UpdateProfile.as_view(), name="auth-update-profile"),
    path("change-password/", PasswordChangeView.as_view(), name="auth-change-password"),
    path("dashboard/", DashboardAPIView.as_view(), name="auth-dashboard"),
    path("register-intake-agent/", RegisterIntakeAgentAPIView.as_view(), name="auth-register-intake-agent"),
    path("register-intake-agent/<int:pk>/", RegisterIntakeAgentAPIView.as_view(), name="auth-register-intake-agent-detail"),
]
