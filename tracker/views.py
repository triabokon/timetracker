from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseBadRequest

from rest_framework import generics, permissions, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from .permissions import IsOwnerOrReadOnly

from users.models import GENDER


class Home(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response('Home of Lume application')


class TaskPause(APIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request, pk, *args, **kwargs):
        task = models.Task.objects.get(pk=pk)
        if task.status == models.TASK_STATUS.paused.value:
            return HttpResponseBadRequest('Task already has paused')
        if task.status == models.TASK_STATUS.finished.value:
            return HttpResponseBadRequest('Task is finished and cannot be paused')
        last_times_entry = task.time_entries.pop()
        last_times_entry[1] = timezone.now()
        task.time_entries.append(last_times_entry)
        task.status = models.TASK_STATUS.paused.value
        task.save()
        return Response(
            {
                'task_status': task.status,
            }
        )


class TaskResume(APIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request, pk, *args, **kwargs):
        task = models.Task.objects.get(pk=pk)
        if task.status == models.TASK_STATUS.active.value:
            return HttpResponseBadRequest('Task is active')
        if task.status == models.TASK_STATUS.finished.value:
            return HttpResponseBadRequest('Task is finished and cannot be resumed')
        task.time_entries.append(models.get_time_entries_default()[0])
        task.status = models.TASK_STATUS.active.value
        task.save()
        return Response(
            {
                'task_status': task.status,
            }
        )


class TaskFinish(APIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request, pk, *args, **kwargs):
        task = models.Task.objects.get(pk=pk)
        if task.status == models.TASK_STATUS.finished.value:
            return HttpResponseBadRequest('Task already has finished')
        if task.status == models.TASK_STATUS.active.value:
            last_times_entry = task.time_entries.pop()
            last_times_entry[1] = timezone.now()
            task.time_entries.append(last_times_entry)
        task.status = models.TASK_STATUS.finished.value
        task.save()
        return Response({'task_status': task.status})


class TaskList(generics.ListCreateAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class About(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'about': (
                    'Lume is a time tracking application. '
                    'Track your time for more comfortable and productive work.'
                )
            }
        )
