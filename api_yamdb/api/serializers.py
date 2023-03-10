from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Categories, Comment, Genres, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

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


class NewUserRegistrationSerializer(UserSerializer):
    """Сериализатор для самостоятельной регистрации новых пользователей."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для повторной отправки кода на почту
    для существующего пользователя."""
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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, value):
        if self.context['request'].method != 'POST':
            return value
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв этому произведению'
            )
        return value


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=None)

    class Meta:
        model = Title
        fields = '__all__'
