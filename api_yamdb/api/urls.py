from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, SignUp, TitleViewSet, UsersViewSet,
                    get_token)

router = DefaultRouter()
router = routers.DefaultRouter()
router.register(r"users", UsersViewSet)
router.register(r"v1/users/me/", UsersViewSet)
router.register(r"users/<str:username>/", UsersViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentsViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view()),
    path('v1/auth/token/', get_token, name='gettoken'),
    path("v1/", include(router.urls)),
]
