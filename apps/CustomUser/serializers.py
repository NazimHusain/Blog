from rest_framework import serializers
from typing import Any, Union
from apps.CustomUser import models as UserModels
from config.exceptions import CustomValidation

class UserLoginSerializer(serializers.Serializer):
    """Serializer for User's login."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self: 'UserLoginSerializer', attrs: dict) -> Union[dict, CustomValidation]:
        username = attrs["username"]
        password = attrs["password"]
        self.user = UserModels.User.objects.filter(email=username, is_active=True).first()
        if self.user and self.user.check_password(password):
            return attrs
        else:
            raise CustomValidation("Invalid Credentials", 400)
        



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModels.Tag

        fields = ("id","name")

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = UserModels.Post
        fields = ("id","title","content", "tags")
        