import json
import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIRequestFactory, APIClient

from DoNotExpire.manager.models import Account, Character, Equipment
from DoNotExpire.manager.serializers import (
    EquipmentSerializer,
    AccountSerializer, CreateAccountSerializer,
    CharacterSerializer, CreateCharacterSerializer,
)


class TestAPIViews(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user('testuser', password='testing')
        cls.user2 = User.objects.create_user(username='otheruser', password='b$labla12@g')
        cls.acc = Account.objects.create(
            name="TestAcc", profile=cls.user.profile, realm="Europe"
        )
        cls.acc2 = Account.objects.create(
            name="OtherAcc", profile=cls.user2.profile, realm="Europe"
        )
        cls.char = Character.objects.create(
            name="TestChar", level=90, char_class="Amazon", acc=cls.acc
        )
        cls.char2 = Character.objects.create(
            name="TestChar2", level=99, char_class="Sorceress", acc=cls.acc
        )
        cls.other_user_char = Character.objects.create(
            name="Other", level=69, char_class="Paladin", acc=cls.acc2
        )

        cls.acc_with_few_chars = Account.objects.create(
            name='Cascade', realm='Europe', profile=cls.user.profile
        )
        Character.objects.bulk_create([
            Character(id=100, name='Testo', level=50, acc=cls.acc_with_few_chars),
            Character(id=101, name='Viron', level=99, acc=cls.acc_with_few_chars),
            Character(id=102, name='Uchodźca', level=50, acc=cls.acc_with_few_chars)
        ])

    def _require_login(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.force_login(user=self.user)

    def test_is_not_authenticated(self):
        response = self.client.post(f'/api/chars/{self.char.name}/', {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_is_not_authenticated_read_only(self):
        response = self.client.get(f'/api/chars/{self.char.name}/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_is_authenticated(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.char.name}/')
        self.assertNotEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_is_char_owner_permission(self):
        User.objects.create_user(
            'sus', email='sus@test.com', password='testing123'
        )
        self.client.login(username="sus", password="testing123")
        response = self.client.get(f'/api/chars/{self.char.name}/equipment')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_get_equipment_char_not_exists(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.get(f'/api/chars/{test_charname}/equipment')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {'Error': f"Character {test_charname} not found!"}
        )

    def test_get_equipment_which_does_not_exist(self):
        char_wout_eq = Character.objects.create(
            name="doesntmatter", level=91, char_class="Paladin", acc=self.acc
        )
        Equipment.objects.get(char=char_wout_eq).delete()

        self._require_login()
        response = self.client.get(f'/api/chars/{char_wout_eq.name}/equipment')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {'Error': f"{char_wout_eq.name}'s equipment not found!"}
        )

    def test_get_equipment(self):
        self._require_login()
        response = self.client.get(f'/api/chars/{self.char.name}/equipment')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.data
        fields = [field.name for field in Equipment._meta.get_fields()]
        self.assertEqual(
            first=sorted(list(data.keys())),
            second=sorted(fields)
        )
        eq = Equipment.objects.get(char__name=self.char.name)
        self.assertEqual(response.json(), EquipmentSerializer(eq).data)

    def test_update_equipment_but_char_does_not_exist(self):
        self._require_login()
        test_charname = 'charthatdoesnotexist'
        response = self.client.post(
            f'/api/chars/{test_charname}/equipment', data={'a': 'b'})
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_equipment_but_it_does_not_exist(self):
        self._require_login()
        char_wout_eq = Character.objects.create(
            name="TestChar3", level=92, char_class="Sorceress", acc=self.acc
        )
        Equipment.objects.get(char=char_wout_eq).delete()
        response = self.client.post(
            f'/api/chars/{char_wout_eq.name}/equipment', data={'random': 'data'}
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_equipment_empty_request(self):
        self._require_login()
        response = self.client.post(
            f'/api/chars/{self.char.name}/equipment',
            data=json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'Error': 'Received empty request!'})

    def test_update_equipment_single_field(self):
        self._require_login()
        response = self.client.post(
            f'/api/chars/{self.char.name}/equipment',
            data=json.dumps({"helmet": "Shako 141"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        eq = Equipment.objects.get(char=self.char)
        self.assertEqual(eq.helmet, 'Shako 141')
        self.assertEqual(response.json(), EquipmentSerializer(eq).data)

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
            f'/api/chars/{self.char.name}/equipment',
            data=json.dumps(payload), content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        eq = Equipment.objects.get(char=self.char)
        self.assertEqual(response.json(), EquipmentSerializer(eq).data)

    def test_update_equipment_invalid_data(self):
        self._require_login()
        payload = {
            'helmet': ''.join(random.choice(string.ascii_letters) for _ in range(51)),
            'anni': ''.join(random.choice(string.ascii_letters) for _ in range(11)),
            'charms': ''.join(random.choice(string.ascii_letters) for _ in range(200)),
        }
        response = self.client.post(
            f'/api/chars/{self.char.name}/equipment',
            data=json.dumps(payload), content_type='application/json'
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'helmet': ['Ensure this field has no more than 50 characters.'],
                'anni': ['Ensure this field has no more than 10 characters.'],
                'charms': ['Ensure this field has no more than 100 characters.']
            }
        )

    def test_list_characters(self):
        self._require_login()
        response = self.client.get('/api/chars/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(),
            CharacterSerializer(Character.objects.all(), many=True).data
        )

    def test_list_characters_user_not_authenticated(self):
        response = self.client.get('/api/chars/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_new_character(self):
        self._require_login()
        response = self.client.post('/api/chars/', {
            'name': 'Test',
            'level': 12,
            'char_class': 'Barbarian',
            'expansion': True,
            'hardcore': False,
            'ladder': True,
            'acc': self.acc.id
        })
        expected_char = Character.objects.get(name='Test')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), CreateCharacterSerializer(expected_char).data)

    def test_create_new_character_without_optional_data(self):
        self._require_login()
        response = self.client.post('/api/chars/', {
            'name': 'mac',
            'level': 15,
            'char_class': 'Paladin',
            'acc': self.acc.id
        })
        expected_char = Character.objects.get(name='mac')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), CreateCharacterSerializer(expected_char).data)

    def test_create_new_char_but_it_already_exists(self):
        self._require_login()
        response = self.client.post('/api/chars/', {
            'name': 'TestChar',
            'level': 99,
            'char_class': 'Barbarian',
            'acc': self.acc.id
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_create_new_char_wrong_data(self):
        self._require_login()
        response = self.client.post('/api/chars/', {
            'name': 'Lol1',
            'level': 101,
            'char_class': 'Shaman',
            'acc': self.acc.id
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'name': ['Character name should consist of letters only. (2 to 15)'],
                'level': ['Ensure this value is less than or equal to 99.'],
                'char_class': ['"Shaman" is not a valid choice.']
            }
        )

    def test_create_new_char_on_not_owned_account(self):
        self._require_login()
        response = self.client.post('/api/chars/', {
            'name': 'NotMyOwnAcc',
            'level': 1,
            'char_class': 'Paladin',
            'acc': self.acc2.id
        })
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'message': 'You do not own this account!'})

    def test_update_character_char_doesnt_exist(self):
        self._require_login()
        response = self.client.patch('/api/chars/XDDDDDD/', {'name': 'wont happen'})
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_character_by_not_owner(self):
        self._require_login()
        response = self.client.patch(f'/api/chars/{self.other_user_char.name}/', {'level': 55})
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_update_character(self):
        self._require_login()
        self.assertEqual(self.char2.name, 'TestChar2')
        self.assertNotEqual(self.char2.level, 92)
        self.assertTrue(self.char2.expansion)
        self.assertNotEqual(self.char2.char_class, 'Druid')
        response = self.client.put(f'/api/chars/{self.char2.name}/', {
            'level': 92,
            'expansion': False,
            'char_class': 'Druid',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        refreshed_char2 = Character.objects.get(name=self.char2.name)
        self.assertEqual(response.json(), CharacterSerializer(refreshed_char2).data)
        self.assertEqual(refreshed_char2.level, 92)
        self.assertFalse(refreshed_char2.expansion)
        self.assertEqual(refreshed_char2.char_class, 'Druid')

    def test_update_character_partially(self):
        self._require_login()
        new_level = 91
        self.assertNotEqual(self.char.level, new_level)
        response = self.client.patch(f'/api/chars/{self.char.name}/', {
            'level': new_level,
        })
        updated_char = Character.objects.get(name=self.char.name)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), CharacterSerializer(updated_char).data)
        self.assertEqual(updated_char.level, new_level)

    def test_delete_character_char_doesnt_exist(self):
        self._require_login()
        response = self.client.delete(f'/api/chars/LMAO/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_char_by_not_owner(self):
        self._require_login()
        response = self.client.delete(f'/api/chars/{self.other_user_char.name}/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_delete_character(self):
        self._require_login()
        response = self.client.delete(f'/api/chars/{self.char2.name}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_list_accounts(self):
        self._require_login()
        response = self.client.get('/api/accs/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(),
            AccountSerializer(Account.objects.all(), many=True).data
        )

    def test_list_accounts_not_authenticated(self):
        response = self.client.get('/api/accs/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), AccountSerializer(Account.objects.all(), many=True).data)

    def test_create_new_account(self):
        self._require_login()
        response = self.client.post('/api/accs/', {
            'name': 'BadBatch',
            'realm': 'Europe',
        })
        new_acc = Account.objects.get(name='BadBatch')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), CreateAccountSerializer(new_acc).data)

    def test_create_new_acc_but_it_already_exists(self):
        self._require_login()
        response = self.client.post('/api/accs/', {
            'name': 'TestAcc',
            'realm': 'Asia',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'name': ['account with this name already exists.']})

    def test_create_new_acc_invalid_data(self):
        self._require_login()
        response = self.client.post('/api/accs/', {
            'name': '&//HaloPowiedzMiProsze',
            'realm': 'San Escobar',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'name': [
                    'Account name should consist of alphanumerics and' +
                    ' ".", "-", "_" signs, and be between 2 and 15 characters.',
                    'Ensure this field has no more than 15 characters.'
                ],
                'realm': ['"San Escobar" is not a valid choice.']
            }
        )

    def test_update_account(self):
        self._require_login()
        self.assertNotEqual(self.acc.realm, 'US East')
        response = self.client.patch(f'/api/accs/{self.acc.name}/', {
            'realm': 'US East',
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        updated_acc = Account.objects.get(name=self.acc.name)
        self.assertEqual(
            response.json(),
            AccountSerializer(updated_acc).data
        )
        self.assertEqual(updated_acc.realm, 'US East')

    def test_update_account_invalid_data(self):
        self._require_login()
        response = self.client.put(f'/api/accs/{self.acc.name}/', {
            'realm': 'lmao',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'realm': ['"lmao" is not a valid choice.']}
        )

    def test_update_account_acc_doesnt_exist(self):
        self._require_login()
        response = self.client.put(f'/api/accs/bajojajo/', {
            'realm': 'xd',
        })
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_update_account_by_not_owner(self):
        self._require_login()
        response = self.client.patch(f'/api/accs/{self.acc2.name}/', {
            'realm': 'US West'
        })
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_delete_account_acc_doesnt_exist(self):
        self._require_login()
        response = self.client.delete(f'/api/accs/hahah/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_acc_by_not_owner(self):
        self._require_login()
        response = self.client.delete(f'/api/accs/{self.acc2.name}/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_delete_account(self):
        self._require_login()
        lookup_name = self.acc_with_few_chars.name
        char_count_before = Character.objects.all().count()
        response = self.client.delete(f'/api/accs/{lookup_name}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Account.objects.get(name=lookup_name)
        self.assertNotEqual(char_count_before, Character.objects.all().count())
