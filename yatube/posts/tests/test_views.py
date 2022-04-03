import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from posts.settings import POSTS_ON_PAGE

INDEX = reverse('posts:index')
NEW_POST = reverse('posts:post_create')

POST_TEST_TEXT = "Ж" * 50
URL_404 = "404/"


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title="Тест-название",
                                         slug='test_slug',
                                         description="Тест-описание")
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        # первый клиент автор поста
        self.guest_client = Client()
        self.user = User.objects.create_user(username='IvanovI')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.username = self.user.username
        # второй клиент не автор поста
        self.authorized_client_2 = Client()
        self.user_2 = User.objects.create_user(username='PetrovP')
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(self.user_2)
        self.username_2 = self.user_2.username

        # создание поста
        self.post = Post.objects.create(text=POST_TEST_TEXT,
                                        group=self.group,
                                        author=self.user)
        # библиотека юрлов
        self.post_id = self.post.id
        self.slug = self.group.slug
        self.group_page = reverse('posts:group_list', args=[self.slug])
        self.profile_page = reverse('posts:profile', args=[self.username])
        self.post_page = reverse('posts:post_detail', args=[self.post_id])
        self.edit_page = reverse('posts:post_edit', args=[self.post.id])

    # Проверяем контекст
    def test_main_group_pages_shows_correct_context(self):
        """Страница index, group, profile сформированы
        с правильным контекстом."""
        urls = [INDEX, self.group_page, self.profile_page, ]

        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                post = response.context['page_obj'][0]
                self.assertEqual(Post.objects.count(), 1)
                self.assertEqual(POST_TEST_TEXT, post.text)
                self.assertEqual(self.username, post.author.username)
                self.assertEqual(self.group.title, post.group.title)

    def test_slug_pages_shows_correct_context(self):
        """Страница post сформирована с правильным контекстом."""
        url = self.post_page
        response = self.guest_client.get(url)
        post = response.context['post']
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(POST_TEST_TEXT, post.text)
        self.assertEqual(self.username, post.author.username)
        self.assertEqual(self.group.title, post.group.title)
        self.assertEqual(self.group.title, post.group.title)


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(title="Тест-название",
                                          slug='test_slug',
                                          description="Тест-описание")
        author = User.objects.create_user(username='test_user')

        for i in range(0, 9):
            Post.objects.create(text="Ж" * i,
                                group=self.group,
                                author=author)
        slug = self.group.slug
        self.guest_client = Client()
        self.user = User.objects.create_user(username='IvanovI')
        self.group_page = reverse('posts:group_list', args=[slug])

    def test_pages_contain_needed_number_of_records(self):
        '''На стр Paginator отображает нужное количество записей'''
        posts_count = Post.objects.count()
        var: 0 if posts_count // 2 == 0 else var = 1
        number_pages = posts_count // POSTS_ON_PAGE + var
        last_page = posts_count - (POSTS_ON_PAGE * (number_pages - var))
        urls = [
            [INDEX, last_page],
            [self.group_page, last_page],
            [f'{INDEX}?page={number_pages}', last_page],
            [f'{self.group_page}?page={number_pages}', last_page],
        ]
        for url, length in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                len_list = len(response.context.get('page_obj').object_list)
                self.assertEqual(len_list, length)
