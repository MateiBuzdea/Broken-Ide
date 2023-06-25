from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .utils import *


UserAccount = get_user_model()

class UserScript(models.Model):

    class Meta:
        db_table = 'User_Scripts'
        verbose_name = _("User_Script")
        verbose_name_plural = _("User_Scripts")

    user = models.ForeignKey(
        UserAccount,
        null=False,
        on_delete=models.CASCADE,
        related_name="scripts",
    )

    # This checks for bad characters in the program filename
    filename_validator = FileNameValidator()

    name = models.CharField(
        _("program_name"),
        max_length=50,
        unique=False,
        blank=False,
        help_text=_(
            "Give a name to your program. 50 characters or fewer."
        ),
        validators=[filename_validator],
    )

    public = models.BooleanField(
        _("is_public"),
        default=False,
    )

    @property
    def file_name(self):
        file = "%s.c" % (self.name, )
        return file
