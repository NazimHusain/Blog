from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotAcceptable
from django.db import DatabaseError
from apps.CustomUser import models as UserModels
from rest_framework.authtoken.models import Token
from apps.Helpers import models as coreModels
from django.contrib.auth import login, logout
from apps.CustomUser import serializers 
from django.db.models import Q
from django.shortcuts import get_object_or_404
from config.pagination import ApiPaginator

pagination_class = ApiPaginator()
# Create your views here.

class SignUp(APIView):
    """Api for Register User."""

    permission_classes = ()
    authentication_classes = ()

    def post(self: "SignUp", request: Request, *args: any, **kwargs: any) -> Response:
        data = request.data
        try:
            if data.get("email"):
                user = UserModels.User.objects.create_user(
                    username=data.get("email"),
                    email=data.get("email"),
                    password=data.get("password"))
                
            token, _ = Token.objects.get_or_create(user=user)
            if data.get("first_name"):
                user.first_name = data.get("first_name")
            if data.get("last_name"):
                user.last_name = data.get("last_name")

            if data.get("role"):
                user.role = coreModels.DropdownValues.objects.get(slug="user-roles")
            if data.get("profilePic"):
                user.profilePic = coreModels.FileUpload.objects.get(id=data.get("profilePic"))
            user.save()

            return Response({"key": token.key}, 201)
        except DatabaseError:
            raise NotAcceptable("Username already exists")
        except Exception as e:
            print(str(e))
            raise NotAcceptable("User could not be created, check the data")


class UserLogin(APIView):
    """Api for Login User.
    username(str) - username of user
    password(str) - password of user
    """

    permission_classes = []

    def post(self: "UserLogin", request: Request, version: str) -> Response:
        data = request.data
        try:
            data["username"]
        except Exception:
            try:
                data["username"] = data["email"]
            except Exception:
                return Response(
                    {
                        "response": "User created but cannot login, please try login manually."
                    },
                    400,
                )
        data["password"] = data.get("password")
        serialized = serializers.UserLoginSerializer(data=data)
        if serialized.is_valid():
            user = serialized.user
            login(request, user)
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            data, success_code = {
                "key": token.key,
                "role": user.role.slug if user.role.slug else None,
                }, 200
            return Response(data, success_code)
        return Response(serialized.errors)
    
    

class UserLogout(APIView):
    """APi for logout."""

    def post(self: "UserLogout", request: Request, version: str) -> Response:
        request.auth.delete()
        logout(request)
        data = {"response": "Log out Successfully"}
        return Response(data=data, status=200)


class TagAPIView(APIView):
    def get(self: "TagAPIView", request:Request,version:str) -> Response:
        tags = UserModels.Tag.objects.all()
        serializer = serializers.TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self: "TagAPIView", request:Request,version:str) -> Response:
        serializer = serializers.TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class PostSearchAPIView(APIView):
    def get(self: "PostSearchAPIView", request:Request,version:str) -> Response:
        query = request.GET.get('q')
        if query:
            post = UserModels.Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            post = UserModels.Post.objects.all()
        result_page = pagination_class.paginate_queryset(post, request)
        serialized = serializers.PostSerializer(result_page, many=True, context={"request": request})
        return pagination_class.get_paginated_response(serialized.data)
    

class PostDetails(APIView):
    def get(self: "TagAPIView", request:Request,postId: int, version:str) -> Response:
        instance = get_object_or_404(UserModels.Post,id=postId)
        serializer = serializers.PostSerializer(instance)
        return Response(serializer.data, 200)
    


    


