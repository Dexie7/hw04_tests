import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from yatube.settings import MAX_PAGE_COUNT


AUTHOR = 'user_test'
GROUP_TITLE = 'Тестовый заголовок'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Описание тестовой группы'
POST_TEST_TEXT = "Ж" * 50
URL_404 = "404/"
INDEX_URL = reverse('posts:index')
GROUP_URL = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG})
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title=GROUP_TITLE,
                                         slug=GROUP_SLUG,
                                         description=GROUP_DESCRIPTION)
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        # первый клиент автор поста
        self.guest = Client()
        self.user = User.objects.create_user(username=AUTHOR)
        self.author = Client()
        self.author.force_login(self.user)

        # создание поста
        self.post = Post.objects.create(text=POST_TEST_TEXT,
                                        group=self.group,
                                        author=self.user)

    # Проверяем контекст
    def test_main_group_pages_shows_correct_context(self):
        """Страница index, group, profile сформированы
        с правильным контекстом."""
        urls = [INDEX_URL, GROUP_URL, PROFILE_URL]

        for url in urls:
            with self.subTest(url=url):
                response = self.guest.get(url)
                post = response.context['page_obj'][0]
                self.assertEqual(POST_TEST_TEXT, post.text)
                self.assertEqual(self.user.username, post.author.username)
                self.assertEqual(self.group.title, post.group.title)
                self.assertEqual(self.group.description,
                                 post.group.description)

    def test_slug_pages_shows_correct_context(self):
        """Страница post сформирована с правильным контекстом."""
        url = reverse('posts:post_detail', args=[self.post.id])
        response = self.guest.get(url)
        post = response.context['post']
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(POST_TEST_TEXT, post.text)
        self.assertEqual(self.user.username, post.author.username)
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
        self.group_page = reverse('posts:group_list', args=[slug])

    def test_pages_contain_needed_number_of_records(self):
        '''На стр Paginator отображает нужное количество записей'''
        posts_count = Post.objects.count()
        var: 0 if posts_count // 2 == 0 else var = 1
        number_pages = posts_count // MAX_PAGE_COUNT + var
        last_page = posts_count - (MAX_PAGE_COUNT * (number_pages - var))
        urls = [
            [INDEX_URL, last_page],
            [self.group_page, last_page],
            [f'{INDEX_URL}?page={number_pages}', last_page],
            [f'{self.group_page}?page={number_pages}', last_page],
        ]
        for url, length in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                len_list = len(response.context.get('page_obj').object_list)
                self.assertEqual(len_list, length)
