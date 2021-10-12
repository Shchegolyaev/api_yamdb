from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentsViewSet
from rest_framework import routers
from .views import SignUp, get_token, UsersViewSet, get_update_me, CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'users/<str:username>/', UsersViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', get_token),
    path('v1/users/me/', get_update_me),
    path('v1/', include(router.urls)),
]
