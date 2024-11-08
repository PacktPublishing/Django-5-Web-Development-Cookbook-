import logging

from articles.models import Article
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

from .forms import CommentForm
from .models import Comment
from .serializers import CommentSerializer
import json

logger = logging.getLogger(__name__)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.prefetch_related("author").all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    def post(self, request, slug, *args, **kwargs):
        try:
            logger.debug(f"Create comment for article with slug: {slug}")
            article = Article.objects.get(slug=slug)
            comment_data = request.data.get("comment", {})
            logger.debug(
                f"Create comment with data: {comment_data} on article {article}"
            )

            serializer_context = self.get_serializer_context()
            serializer_context["article"] = article

            serializer = self.get_serializer(
                data=comment_data, context=serializer_context
            )
            logger.debug(f"Serializer: {serializer}")
            serializer.is_valid(raise_exception=True)
            logger.debug(f"Serializer is valid")
            self.perform_create(serializer)
            logger.debug(f"Serializer data: {serializer.data}")

            return Response(
                {"comment": serializer.data}, status=status.HTTP_201_CREATED
            )
        except Article.DoesNotExist:
            return Response(
                {
                    "errors": {
                        "body": ["Article does not exist"],
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {
                    "errors": {
                        "body": ["Bad request: unable to create comment"],
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, slug, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
            comments = Comment.objects.filter(article=article)
            serializer = self.get_serializer(comments, many=True)
            return Response({"comments": serializer.data})
        except Article.DoesNotExist:
            return Response(
                {
                    "errors": {
                        "body": ["Article does not exist"],
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class DeleteCommentView(generics.DestroyAPIView):
    def destroy(self, request, slug, id, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
            comment = Comment.objects.get(id=id, article=article)
            self.perform_destroy(comment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response(
                {
                    "errors": {
                        "body": ["Article does not exist"],
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Comment.DoesNotExist:
            return Response(
                {
                    "errors": {
                        "body": ["Comment does not exist"],
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {
                    "errors": {
                        "body": ["Bad request: unable to delete comment"],
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@require_http_methods(["POST"])
@login_required
def add_comment(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id)
    comment: Comment | None = None

    if (form := CommentForm(request.POST)).is_valid():

        comment = form.save(commit=False)
        comment.author = request.user
        comment.article = article
        comment.save()
        logger.info(f"Comment {comment} created")

        channel_layer = get_channel_layer()
        group_name = f"comments_{article_id}"
        logger.info(f"Send comment to group {group_name}")
        # Convert the comment data to JSON
        comment_data = {
            "id": comment.id,
            "content": comment.content,
            "author_id": comment.author.id,
            "html": json.dumps(
                render_to_string(
                    "comments/_comment.html", {"comment": comment}
                )
            ),
        }

        # Send the comment JSON to the group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "comment_message",
                "comment": comment_data,
            },
        )

        logger.info(
            f"Comment sent to group {group_name} with data: {comment_data}"
        )

        # reset form
        form = CommentForm()

    return TemplateResponse(
        request,
        "comments/_comment_form.html",
        {
            "article": article,
            "form": form,
            "new_comment": comment,
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def edit_comment(request: HttpRequest, comment_id: int) -> HttpResponse:

    comment = get_object_or_404(
        Comment.objects.select_related("author"),
        author=request.user,
        pk=comment_id,
    )

    if request.method == "GET":

        return TemplateResponse(
            request,
            "comments/_comment_form.html",
            {
                "comment": comment,
                "form": CommentForm(instance=comment),
            },
        )

    if (form := CommentForm(request.POST, instance=comment)).is_valid():
        comment = form.save()

        return TemplateResponse(
            request, "comments/_comment.html", {"comment": comment}
        )

    return TemplateResponse(
        request,
        "comments/_comment_form.html",
        {
            "comment": comment,
            "form": form,
        },
    )


@require_http_methods(["DELETE"])
@login_required
def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(
        Comment,
        author=request.user,
        pk=comment_id,
    )
    comment.delete()
    return HttpResponse()
