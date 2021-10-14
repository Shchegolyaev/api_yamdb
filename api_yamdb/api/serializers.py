from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title, User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError("me - недопустимый username")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)[0]

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("me - недопустимый username")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=500)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class ReviewSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if self.context['request'].method == 'PATCH':
            return data
        if title.reviews.filter(author=author).exists():
            raise ValidationError(
                detail="Пользователь уже оставил отзыв " "на это произведение."
            )
        return data


class CommentsSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
