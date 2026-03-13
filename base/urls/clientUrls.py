from django.urls import path
from base.views.client.authViews import (
    RegisterView,
    LoginView,
    ResendOTPView,
    VerifyOTPView,
    ForgetPasswordView,
    ForgetPasswordConfirmView,
    ResetPasswordView,
    TokenRefreshView,
    LogoutView,
    UpdateOneSignalPlayerIdView,
)
from base.views.client.profileViews import ProfileView, DeleteProfilePictureView
from base.views.client.complaintViews import ComplaintListCreateView, ComplaintDetailView
from base.views.client.newsViews import NewsListView, NewsDetailView
from base.views.client.categoryViews import CategoryListView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='client-register'),
    path('auth/login/', LoginView.as_view(), name='client-login'),
    path('auth/resend-otp/', ResendOTPView.as_view(), name='client-resend-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='client-verify-otp'),
    path('auth/forget-password/', ForgetPasswordView.as_view(), name='client-forget-password'),
    path('auth/forget-password/confirm/', ForgetPasswordConfirmView.as_view(), name='client-forget-password-confirm'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='client-reset-password'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='client-token-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='client-logout'),
    path('auth/update-player-id/', UpdateOneSignalPlayerIdView.as_view(), name='client-player-id'),

    # Profile
    path('profile/', ProfileView.as_view(), name='client-profile'),
    path('profile/remove-profile-picture/', DeleteProfilePictureView.as_view(), name='client-profile-picture'),

    # Complaints
    path('complaints/', ComplaintListCreateView.as_view(), name='client-complaints'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='client-complaint-detail'),

    # News
    path('news/', NewsListView.as_view(), name='client-news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='client-news-detail'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='client-categories'),
]
