from django.urls import include, path
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentsViewSet

router = DefaultRouter()
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
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
=======
from rest_framework import routers
from .views import SignUp, get_token, UsersViewSet, get_update_me


router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'users/<str:username>/', UsersViewSet)



urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', get_token),
    path('v1/users/me/', get_update_me),
    path('v1/', include(router.urls))
]
>>>>>>> origin/feature/categories_and_genres
