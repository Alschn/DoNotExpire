from django.contrib.auth.models import User
from django.test import TestCase

from manager.models import Account, Character


# to be finished
class ManagerModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            'TestUser', email='testuser@tested.com', password='testing')
        cls.acc = Account.objects.create(
            name="TestAcc3", profile=cls.user.profile, realm="US West")
        cls.char1 = Character.objects.create(
            name="TestChar1", level=99, char_class="Barbarian", acc=cls.acc)
        cls.char2 = Character.objects.create(
            name="TestChar2", level=1, char_class="Paladin", acc=cls.acc)

    def test_acc_get_all_characters(self):
        pass

    def test_acc_get_all_characters_count(self):
        pass

    def test_char_get_class_image(self):
        pass

    def test_char_expires_in(self):
        pass

    def test_equipment_is_created_with_character(self):
        pass
