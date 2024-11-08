from articles import views
from config import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

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
    path("", views.ArticleListView.as_view(), name="article-list"),
    path("search/", views.search_articles, name="article-search"),
    path("ranking/", views.ranked_articles, name="ranking"),
    path("latest_comments/", views.latest_comments, name="latest_comments"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
