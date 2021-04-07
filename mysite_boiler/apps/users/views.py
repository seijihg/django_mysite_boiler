from .serializers import UserSerializer
from .models import ExtendedUser

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import os

# Create your views here.


@api_view(["GET"])
# Make API public.
@permission_classes([AllowAny])
@authentication_classes([])
def users_list(request):
    print(os.environ.get("FOO"))
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

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as error:
            print("Catch KeyError:", error)
            return Response({"error": "Keyerror"}, status=status.HTTP_400_BAD_REQUEST)
