from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comments, Title


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
