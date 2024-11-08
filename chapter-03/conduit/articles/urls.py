from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles import views

router = DefaultRouter(trailing_slash=False)
router.register("articles", views.ArticleViewSet, basename="articles")
router.register("tags", views.TagView)

urlpatterns = [
    path("", include(router.urls)),
]
