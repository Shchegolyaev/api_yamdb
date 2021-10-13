from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category, Comment, Genre, Review, Title, Token,
                            User)


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


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return value

    def validate(self, data):
        if not default_token_generator.check_token(
            data["username"], data["confirmation_code"]
        ):
            raise serializers.ValidationError("Код подтверждения не верен")
        return data


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
        if 1 <= data["score"] <= 10:
            return data
        raise serializers.ValidationError("Рейтинг должен быть от 1 до 10.")


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
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


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
