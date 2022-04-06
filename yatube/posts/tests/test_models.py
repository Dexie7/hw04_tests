from django.test import TestCase

from ..models import Group, Post, User


AUTHOR = 'user_test'
POST_TEXT = 'Тестовый тест'
GROUP_TITLE = 'Тестовый заголовок'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Описание тестовой группы'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)

        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
        )

    def test_models_have_correct_object_names(self):
        self.assertEqual(str(self.group), self.group.title)
        self.assertEqual(str(self.post), self.post.text[:15])

    def test_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_help_text(self):
        post = PostModelTest.post
        field_help_text = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )
