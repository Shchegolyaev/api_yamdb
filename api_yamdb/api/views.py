from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from .serializers import ReviewSerializers, CommentsSerializers
from reviews.models import Review, Comments, Title
from .pagination import CommentsPagination, ReviewPagination
from .permissions import ReviewCommentsPermission

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (ReviewCommentsPermission,)
    pagination_class = ReviewPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        author = self.request.user
        title = get_object_or_404(Title, id=title_id)
        if title.reviews.filter(author=author).exists():
            raise ValidationError(
                detail='Пользователь уже оставил отзыв '
                       'на это произведение.'
            )
        serializer.save(
            author=self.request.user,
            title_id=title
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    permission_classes = (ReviewCommentsPermission,)
    pagination_class = CommentsPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        reviews_id = self.kwargs['review_id']
        review = get_object_or_404(
            Review,
            id=reviews_id,
            title_id=title_id
        )
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        reviews_id = self.kwargs['review_id']
        review = get_object_or_404(
            Review,
            id=reviews_id,
            title_id=title_id
        )
        serializer.save(
            author=self.request.user,
            review_id=review
        )