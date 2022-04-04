from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from. import constants as c


AUTH = reverse('login')
FAKE_PAGE = '/fake/page'


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.some_user = User.objects.create_user(username='someuser')
        cls.user = User.objects.create_user(username=c.AUTHOR)
        cls.group = Group.objects.create(
            title=c.GROUP_TITLE,
            description=c.GROUP_DESC,
            slug=c.GROUP_SLUG
        )
        cls.post = Post.objects.create(
            text='a' * 20,
            author=cls.user
        )
        cls.VIEW_POST = reverse(
            'posts:post_detail',
            kwargs={
                'post_id': cls.post.id}
        )
        cls.POST_EDIT = reverse(
            'posts:post_edit',
            kwargs={
                'post_id': cls.post.id}
        )
        cls.redirects_urls = {
            '/create/':
                '/auth/login/?next=/create/',
            f'/posts/{cls.post.pk}/edit/':
                f'/auth/login/?next=/posts/{cls.post.pk}/edit/'
        }

    def setUp(self):
        self.guest = Client()
        self.author = Client()
        self.author.force_login(self.user)
        self.another = Client()
        self.another.force_login(self.some_user)

    def test_pages_codes(self):
        """Страницы доступны любому пользователю."""
        SUCCESS = 200
        REDIRECT = 302
        NOT_FOUND = 404
        url_names = [
            [self.author, c.NEW_URL, SUCCESS],
            [self.author, self.POST_EDIT, SUCCESS],
            [self.another, self.POST_EDIT, REDIRECT],
            [self.guest, c.INDEX_URL, SUCCESS],
            [self.guest, c.NEW_URL, REDIRECT],
            [self.guest, self.POST_EDIT, REDIRECT],
            [self.guest, c.GROUP_URL, SUCCESS],
            [self.guest, c.PROFILE_URL, SUCCESS],
            [self.guest, self.VIEW_POST, SUCCESS],
            [self.guest, FAKE_PAGE, NOT_FOUND]
        ]
        for client, url, code in url_names:
            with self.subTest(url=url):
                self.assertEqual(code, client.get(url).status_code)

    def test_redirect(self):
        """Перенаправление пользователя."""
        for address, redirect in self.redirects_urls.items():
            with self.subTest(address=address):
                response = self.guest.get(address)
                self.assertEqual(self.guest.get(address).status_code, HTTPStatus.FOUND)
                self.assertRedirects(self.guest.get(address), redirect)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            c.INDEX_URL: 'posts/index.html',
            c.NEW_URL: 'posts/create_post.html',
            c.GROUP_URL: 'posts/group_list.html',
            c.PROFILE_URL: 'posts/profile.html',
            self.VIEW_POST: 'posts/post_detail.html',
            self.POST_EDIT: 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    self.author.get(url),
                    template
                )
