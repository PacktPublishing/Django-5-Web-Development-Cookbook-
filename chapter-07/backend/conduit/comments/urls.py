from comments import views
from django.urls import path

urlpatterns = [
    path(
        "articles/<str:slug>/comments/",
        views.CommentView.as_view(),
        name="comment-article",
    ),
    path(
        "articles/<str:slug>/comments/<int:id>",
        views.DeleteCommentView.as_view(),
        name="comment-delete",
    ),
    path(
        "add/<int:article_id>/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "edit/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "delete/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
]
