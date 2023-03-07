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


class NewUserRegistrationSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']
