from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import Post, PostForm
from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Vlad')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
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
            group=cls.group,
            author=cls.user
        )
        cls.form = PostForm()

    def test_create_post(self):
        """Проверка формы создания поста"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': PostFormTest.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': f'{self.user}'}
            ))
        self.assertEqual(
            Post.objects.count(),
            post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=PostFormTest.group.id
            ).exists())

    def test_edit_post(self):
        """Проверка формы редактирования поста"""
        form_data = {
            'text': 'Тестовый тест 2',
            'group': PostFormTest.group_new.id
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.id}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.id}'}
            ))
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый тест 2',
                group=PostFormTest.group_new.id
            ).exists())
        self.assertFalse(
            Post.objects.filter(
                text='Тестовый текст',
                group=PostFormTest.group.id
            ).exists())
