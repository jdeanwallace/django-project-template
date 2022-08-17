import logging

from rest_framework import views, permissions, response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers


logger = logging.getLogger(__name__)


# Create your views here.
class AuthTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
