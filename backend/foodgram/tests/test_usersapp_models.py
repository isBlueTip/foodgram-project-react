from django import test
from django.db.utils import IntegrityError

from tests import fixtures
from users.models import ADMIN, USER, Subscription, User


class UserFixtures(test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create(
            first_name=fixtures.user_1_first_name,
            last_name=fixtures.user_1_last_name,
            username=fixtures.user_1_username,
            email=fixtures.user_1_email,
            role=USER,
        )
        cls.user_2 = User.objects.create(
            first_name=fixtures.user_2_first_name,
            last_name=fixtures.user_2_last_name,
            email=fixtures.user_2_email,
            role=ADMIN,
        )


class UserModelTest(UserFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_object_fields(self):
        user_1 = UserModelTest.user_1
        expected_values = {
            "first_name": fixtures.user_1_first_name,
            "last_name": fixtures.user_1_last_name,
            "username": fixtures.user_1_username,
            "email": fixtures.user_1_email,
            "role": USER,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(user_1, field), expected_value)

        expected_object_name = fixtures.user_1_first_name[:32]
        expected_object_verbose = "пользователь"
        expected_object_verbose_plural = "пользователи"
        self.assertEqual(expected_object_name, str(user_1))
        self.assertEqual(expected_object_verbose, user_1._meta.verbose_name)
        self.assertEqual(
            expected_object_verbose_plural, user_1._meta.verbose_name_plural
        )


class SubscriptionModelTest(UserFixtures):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subscription_1 = Subscription.objects.create(
            follower=cls.user_1,
            author=cls.user_2,
        )

    def test_object_fields(self):
        user_1 = SubscriptionModelTest.user_1
        user_2 = SubscriptionModelTest.user_2
        subscription_1 = SubscriptionModelTest.subscription_1

        expected_values = {
            "follower": user_1,
            "author": user_2,
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(subscription_1, field),
                                 expected_value)

        expected_object_verbose = "избранное"
        expected_object_verbose_plural = "избранные"
        self.assertEqual(expected_object_verbose,
                         subscription_1._meta.verbose_name)
        self.assertEqual(expected_object_verbose_plural,
                         subscription_1._meta.verbose_name_plural)

    def test_unique_subscription(self):
        with self.assertRaises(IntegrityError):
            Subscription.objects.create(
                follower=SubscriptionModelTest.user_1,
                author=SubscriptionModelTest.user_2,
            )
