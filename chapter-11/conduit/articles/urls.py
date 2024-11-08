from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from articles import views
from config import settings

router = DefaultRouter(trailing_slash=False)
router.register("articles", views.ArticleViewSet)
router.register("tags", views.TagView)

urlpatterns = [
    path("api/", include(router.urls)),
    path("articles", views.ArticleListView.as_view(), name="article-list"),
    path(
        "articles/new",
        views.ArticleCreateView.as_view(),
        name="create-article-view",
    ),
    path(
        "articles/<slug:slug>",
        views.ArticleDetailView.as_view(),
        name="article-detail-view",
    ),
    # add favorite article path
    path(
        "article/favorite/<int:article_id>/",
        views.favorite,
        name="favorite",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
