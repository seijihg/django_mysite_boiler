from .serializers import UserSerializer
from .models import ExtendedUser

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import datetime
import os
import jwt

# Create your views here.


@api_view(["GET"])
# Make API public.
@permission_classes([AllowAny])
@authentication_classes([])
def users_list(request):
    if request.method == 'GET':

        user = ExtendedUser.objects.get(pk=request.token["id"])
        if user.is_staff:
            users = ExtendedUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        return Response({"error": "Access denied."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if request.method == 'POST':
        try:
            if serializer.is_valid():
                serializer.save()
                encoded = jwt.encode({"id": serializer.data["id"], "email": serializer.data["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, os.environ.get(
                    "JWTKEY"), algorithm="HS256")
                return Response({**serializer.data, "token": encoded}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as error:
            print("Catch KeyError:", error)
            return Response({"error": "Keyerror"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def change_user(request, id):
    decoded_user_id = request.token["id"]

    try:
        user = ExtendedUser.objects.get(pk=id)
        decoded_user = ExtendedUser.objects.get(pk=decoded_user_id)
    except ExtendedUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)

    # Check if user is staff to have access to all users.
    if decoded_user.is_staff:
        if request.method == 'GET':
            return Response(serializer.data)

    # User has access only to himself
    if decoded_user_id == user.id:
        if request.method == 'GET':
            return Response(serializer.data)
    else:
        return Response({"error": "Something went wrong."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def log_in_user(request):
    try:
        user = ExtendedUser.objects.get(email=request.data["email"])
        if user.check_password(request.data["password"]):
            encoded = jwt.encode({"id": user.id, "email": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)}, os.environ.get(
                "JWTKEY"), algorithm="HS256")
            return Response({"id": user.id, "email": user.email, "user_name": user.user_name, "token": encoded}, status=status.HTTP_200_OK)

        return Response({"error": "Email or password is wrong"}, status=status.HTTP_404_NOT_FOUND)

    except ExtendedUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
