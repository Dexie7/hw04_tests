from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User


AUTHOR = 'user_test'
POST_TEXT = 'Тестовый тест'
GROUP_TITLE = 'Тестовый заголовок'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Описание тестовой группы'
NEW_URL = reverse('posts:post_create')
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION
        )
        cls.new_group = Group.objects.create(
            title='Заголовок_новый',
            slug='test_slug_new',
            description='текстовое поле'
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
            group=cls.group
        )
        cls.EDIT_URL = reverse('posts:post_edit',
                               kwargs={'post_id': cls.post.id})
        cls.POST_URL = reverse('posts:post_detail',
                               kwargs={'post_id': cls.post.id})

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_creat_new_post(self):
        post_count = Post.objects.count()
        posts = set(Post.objects.all())
        form_data = {
            'text': 'test_text',
            'group': self.group.id,
        }
        response_post = self.authorized_client.post(
            NEW_URL,
            data=form_data,
            follow=True
        )
        posts = set(Post.objects.all()) - posts
        self.assertRedirects(response_post, PROFILE_URL)
        self.assertEqual(len(posts), 1)
        post = posts.pop()
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(
            len([post.id for post in response_post.context['page_obj']]),
            post_count + 1
        )

    def test_change_post(self):
        new_group = Group.objects.create()
        form_data = {
            'text': 'new_text',
            'group': new_group.id,
        }
        response = self.authorized_client.post(
            self.EDIT_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.POST_URL)
        post = response.context['post']
        self.assertEqual(post.id, self.post.id)
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.post.author)
