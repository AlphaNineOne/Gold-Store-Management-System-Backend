from django.urls import path
from core.views import RegistrationView, ForgetPasswordView, UserDetailView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    # path('google/login/', GoogleLoginView.as_view(), name='google-login'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forget/password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('me/', UserDetailView.as_view(), name='user'),
    path('change/password/', ChangePasswordView.as_view(), name='change-password'),

]
