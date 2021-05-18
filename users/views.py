from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from . import models
from . import serializers

from tracker.permissions import IsOwnerOrReadOnly


class Profile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'gender': models.GENDER(request.user.gender).name,
            'birthday': request.user.birthday,
        })


class UserList(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
