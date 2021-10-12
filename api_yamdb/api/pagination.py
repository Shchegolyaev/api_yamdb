from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    page_size = 10


class CommentsPagination(PageNumberPagination):
    page_size = 10
