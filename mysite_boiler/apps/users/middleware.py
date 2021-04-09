from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
import jwt
import os


def check_path(str_word, path_arr):
    if str_word in path_arr:
        return True
    else:
        return False


def user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        path_splitted = list(filter(None, request.path.split("/")))
        print(path_splitted)

        # Route needs to match the below.
        if request.method == "GET" and (check_path("users", path_splitted) or check_path("user", path_splitted)):
            try:
                auth_header = request.META["HTTP_AUTHORIZATION"]
                token = auth_header.split(" ")[-1]
                jwt.decode(token, os.environ.get(
                    "JWTKEY"), algorithms="HS256")
            except KeyError as error:
                print("Catch KeyError:", error)
                return JsonResponse({"error": "Not Authenticated."}, status=401)
            except jwt.InvalidSignatureError as error:
                print("Signature Error:", error)
                return JsonResponse({"error": str(error)}, status=401)
            except jwt.ExpiredSignatureError as error:
                print("Signature Error:", error)
                return JsonResponse({"error": str(error)}, status=401)
            except Exception as error:
                print("Error type:", type(error))
                return JsonResponse({"error": "Something went wrong. Contact administrator."}, status=400)

        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
