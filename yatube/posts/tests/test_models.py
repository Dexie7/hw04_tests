from django.test import TestCase

from ..models import Group, Post, User



class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_names(self):
        expected_group_title = self.group.title
        self.assertEqual(str(self.group), expected_group_title)
        expected_post_title = self.post.text[:15]
        self.assertEqual(str(self.post), expected_post_title)

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        field_help_text = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, expected_value
                )
