import django_filters
from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(method="tag_filter")
    author = django_filters.CharFilter(method="author_filter")
    favorited = django_filters.CharFilter(
        field_name="favorites",
        method="favorited_filter",
        label="Are the articles favorited",
    )
    limit = django_filters.NumberFilter(method="limit_filter")
    offset = django_filters.NumberFilter(method="offset_filter")

    class Meta:
        model = Article
        fields = ["tag", "author", "favorited", "limit", "offset"]

    def tag_filter(self, queryset, name, value):
        return queryset.filter(tags__name__in=[value])

    def author_filter(self, queryset, name, value):
        return queryset.filter(author__name__icontains=value)

    def favorited_filter(self, queryset, name, value):
        return queryset.filter(favorites__name__icontains=value)

    def limit_filter(self, queryset, name, value):
        return queryset[:value]

    def offset_filter(self, queryset, name, value):
        return queryset[value:]
