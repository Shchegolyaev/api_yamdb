from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import ListCreateDestroyAPIView
from .pagination import CommentsPagination, ReviewPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, ReviewCommentsPermission
from .serializers import (
    CategorySerializer,
    CommentsSerializers,
    GenreSerializer,
    MeSerializer,
    ReviewSerializers,
    SingUpSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
    TokenSerializer,
    UserSerializer,
)
from .utils import sent_verification_code
from reviews.models import Category, Genre, Review, Title, User


class SignUp(APIView):
    permission_classes = [AllowAny]
    serializer_class = SingUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if not User.objects.filter(
            username=serializer.validated_data["username"]
        ).exists():
            user = serializer.validated_data
            sent_verification_code(user)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        else:
            user = get_object_or_404(
                User, username=serializer.validated_data["username"]
            )
            sent_verification_code(user)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )


@api_view(["POST"])
@permission_classes([AllowAny, ])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    confirmation_code = serializer.data["confirmation_code"]
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(request.user)
        return Response(f"token: {token}", status=status.HTTP_200_OK)
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

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = MeSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = MeSerializer(request.user)
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
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializerGet
        return TitleSerializerPost


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
        title = get_object_or_404(Title, id=title_id)
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
