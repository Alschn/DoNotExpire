from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

alphanumeric_validator = RegexValidator(
    r'^[0-9a-zA-Z\.\-\_]{2,15}$',
    'Account name should consist of alphanumerics and ".", "-", "_" signs, and be between 2 and 15 characters.'
)  # and probably more special signs

letters_only_validator = RegexValidator(
    r'^[a-zA-Z\_]{2,15}$',
    "Character's name should consist of letters only and up to one underscore. It should be between 2 and 15 "
    "characters. "
)


def underscore_validator(value: str) -> None:
    if value.count('_') > 1:
        raise ValidationError(
            "Character's name can consist of at most one underscore!"
        )

    elif value.startswith('_') or value.endswith('_'):
        raise ValidationError(
            "Character's name cannot start nor end with an underscore!"
        )
