from rest_framework import serializers
<<<<<<< HEAD
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comments, Title
from reviews.models import User, Token
from django.contrib.auth.tokens import default_token_generator


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("me - недопустимый username")
        return data


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)[0]

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("me - недопустимый username")
        return data


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

        def validate_username(self, value):
            if not User.objects.filter(username=value).exists():
                raise serializers.ValidationError("Пользователь не найден")
            return value

        def validate(self, data):
            if not default_token_generator.check_token(data['username'],
                                                       data['confirmation_code']):
                raise serializers.ValidationError("Код подтверждения не верен")
            return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class ReviewSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if 1 <= data['score'] <= 10:
            return data
        raise serializers.ValidationError(
            'Рейтинг должен быть от 1 до 10.')


# class ReviewSerializers(serializers.ModelSerializer):
#     author = SlugRelatedField(
#         slug_field='username',
#         default=serializers.CurrentUserDefault(),
#         read_only=True,
#     )
#     # title_id = serializers.PrimaryKeyRelatedField(
#     #     read_only=True,
#     #     required=False
#     # )
#     title_id = SlugRelatedField(
#             slug_field='id',#1
#             #queryset=Title.objects.all(),
#             #read_only=True,
#             required=False,
#             read_only=True, #1
#             #write_only=True,
#             default=None #1
#     )
#
#     class Meta:
#         fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
#         model = Review
#         read_only_fields = ('title_id',)
#         # validators = [
#         #     UniqueTogetherValidator(
#         #         queryset=Review.objects.all(),
#         #         fields=('title_id', 'author',),
#         #         message='Пользователь уже оставил отзыв на это произведение.'
#         #     )
#         # ]

    # def validate(self, data):
    #     if 1 <= data['score'] <= 10:
    #         return data
    #     raise serializers.ValidationError(
    #             'Рейтинг должен быть от 1 до 10.')


class CommentsSerializers(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments

