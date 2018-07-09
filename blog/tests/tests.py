from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class BlogTest(TestCase):
    fixtures = ["blog/tests/test_data.json"]

    def test_list(self):
        url = reverse('post_list')
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/post_list.html')
        self.assertContains(res, 'Testing tools')

    def test_create_post(self):
        # create new post
        self.client.force_login(User.objects.get_or_create(username='tester')[0])
        url = reverse('post_new')
        res = self.client.post(url, {'title': 'Posting test', 'text': "Some text"})
        self.assertRedirects(res, '/post/3/')

        # check created post
        url = reverse('post_detail', kwargs={"pk": 3})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/post_detail.html')
        self.assertContains(res, 'Posting test')

    def test_create_post_unauthorised(self):
        # create new post without authorisation
        url = reverse('post_new')
        res = self.client.post(url, {'title': 'Posting test', 'text': "Some text"})
        # print(res.content.decode())
        self.assertRedirects(res, '/admin/login/?next=/new/')

        # check post is not created
        url = reverse('post_detail', kwargs={"pk": 3})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 404)

    def test_delete_post(self):
        # delete post
        self.client.force_login(User.objects.get_or_create(username='tester')[0])
        url = reverse('post_detail', kwargs={"pk": 2})
        res = self.client.post(url, {'action': 'delete'})
        self.assertRedirects(res, '/')

        # check post is deleted
        url = reverse('post_detail', kwargs={"pk": 2})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 404)

    def test_delete_post_unauthorised(self):
        # delete post without authorisation
        url = reverse('post_detail', kwargs={"pk": 2})
        res = self.client.post(url, {'action': 'delete'})
        self.assertRedirects(res, '/admin/login/?next=/post/2')

        # check post is not deleted
        url = reverse('post_detail', kwargs={"pk": 2})
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
        self.assertContains(res, 'Testing tools')


class BlogAppearanceTest(TestCase):

    def test_empty_list(self):
        url = reverse('post_list')
        res = self.client.get(url)
        self.assertContains(res, 'Ничего не найдено')


class SidePanelTest(TestCase):
    TEMPLATE = Template("{% load side_panel %}{% last_posts %}")

    def test_empty(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn('В блоге еще нет записей', rendered)

    def test_many_posts(self):
        user = User.objects.get_or_create(username='tester')[0]
        for n in range(6):
            Post(author=user, title="Post #{0}".format(n)).publish()
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("Post #5", rendered)
        self.assertNotIn("Post #6", rendered)
