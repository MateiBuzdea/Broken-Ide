from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils import UserNameValidator


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Based on django.contrib.auth.models.AbstractUser
    """

    class Meta:
        db_table = 'User_Accounts'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        abstract = False

    objects = UserManager()

    # this validator is present in the default user model
    username_validator = UserNameValidator()

    IDE_THEMES = (
        ('darcula', 'dark'),
        ('default', 'light'),
    )

    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    theme = models.CharField(
        _("IDE theme"),
        max_length=10,
        choices=IDE_THEMES,
        default="darcula",
    )
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    email = models.EmailField(_("email"), max_length=50, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates if the user is Staff."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['theme',]

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def clean(self):
        # this normalizes the username field
        self.username = self.normalize_username(self.username)

    def __str__(self):
        return self.username
