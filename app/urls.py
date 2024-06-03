from django.urls import path
from rest_framework import permissions
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Social Net API",
        default_version='v1',
        description="API for Social App",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('users/search/', views.UserSearchView.as_view(), name='user-search'),
    path('friend-requests/', views.FriendRequestCreateView.as_view(), name='friend-request-create'),
    path('friend-requests/accept/', views.FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friend-requests/reject/', views.FriendRequestRejectView.as_view(), name='friend-request-reject'),
    path('friends/', views.FriendListView.as_view(), name='friend-list'),
    path('friend-requests/pending/', views.PendingFriendRequestListView.as_view(), name='pending-friend-requests'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]