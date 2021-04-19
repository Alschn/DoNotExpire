import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
)
from rest_framework.test import APIRequestFactory, APIClient

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
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_is_authenticated(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertNotEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_is_char_owner_permission(self):
        user = User.objects.create_user(
            'sus', email='sus@test.com', password='testing123')
        user.save()
        self.client.login(username="sus", password="testing123")
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_get_equipment_char_not_exists(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.get(f'/api/chars/{test_charname}')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {'Error': f"Character {test_charname} not found!"})

    def test_get_equipment_which_does_not_exist(self):
        char_wout_eq = Character.objects.create(
            name="TestChar2", level=91, char_class="Paladin", acc=self.account
        )
        Equipment.objects.get(char=char_wout_eq).delete()

        self._require_login()
        response = self.client.get(f'/api/chars/{char_wout_eq.name}')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {
                'Error': f"{char_wout_eq.name}'s equipment not found!"}
        )

    def test_get_equipment(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.character.name}')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.data
        fields = [field.name for field in Equipment._meta.get_fields()]
        self.assertEqual(
            first=sorted(list(data.keys())),
            second=sorted(fields)
        )

    def test_update_equipment_but_char_does_not_exist(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.post(
            f'/api/equipments/{test_charname}', data={'a': 'b'})
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_equipment_but_it_does_not_exist(self):
        self._require_login()
        char_wout_eq = Character.objects.create(
            name="TestChar3", level=92, char_class="Sorceress", acc=self.account
        )
        Equipment.objects.get(char=char_wout_eq).delete()
        response = self.client.post(
            f'/api/equipments/{char_wout_eq.name}', data={'random': 'data'})
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_equipment_empty_request(self):
        self._require_login()
        response = self.client.post(
            f'/api/equipments/{self.character.name}', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_update_equipment_single_field(self):
        self._require_login()
        response = self.client.post(
            f'/api/equipments/{self.character.name}', data=json.dumps({"helmet": "Shako 141"}), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        eq = Equipment.objects.get(char=self.character)
        self.assertEqual(eq.helmet, 'Shako 141')

    def test_update_equipment_all_fields(self):
        self._require_login()
        payload = {
            'helmet': 'Griffon 20/15 15ias 15@',
            'armor': 'Enigma 15/775/15 MP',
            'belt': 'TGV 200ed',
            'gloves': '3/20 gloves',
            'boots': 'WW 65l',
            'amulet': 'Mara 30',
            'left_ring': 'Raven 20',
            'right_ring': 'Manald',
            'main_hand': 'Eth Upg Titans 200ed',
            'off_hand': 'JMOD 148 60/60',
            'switch_main_hand': 'Cta 6/6/4',
            'switch_off_hand': 'Spirit 35',
            'torch': '20/20/5',
            'anni': '20/20/10',
            'charms': '9x java45',
        }
        response = self.client.post(
            f'/api/equipments/{self.character.name}', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        eq = Equipment.objects.get(char=self.character)
        # get dictionary with all fields and their values to check if changes had been applied
        eq_fields = eq.__dict__
        self.assertDictContainsSubset(payload, eq_fields)
