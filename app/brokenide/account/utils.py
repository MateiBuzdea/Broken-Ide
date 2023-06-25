from django.core import validators
from django.utils.translation import gettext_lazy as _


class UserNameValidator(validators.RegexValidator):
    regex = r"^[\/\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only "
        "letters, numbers, and ./-/_/+/@ characters."
    )
    flags = 0
