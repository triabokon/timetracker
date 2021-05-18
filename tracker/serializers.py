from rest_framework import serializers
from tracker import models


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'time_entries',
            'status',
            'owner',
        )
        model = models.Task
