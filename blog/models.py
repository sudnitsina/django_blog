from django.db import models
from django.db.models import Count, Max, Min
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import Tag
from tinymce.models import HTMLField


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


def font_size(self):
    max_font = 28
    min_font = 12
    v = Tag.objects.all().annotate(c=Count('post')).filter(c__gt=0).aggregate(Min('c'), Max('c'))
    max_tag, min_tag = v["c__max"], v["c__min"]
    try:
        step = (max_font - min_font)/float(max_tag-min_tag)
    except ZeroDivisionError:
        step = 1
    tag_count = Post.objects.filter(tags__name=self.name).count()
    font = int(min_font + (tag_count-min_tag)*step)
    return font


Tag.f = font_size
