from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    def setup(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmai.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title='A good Title',
            body='What do you feel like writing today',
            author=self.user
        )

    def test_string_representation(self):
        post = Post(title='A simple good Title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good Title')
        self.assertEqual(f'{self.post.body}', 'testuser')
        self.assertEqual(f'{self.post.author}', 'NIce body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_views(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_details.html')