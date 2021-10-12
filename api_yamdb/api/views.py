from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .pagination import CommentsPagination, ReviewPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, ReviewCommentsPermission
from .serializers import (CategorySerializer, CommentsSerializers,
                          GenreSerializer, MeSerializer, ReviewSerializers,
                          SingUpSerializer, TitleSerializerGet,
                          TitleSerializerPost, TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class ListCreateDestroyAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


def sent_verification_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Код подтверждения",
        f"Ваш код: {confirmation_code}",
        "db_yamdb@example.com",
        [user.email],
        fail_silently=False,
    )


# Доступно всем
class SignUp(APIView):
    permission_classes = [AllowAny]
    serializer_class = SingUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not User.objects.filter(username=request.user.username).exists():
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.instance
            sent_verification_code(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(username=request.user.username).exists():
            user = get_object_or_404(User, username=request.data["username"])
            sent_verification_code(user)
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data["username"])
    if default_token_generator.check_token(
        user, request.data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(
        "Отсутствует обязательное поле или оно некорректно",
        status=status.HTTP_400_BAD_REQUEST,
    )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class UpdateListViewSet(
    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


# Доступно любому авторизированному user
@api_view(["GET", "PATCH"])
def get_update_me(request):
    if request.method == "PATCH":
        me = get_object_or_404(User, username=request.user.username)
        serializer = MeSerializer(me, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    me = get_object_or_404(User, username=request.user.username)
    serializer = MeSerializer(me)
    return Response(serializer.data)


class CategoryViewSet(ListCreateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = ReviewPagination


class GenreViewSet(ListCreateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = [
        "slug",
    ]
    search_fields = ("name",)
    pagination_class = ReviewPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializerGet
        return TitleSerializerPost

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg("reviews__score"))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (ReviewCommentsPermission,)
    pagination_class = ReviewPagination

    def get_queryset(self):
        title_id = self.kwargs["title_id"]
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs["title_id"]
        author = self.request.user
        title = get_object_or_404(Title, id=title_id)
        if title.reviews.filter(author=author).exists():
            raise ValidationError(
                detail="Пользователь уже оставил отзыв " "на это произведение."
            )
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    permission_classes = (ReviewCommentsPermission,)
    pagination_class = CommentsPagination

    def get_queryset(self):
        title_id = self.kwargs["title_id"]
        reviews_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=reviews_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs["title_id"]
        reviews_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=reviews_id, title_id=title_id)
        serializer.save(author=self.request.user, review_id=review)
