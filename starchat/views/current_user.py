from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from starchat.serializers.user import UserSerializer


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
