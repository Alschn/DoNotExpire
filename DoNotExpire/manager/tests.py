from DoNotExpire.manager.models import Account, Character
from django.contrib.auth.models import User
from django.test import TestCase
from .forms import CreateAccountForm, CreateCharacterForm


class RegexValidatorsOnModelFormTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            'TestUser', email='testuser@tested.com', password='testing')

    def test_alphanumeric_too_short_and_forbidden_sign(self):
        acc_form1 = CreateAccountForm({'name': '$', 'realm': 'Asia'})
        self.assertFalse(acc_form1.is_valid())

    def test_alphanumeric_too_short_good_signs(self):
        acc_form2 = CreateAccountForm({'name': '.', 'realm': 'Europe'})
        self.assertFalse(acc_form2.is_valid())

    def test_alphanumeric_forbidden_sign_mixed_with_good(self):
        acc_form3 = CreateAccountForm({'name': '__&ad', 'realm': 'US West'})
        self.assertFalse(acc_form3.is_valid())

    def test_alphanumeric_begins_with_forbidden_sign(self):
        acc_form4 = CreateAccountForm(
            {'name': '^Adamson313', 'realm': 'US East'})
        self.assertFalse(acc_form4.is_valid())

    def test_alphanumeric_too_long(self):
        acc_form5 = CreateAccountForm(
            {'name': 'AaBbCcDdOoPpRrSs', 'realm': 'Europe'})
        self.assertFalse(acc_form5.is_valid())

    def test_alphanumeric_validator_success(self):
        acc_form_1 = CreateAccountForm({'name': '-Ada-son', 'realm': 'Asia'})
        self.assertTrue(acc_form_1.is_valid())

        acc_form_2 = CreateAccountForm({'name': '_adam_', 'realm': 'Asia'})
        self.assertTrue(acc_form_2.is_valid())

        acc_form_3 = CreateAccountForm({'name': 'Adams.on', 'realm': 'Asia'})
        self.assertTrue(acc_form_3.is_valid())

        acc_form_3 = CreateAccountForm({'name': 'Ad-am_s.on', 'realm': 'Asia'})
        self.assertTrue(acc_form_3.is_valid())

    def test_letters_only_validator_fails(self):
        pass

    def test_letters_only_validator_success(self):
        pass


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


class ManagerViewsTests(TestCase):
    pass
