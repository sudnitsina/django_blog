from django import template
from django.utils import timezone
from blog.models import Post
from taggit.models import Tag
from django.db.models import Count


register = template.Library()


@register.inclusion_tag('blog/last_posts.html')
def last_posts():
    post_list = Post.objects.filter(published_date__lte=timezone.now())[:9]
    cloud = Tag.objects.all().annotate(c = Count('post')).filter(c__gt = 0)
    return {'post_list': post_list, 'cloud': cloud}
