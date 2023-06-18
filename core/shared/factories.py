import factory
import faker
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from manager.models import Account, Character

User = get_user_model()

DEFAULT_USER_FACTORY_PASSWORD = 'test'

fake = faker.Faker()


def get_unique_name() -> str:
    name: str = fake.unique.name()
    name = name.replace(' ', '')
    if len(name) > 15:
        name = name[:15]
    return name


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttributeSequence(
        lambda o, n: "%s_%s_%d" % (o.first_name.lower(), o.last_name.lower(), n)
    )
    email = factory.LazyAttributeSequence(
        lambda o, n: "%s.%s%d@example.com" % (o.first_name.lower(), o.last_name.lower(), n)
    )
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_USER_FACTORY_PASSWORD)
    profile = factory.RelatedFactory(
        'core.shared.factories.ProfileFactory',
        factory_related_name='user'
    )


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'profiles.Profile'

    user = factory.SubFactory(
        'core.shared.factories.UserFactory',
        profile=None
    )


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = 'manager.Account'

    name = factory.LazyFunction(get_unique_name)
    profile = factory.SubFactory(
        'core.shared.factories.ProfileFactory',
    )
    realm = factory.Faker(
        'random_element',
        elements=Account.Realm.values
    )


class CharacterFactory(DjangoModelFactory):
    class Meta:
        model = 'manager.Character'

    name = factory.LazyFunction(get_unique_name)
    level = factory.Faker('random_int', min=1, max=99)
    char_class = factory.Faker(
        'random_element',
        elements=Character.Class.values
    )
    acc = factory.SubFactory(
        'core.shared.factories.AccountFactory',
    )
    hardcore = factory.Faker('boolean', chance_of_getting_true=30)
    ladder = factory.Faker('boolean', chance_of_getting_true=50)

    @factory.post_generation
    def expansion(obj, created, extracted, **kwargs):
        if obj.char_class in [Character.Class.DRUID, Character.Class.ASSASSIN]:
            obj.expansion = True
            return

        obj.expansion = fake.boolean(chance_of_getting_true=70)
