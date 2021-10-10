from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"categories", views.CategoryViewSet)
router.register(r"genres", views.GenreViewSet)
router.register(r"titles", views.TitleViewSet, basename="titles")

urlpatterns = [
    path("v1/", include(router.urls)),
]
