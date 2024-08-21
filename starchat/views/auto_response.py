from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from starchat.models.auto_response import AutoResponse
from starchat.requests.auto_response.create import CreateAutoResponseRequestBody
from starchat.views.base_crud import BaseCrudViewSet


class AutoResponseViewSet(BaseCrudViewSet):
    permission_classes = [IsAuthenticated]
    create_request_body = CreateAutoResponseRequestBody
    queryset = AutoResponse.objects.all()

    def create(self, *args, **kwargs):
        body = self._pack_to_req_model(self.create_request_body, self.request.data)

        if body.timeout == 0:
            self.get_queryset().filter(user_id=self.request.user.id).delete()
        else:
            auto_response: AutoResponse = self.get_queryset().get_or_create(user_id=self.request.user.id)[0]
            auto_response.timeout = body.timeout
            auto_response.save()

        body = {'timeout': body.timeout}
        return Response(status=status.HTTP_200_OK, data=body)

    def retrieve(self, *args, **kwargs):
        item_or_empty = self.get_queryset().filter(user_id=self.request.user.id)
        if item_or_empty.exists():
            timeout = item_or_empty.get().timeout
        else:
            timeout = 0

        body = {'timeout': timeout}
        return Response(status=status.HTTP_200_OK, data=body)
