from reviews.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'You can`t use "me"'
            )
        return value

    def validate_role(self, value):
        if value in ['admin', 'user', 'moderator']:
            return value
        raise serializers.ValidationError(
            'There is no such role'
        )


class NewUserRegistrationSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = (
            'username', 'email',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            'username', 'confirmation_code',
        )
        model = User
