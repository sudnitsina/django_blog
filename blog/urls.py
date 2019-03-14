from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.post_list, name="post_list"),
    url(r"^new/$", views.post_new, name="post_new"),
    url(r"^tag/(?P<tag_slug>[\w-]+)/$", views.post_list, name="post_list"),
    url(r"^post/(?P<pk>\d+)/$", views.post_detail_by_id, name="post_detail_by_id"),
    url(r"^post/(?P<slug>[\w-]+)/$", views.post_detail, name="post_detail"),
    url(r"^post/(?P<slug>[\w-]+)/edit/$", views.post_edit, name="post_edit"),
    url(r"^rss/$", views.RSSFeed(), name="rss"),
]
