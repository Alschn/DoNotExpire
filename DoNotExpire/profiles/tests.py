from django.contrib.auth.models import User
from django.test import TestCase

from DoNotExpire.manager.models import Account, Character
from DoNotExpire.profiles.models import Profile


class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            'TestUser', email='testuser@tested.com', password='testing')
        cls.acc1 = Account.objects.create(
            name="TestAcc", profile=cls.user.profile, realm="Asia")
        cls.acc2 = Account.objects.create(
            name="TestAcc2", profile=cls.user.profile, realm="Europe")
        cls.acc3 = Account.objects.create(
            name="TestAcc3", profile=cls.user.profile, realm="US West")
        cls.char1 = Character.objects.create(
            name="TestChar1", level=99, char_class="Barbarian", acc=cls.acc1)
        cls.char2 = Character.objects.create(
            name="TestChar2", level=60, char_class="Paladin", acc=cls.acc1)
        cls.char3 = Character.objects.create(
            name="TestChar3", level=15, char_class="Sorceress", acc=cls.acc2)
        cls.char4 = Character.objects.create(
            name="TestChar4", level=99, char_class="Amazon", acc=cls.acc2)
        cls.char5 = Character.objects.create(
            name="TestChar5", level=90, char_class="Amazon", acc=cls.acc2)
        cls.char6 = Character.objects.create(
            name="TestChar6", level=15, char_class="Sorceress", acc=cls.acc2)

    def test_profile_is_created_with_user(self):
        """Tests signals.py - whether profile was created with a user."""
        profile_query = Profile.objects.filter(user=self.user)
        self.assertTrue(profile_query.exists())
        self.assertTrue(self.user.profile)
        self.assertEqual(profile_query[0], self.user.profile)

    def test_profile_get_all_accounts(self):
        profile = self.user.profile
        actual = Account.objects.filter(profile=profile)
        expected = profile.get_all_accounts()
        self.assertQuerysetEqual(actual, expected)

    def test_profile_get_accounts_count(self):
        profile = self.user.profile
        accounts_count = profile.get_all_accounts().count()
        self.assertEqual(accounts_count, 3)

    def test_profile_get_all_characters(self):
        chars = self.user.profile.get_all_characters()
        queryset = Character.objects.all()
        self.assertQuerysetEqual(chars, queryset)

    def test_profile_get_all_expired_characters(self):
        expired = self.user.profile.get_all_expired_characters()
        self.assertEqual(expired.count(), 0)
        self.char6.expired = True
        self.char6.save(update_fields=['expired'])
        expired = self.user.profile.get_all_expired_characters()
        self.assertEqual(expired.count(), 1)
        self.assertEqual(expired.first(), self.char6)

    def test_profile_get_all_characters_count(self):
        chars = self.user.profile.get_all_characters()
        count = self.user.profile.get_all_characters_count()
        self.assertEqual(chars.count(), count)
        self.assertEqual(count, 6)

    def test_profile_accounts_are_your_own(self):
        """This test proves that those methods work on related objects,
        Not all objects in database."""
        user2 = User.objects.create_user(
            'SecondUser', email='user2@tested.com', password='testing')
        acc = Account.objects.create(
            name="Test", profile=user2.profile, realm="Asia")
        accounts = user2.profile.get_all_accounts()
        queryset = Account.objects.filter(profile=user2.profile)
        self.assertEqual(accounts.count(), 1)
        self.assertEqual(accounts.first(), acc)
        self.assertEqual(queryset.first(), acc)
