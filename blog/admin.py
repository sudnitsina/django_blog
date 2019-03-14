from django.contrib import admin
from django.utils.html import format_html

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ("title", "slug", "created_date", "published_date", "tag_list")
    list_filter = ("published_date", "tags")
    search_fields = ("title",)

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return format_html(
            ", ".join(
                "<a href='?tags__id__exact={}'>{}</a>".format(o.id, o.name)
                for o in obj.tags.all()
            )
        )
