from django.test import TestCase
from django.urls import reverse

from posts.models import Post, User


INDEX = reverse('posts:index')
NEW_POST = reverse('posts:post_create')


class RoutesTest(TestCase):
    def test_routes(self):
        user = User.objects.create_user(username='testuser')
        group_slug = 'test-slug'
        post = Post.objects.create(
            text='Тестовый пост',
            author=user
        )
        PROFILE = reverse(
            'posts:profile',
            kwargs={'username': user.username}
        )
        GROUP_POSTS = reverse(
            'posts:group_list',
            kwargs={'slug': group_slug}
        )
        VIEW_POST = reverse(
            'posts:post_detail',
            kwargs={
                'post_id': post.id}
        )
        POST_EDIT = reverse(
            'posts:post_edit',
            kwargs={
                'post_id': post.id}
        )
        routes_and_urls = [
            [INDEX, '/'],
            [NEW_POST, '/create/'],
            [PROFILE, f'/profile/{user.username}/'],
            [GROUP_POSTS, f'/group/{group_slug}/'],
            [VIEW_POST, f'/posts/{post.id}/'],
            [POST_EDIT, f'/posts/{post.id}/edit/']
        ]
        for route, url in routes_and_urls:
            self.assertEqual(route, url)
