from rest_framework import serializers
from .models import ExtendedUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    # This is needed for it to hit create_user in model.
    def create(self, validated_data):
        # Validate password using default Django lib.
        try:
            validate_password(validated_data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e)})

        # if len(validated_data["email"]) < 100:
        #     raise serializers.ValidationError({"email": ["Too short"]})

        user = ExtendedUser.objects.create_user(
            email=validated_data['email'],
            user_name=validated_data['user_name'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = ExtendedUser
        fields = '__all__'
