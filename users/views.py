from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterUserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserActivity
from .serializers import UserActivitySerializer

# Create your views here.

@swagger_auto_schema(
    method="post",
    operation_description="Register a new user",
    request_body=RegisterUserSerializer,
    responses={201: "User registered successfully", 400: "Bad Request"},
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            return super().post(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
            

@swagger_auto_schema(
    method="post",
    operation_description="Track user activity such as viewed, liked, or skipped content.",
    request_body=UserActivitySerializer,
    responses={
        201: "Activity logged successfully",
        400: "Bad request. Invalid data format.",
        401: "Unauthorized. Authentication required.",
        500: "Internal server error."
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def track_user_activity(request):
    try:
        serializer = UserActivitySerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
            
        serializer.save(user=request.user) 
        return Response({"message": "UserActivity Created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message" : "An Error Occured while trying to create the UserActivity"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)