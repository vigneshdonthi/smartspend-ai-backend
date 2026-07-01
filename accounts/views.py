from urllib import request
from httpcore import request

from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status

# Create your views here.
class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully.",
                    "username": serializer.validated_data["username"],
                    "email": serializer.validated_data["email"],
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=400)


class LoginAPIView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=username,password=password)
            if not user:
                return Response({"error":"Invalid credentials."},status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },

                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"error":"Refresh token is required."},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message":"Logout successful."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":"Invalid refresh token."},status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
