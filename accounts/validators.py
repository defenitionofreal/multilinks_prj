from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MyUsernameValidator(validators.RegexValidator):
    """
    Validator for usernames.

    - Only ASCII lowercase letters, numbers and underscore are supported.
    - Must start with a letter.
    """
    regex = r'^[a-z][a-z0-9_]+$'
    message = _(
        'Введите корректный Login. Допустимые значения: латинские буквы в маленьком регистре, '
        'цифры, и нижнее подчеркивание. Должно начинаться с буквы. Максимум 50 символов.'
    )
    flags = 0