from django.db import models
from django.db.models import Count, Max, Min
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import Tag
from tinymce.models import HTMLField

from .utils import unique_slug_generator


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    text = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-published_date']

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})

    def save(self):
        if not self.slug:
            self.slug = unique_slug_generator(self)

        super().save()

    def publish(self, user):
        self.published_date = timezone.now()
        self.author = user
        self.save()
        return self

    def __str__(self):
        return self.title


def font_size(self, max_font=28, min_font=12):
    """ Calculate font size for tag based on it's occurrence
    """
    v = Tag.objects.all().annotate(c=Count('post')).filter(c__gt=0).aggregate(Min('c'), Max('c'))
    max_tag, min_tag = v["c__max"], v["c__min"]
    try:
        step = (max_font - min_font) / float(max_tag - min_tag)
    except ZeroDivisionError:
        step = 1
    tag_count = Post.objects.filter(tags__name=self.name).count()
    size = int(min_font + (tag_count - min_tag) * step)

    return size


Tag.f = font_size
