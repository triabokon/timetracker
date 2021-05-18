from rest_framework import serializers
from . import models
from tracker.models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = (
            'id',
            'username',
            'email',
            'birthday',
            'gender',
        )
