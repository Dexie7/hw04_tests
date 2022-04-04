from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User
from. import constants as c


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=c.AUTHOR)
        cls.group = Group.objects.create(
            title=c.GROUP_TITLE,
            slug=c.GROUP_SLUG,
            description=c.GROUP_DESC
        )
        cls.new_group = Group.objects.create(
            title='Заголовок_новый',
            slug='test_slug_new',
            description='текстовое поле'
        )
        cls.post = Post.objects.create(
            text=c.POST_TEXT,
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
        posts_id = [post.id for post in Post.objects.all()]
        form_data = {
            'text': 'test_text',
            'group': self.group.id,
        }
        response_post = self.authorized_client.post(
            c.NEW_URL,
            data=form_data,
            follow=True
        )
        posts_new_id = [post.id for post in response_post.context['page_obj']]
        list_post_id = list(set(posts_new_id) - set(posts_id))
        self.assertRedirects(response_post, c.PROFILE_URL)
        self.assertEqual(len(list_post_id), 1)
        post = [
            post for post in response_post.context['page_obj']
            if post.id == list_post_id[0]][0]
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(len(posts_new_id), post_count + 1)

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
        self.assertEqual(post.group.id, new_group.id)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.post.author)
