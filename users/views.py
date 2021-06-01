from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class Profile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'username': request.user.username,
                'email': request.user.email,
                'gender': models.GENDER(request.user.gender).name,
                'birthday': request.user.birthday,
            }
        )


class UserList(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


User = get_user_model()


class OnlineUserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        users = User.objects.select_related('logged_in_user')
        for user in users:
            user.status = (
                'Online' if hasattr(user, 'logged_in_user') else 'Offline'
            )
        return render(request, 'user/user_list.html', {'users': users})


class Chat(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, room_name, *args, **kwargs):
        return render(request, 'user/chat.html', {'room_name': room_name})
