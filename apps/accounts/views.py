from rest_framework import viewsets, permissions, decorators, mixins, response
from rest_framework.authtoken.models import Token

from django.shortcuts import render

from . import models, serializers


# Create your views here.
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.AuthTokenSerializer

    @decorators.action(
        detail=False, methods=['POST'],
        serializer_class=serializers.AuthTokenSerializer,
    )
    def token(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({'token': token.key})
