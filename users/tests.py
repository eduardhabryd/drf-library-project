from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email="testuser@mail.com", password="password"
        )

        self.assertEqual(user.email, "testuser@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            email="testsuperuser@mail.com", password="password"
        )

        self.assertEqual(admin_user.email, "testsuperuser@mail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str(self):
        user = get_user_model().objects.create_user(
            email="testuser@mail.com", password="password"
        )

        self.assertEqual(str(user), "testuser@mail.com")
