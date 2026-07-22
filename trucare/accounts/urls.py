from django.urls import path

from .views import JWTLoginView, JWTRefreshView, MeAPIView, RegisterAPIView


urlpatterns = [
    # path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", JWTLoginView.as_view(), name="token-obtain-pair"),
    path("refresh/", JWTRefreshView.as_view(), name="token-refresh"),
    path("me/", MeAPIView.as_view(), name="auth-me"),
]
