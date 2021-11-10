from .models import Comment, Reviews, Titles, Genres, Categories, User
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')
        model = User


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Categories


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.FloatField(
        source='reviews_title__score__avg', read_only=True
    )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(),
                                            slug_field='slug',
                                            required=False)
    genre = serializers.SlugRelatedField(queryset=Genres.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'title_id', 'author', 'text', 'score', 'pub_date')
        model = Reviews

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Reviews.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже писали отзыв к данному произведению'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
