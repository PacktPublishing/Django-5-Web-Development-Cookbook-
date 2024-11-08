from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer
from articles.models import Article
import logging

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
