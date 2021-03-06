import enum

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class GENDER(enum.Enum):
    not_specified = 1
    female = 2
    male = 3


class CustomUser(AbstractUser):
    gender = models.PositiveSmallIntegerField(
        'Gender',
        choices=tuple((s.value, s.name) for s in GENDER),
        default=GENDER.not_specified.value,
        db_index=True,
    )
    birthday = models.DateTimeField(
        'Birthday',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'User: {self.username} {self.email}'


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='logged_in_user',
        on_delete=models.CASCADE,
    )
