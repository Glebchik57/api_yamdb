from rest_framework.relations import SlugRelatedField
from rest_framework import serializers

from reviews.models import User, Review



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    
    class Meta:
        fields = '__all__'
        model = Review
