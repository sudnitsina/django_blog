import logging

from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse

from blog.models import Post

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BlogTest(TestCase):
    fixtures = ["blog/tests/test_data.json"]

    def setUp(self):
        logger.info(f"'{self._testMethodName}' testcase started")

    def test_list(self):

        url = reverse("blog:post_list")
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "blog/post_list.html")
        self.assertContains(res, "Testing tools")

    def test_create_post(self):
        # create new post
        self.assertFalse(Post.objects.filter(slug="posting-test").exists())
        self.client.force_login(User.objects.get_or_create(username="tester")[0])
        url = reverse("blog:post_new")
        res = self.client.post(url, {"title": "Posting test", "text": "Some text"})
        self.assertRedirects(res, "/post/posting-test/")

        # check created post
        self.assertTrue(Post.objects.filter(slug="posting-test").exists())

        url = reverse("blog:post_detail", kwargs={"slug": "posting-test"})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "blog/post_detail.html")
        self.assertContains(res, "Posting test")

    def test_create_post_unauthorised(self):
        # create new post without authorisation
        url = reverse("blog:post_new")
        res = self.client.post(url, {"title": "Posting test", "text": "Some text"})
        # print(res.content.decode())
        self.assertRedirects(res, "/admin/login/?next=/new/")

        self.assertFalse(Post.objects.filter(title="Posting test").exists())

    def test_delete_post(self):
        self.assertTrue(Post.objects.filter(slug="testing-tools").exists())
        # delete post
        self.client.force_login(User.objects.get_or_create(username="tester")[0])
        url = reverse("blog:post_detail", kwargs={"slug": "testing-tools"})
        res = self.client.post(url, {"action": "delete"})
        self.assertRedirects(res, "/")

        self.assertFalse(Post.objects.filter(slug="testing-tools").exists())

    def test_delete_post_unauthorised(self):
        # delete post without authorisation
        url = reverse("blog:post_detail", kwargs={"slug": "testing-tools"})
        res = self.client.post(url, {"action": "delete"})
        self.assertRedirects(res, "/admin/login/?next=/post/testing-tools")

        # check post is not deleted
        url = reverse("blog:post_detail", kwargs={"slug": "testing-tools"})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertContains(res, "Testing tools")


class BlogAppearanceTest(TestCase):
    def test_empty_list(self):
        url = reverse("blog:post_list")
        res = self.client.get(url)
        self.assertContains(res, "Ничего не найдено")


class SidePanelTest(TestCase):
    TEMPLATE = Template("{% load side_panel %}{% last_posts %}")

    def test_empty(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("В блоге еще нет записей", rendered)

    def test_many_posts(self):
        user = User.objects.get_or_create(username="tester")[0]
        for n in range(6):
            Post(author=user, title="Post #{0}".format(n)).publish(user)
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("Post #5", rendered)
        self.assertNotIn("Post #6", rendered)


class PaginatorTest(TestCase):
    fixtures = ["blog/tests/test_data.json"]

    def test_one_page(self):
        list_ = Post.objects.all()
        p = Paginator(list_, 5)
        posts = p.page(1)
        self.assertEqual(len(posts), 2)

        p = Paginator(list_, 1)
        posts = p.page(1)
        self.assertEqual(len(posts), 1)
        logging.info(p.page_range)
