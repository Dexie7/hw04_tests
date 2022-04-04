from django.test import TestCase

from. import constants as c


class RoutesTest(TestCase):
    def test_routes(self):
        routes_and_urls = [
            [c.INDEX_URL, '/'],
            [c.NEW_URL, '/create/'],
            [c.PROFILE_URL, f'/profile/{c.AUTHOR}/'],
            [c.GROUP_URL, f'/group/{c.GROUP_SLUG}/'],
            [c.POST_URL, f'/posts/{c.POST_ID}/'],
            [c.EDIT_URL, f'/posts/{c.POST_ID}/edit/']
        ]
        for route, url in routes_and_urls:
            self.assertEqual(route, url)
