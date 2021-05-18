import enum
from django.db import models
from django.contrib.postgres import fields
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class TASK_STATUS(enum.Enum):
    active = 1
    paused = 2
    finished = 3


def get_time_entries_default():
    return [[timezone.now(), None]]


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        'Task status',
        choices=tuple((s.value, s.name) for s in TASK_STATUS),
        default=TASK_STATUS.active.value,
        db_index=True,
    )
    time_entries = fields.ArrayField(
        fields.ArrayField(
            models.DateTimeField(null=True, blank=True),
            size=2,
        ),
        default=get_time_entries_default,
    )
    owner = models.ForeignKey(
        'users.CustomUser', related_name='tasks', on_delete=models.CASCADE
    )

    def __str__(self):
        """A string representation of the model."""
        return f'Task: {self.name} {TASK_STATUS(self.status)}'
