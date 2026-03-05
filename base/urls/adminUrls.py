from django.urls import path
from base.views.admin.authViews import AdminLoginView, AdminLogoutView, AdminChangePasswordView
from base.views.admin.profileViews import AdminProfileView, UserListView, ToggleUserActiveView
from base.views.admin.complaintViews import AdminComplaintListView, AdminComplaintDetailView
from base.views.admin.categoryViews import CategoryListCreateView, CategoryDetailView
from base.views.admin.newsViews import AdminNewsListCreateView, AdminNewsDetailView

urlpatterns = [
    # Auth
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('auth/logout/', AdminLogoutView.as_view(), name='admin-logout'),
    path('auth/change-password/', AdminChangePasswordView.as_view(), name='admin-change-password'),

    # Profile & Users
    path('profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('users/', UserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/toggle-active/', ToggleUserActiveView.as_view(), name='admin-toggle-user'),

    # Complaints
    path('complaints/', AdminComplaintListView.as_view(), name='admin-complaints'),
    path('complaints/<int:pk>/', AdminComplaintDetailView.as_view(), name='admin-complaint-detail'),

    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='admin-categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='admin-category-detail'),

    # News
    path('news/', AdminNewsListCreateView.as_view(), name='admin-news'),
    path('news/<int:pk>/', AdminNewsDetailView.as_view(), name='admin-news-detail'),
]
