import django_filters
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from .models import Comment


class CommentFilter(FilterSet):
    post = django_filters.NumberFilter(lookup_expr="exact", required=False)
    author = django_filters.NumberFilter(lookup_expr="exact", required=False)

    class Meta:
        model = Comment
        fields = ["post", "author"]

    def filter_queryset(self, queryset):
        if self.request:
            post_id: Request = self.request.queryparams.get("post_id")
            author_id: Request = self.request.queryparams.get("author_id")

            if not (post_id and author_id):
                raise ValidationError("No post_id")

            return super().filter_queryset(queryset)
