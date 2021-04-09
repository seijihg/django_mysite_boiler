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
        users = ExtendedUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


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
    try:
        user = ExtendedUser.objects.get(pk=id)
        print("User:", user)
    except ExtendedUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
