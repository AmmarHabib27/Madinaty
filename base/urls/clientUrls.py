from django.urls import path
from base.views.client.authViews import (
    RegisterView,
    RequestOTPView,
    VerifyOTPView,
    LogoutView,
    UpdateOneSignalPlayerIdView,
)
from base.views.client.profileViews import ProfileView, DeleteProfilePictureView
from base.views.client.complaintViews import ComplaintListCreateView, ComplaintDetailView
from base.views.client.newsViews import NewsListView, NewsDetailView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='client-register'),
    path('auth/request-otp/', RequestOTPView.as_view(), name='client-request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='client-verify-otp'),
    path('auth/logout/', LogoutView.as_view(), name='client-logout'),
    path('auth/player-id/', UpdateOneSignalPlayerIdView.as_view(), name='client-player-id'),

    # Profile
    path('profile/', ProfileView.as_view(), name='client-profile'),
    path('profile/picture/', DeleteProfilePictureView.as_view(), name='client-profile-picture'),

    # Complaints
    path('complaints/', ComplaintListCreateView.as_view(), name='client-complaints'),
    path('complaints/<int:pk>/', ComplaintDetailView.as_view(), name='client-complaint-detail'),

    # News
    path('news/', NewsListView.as_view(), name='client-news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='client-news-detail'),
]
