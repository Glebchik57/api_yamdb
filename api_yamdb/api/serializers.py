from rest_framework.relations import SlugRelatedField
from rest_framework import serializers

from reviews.models import User, Review, Comment, Titles, Categories, Genres


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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlePostPatchSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = Review.objects.filter(title__id=obj.id).annotate(
            avg_rating=Avg('score'))
        return rating

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'genre', 'category')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'
