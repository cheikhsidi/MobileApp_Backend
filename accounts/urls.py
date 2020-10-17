from django.conf.urls import url, include
from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserAPIView, LoginAPIView, LogoutUserAPIView, FacebookLogin, UserAPIView, ChangePasswordView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView


urlpatterns = [
    # url('auth/login/',
    #     obtain_auth_token,
    #     name='auth_user_login'),
    url('auth/login/', LoginAPIView.as_view(), name='auth-user-login'),
    # url('auth/login/', login, name='auth_user_login'),
    url('auth/register/', CreateUserAPIView.as_view(), name='auth_user_create'),
    url('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    url('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    url('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

    # url('reset-password/verify-token/', CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    url('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    url('users/update/', UserAPIView.as_view(), name = 'update_user'),
    # url('users/', UserDetail.as_view(), name = 'users')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
