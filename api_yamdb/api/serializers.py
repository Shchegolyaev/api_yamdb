from rest_framework import serializers
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
