# views.py
from rest_framework import generics, permissions, status, throttling, pagination, filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Register a new user',
        responses={201: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "id": user.id,
            "email": user.email,
            "token": token.key
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Login with email and password',
        responses={200: openapi.Response(description='Successful login', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))}
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "id": user.id,
                "email": user.email,
                "token": token.key
            }
            return Response(data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']

    @swagger_auto_schema(
        operation_description='Search users by email or name',
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Keyword to search users", type=openapi.TYPE_STRING)
        ],
        responses={200: UserSerializer(many=True)}
    )
    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        queryset = User.objects.filter(
            Q(email__iexact=search_query) | Q(name__icontains=search_query)
        ).exclude(id=self.request.user.id)
        return queryset

class RateThrottle(throttling.UserRateThrottle):
    rate = '3/min'

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [RateThrottle]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @swagger_auto_schema(
        operation_description='Send a friend request to another user',
        responses={201: FriendRequestSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class FriendRequestAcceptView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Accept a friend request',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: openapi.Response(description='Friend request accepted', schema=FriendRequestSerializer)}
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        friend_request = FriendRequest.objects.filter(from_user_id=user_id, to_user=request.user, status='pending').first()
        if friend_request:
            friend_request.status = 'accepted'
            friend_request.save()
            request.user.friends.add(friend_request.from_user)
            serializer = self.get_serializer(friend_request)
            return Response(serializer.data)
        return Response({'error': 'Invalid friend request'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestRejectView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Reject a friend request',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: openapi.Response(description='Friend request rejected', schema=FriendRequestSerializer)}
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        friend_request = FriendRequest.objects.filter(from_user_id=user_id, to_user=request.user, status='pending').first()
        if friend_request:
            friend_request.status = 'rejected'
            friend_request.save()
            serializer = self.get_serializer(friend_request)
            return Response(serializer.data)
        return Response({'error': 'Invalid friend request'}, status=status.HTTP_400_BAD_REQUEST)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='List friends of the authenticated user',
        responses={200: UserSerializer(many=True)}
    )
    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(friends=self.request.user)

class PendingFriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='List pending friend requests received by the authenticated user',
        responses={200: FriendRequestSerializer(many=True)}
    )
    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')