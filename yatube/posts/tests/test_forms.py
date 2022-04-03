from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Vlad')
        cls.group = Group.objects.create(
            title='Заголовок', 
            slug='test_slug', 
            description='текстовое поле' 
        )
        cls.group_new = Group.objects.create( 
            title='Заголовок_новый', 
            slug='test_slug_new', 
            description='текстовое поле' 

        ) 
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        last_post = Post.objects.last()
        self.assertRedirects(
            response, reverse(
                'posts:profile', 
                kwargs={'username': f'{self.user}'}
            ))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(last_post.text, form_data['text'])
        self.assertEqual(last_post.group.id, form_data['group'])

    def test_change_post(self):
        post_count = Post.objects.count()
        post_edit = Post.objects.get(pk=1)
        form_data = {
            'text': 'Тестовый другой текст',
            'group': self.group_new.id,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={
                    'post_id': post_edit.id,
                }
            ),
            data=form_data,
            follow=True
        )
        post_fin = Post.objects.get(pk=1)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post_fin.text, form_data['text'])
        self.assertEqual(post_fin.group.id, form_data['group'])
        # self.assertTrue( 
        #     Post.objects.filter( 
        #         text='Тестовый тест 2',
        #         group=self.group_new.id 
        #     ).exists()) 
