from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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















