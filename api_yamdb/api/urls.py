from django.urls import include, path
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