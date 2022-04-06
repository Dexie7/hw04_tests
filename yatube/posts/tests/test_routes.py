from django.test import TestCase
from django.urls import reverse


AUTHOR = 'user_test'
AUTHOR_2 = 'user_test_2'
POST_TEXT = 'Тестовый тест'
POST_ID = '1'
GROUP_TITLE = 'Тестовый заголовок'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Описание тестовой группы'
INDEX_URL = reverse('posts:index')
NEW_URL = reverse('posts:post_create')
GROUP_URL = reverse('posts:group_list', kwargs={'slug': GROUP_SLUG})
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])
POST_URL = reverse('posts:post_detail', kwargs={'post_id': POST_ID})
EDIT_URL = reverse('posts:post_edit', kwargs={'post_id': POST_ID})

routes_and_urls = [
    [INDEX_URL, '/'],
    [NEW_URL, '/create/'],
    [PROFILE_URL, f'/profile/{AUTHOR}/'],
    [GROUP_URL, f'/group/{GROUP_SLUG}/'],
    [POST_URL, f'/posts/{POST_ID}/'],
    [EDIT_URL, f'/posts/{POST_ID}/edit/']
]


class RoutesTest(TestCase):
    def test_routes(self):
        for route, url in routes_and_urls:
            self.assertEqual(route, url)
