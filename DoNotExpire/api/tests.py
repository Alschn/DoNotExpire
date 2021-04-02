from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient

from DoNotExpire.profiles.models import Profile
from DoNotExpire.manager.models import Account, Character, Equipment


class TestAPIViews(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            'testuser', email='testuser@test.com', password='testing')
        self.user.save()
        self.account = Account.objects.create(
            name="TestAcc", profile=self.user.profile, realm="Europe")
        self.account.save()
        self.character = Character.objects.create(
            name="TestChar", level=90, char_class="Amazon", acc=self.account
        )
        self.character.save()

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def test_is_not_authenticated(self):
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertEqual(response.status_code, 401)

    def test_is_authenticated(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertNotEqual(response.status_code, 403)

    def test_is_char_owner_permission(self):
        user = User.objects.create_user(
            'sus', email='sus@test.com', password='testing123')
        user.save()
        self.client.login(username="sus", password="testing123")
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertEqual(response.status_code, 403)

    def test_get_equipment_char_not_exists(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.get(f'/api/chars/{test_charname}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, {'Error': f"Character {test_charname} not found!"})

    def test_get_equipment_which_does_not_exist(self):
        char_wout_eq = Character.objects.create(
            name="TestChar2", level=91, char_class="Paladin", acc=self.account
        )
        Equipment.objects.get(char=char_wout_eq).delete()

        self._require_login()
        response = self.client.get(f'/api/chars/{char_wout_eq.name}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, {
                'Error': f"{char_wout_eq.name}'s equipment not found!"}
        )

    def test_get_equipment(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertEqual(response.status_code, 200)
        data = response.data
        fields = [field.name for field in Equipment._meta.get_fields()]
        self.assertEqual(
            first=sorted(list(data.keys())),
            second=sorted(fields)
        )

    def test_update_equipment_but_char_does_not_exist(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.post(f'/api/equipments/{test_charname}')
        self.assertEqual(response.status_code, 404)

    def test_update_equipment_but_it_does_not_exist(self):
        self._require_login()
        char_wout_eq = Character.objects.create(
            name="TestChar3", level=92, char_class="Sorceress", acc=self.account
        )
        Equipment.objects.get(char=char_wout_eq).delete()
        response = self.client.post(f'/api/equipments/{char_wout_eq.name}')
        self.assertEqual(response.status_code, 404)

    # def test_update_equipment(self):
    #     self._require_login()
    #     response = self.client.post(f'/api/equipments/{self.character.name}')
