import pydantic
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from starchat.requests import DestroyItemRequestUrlParams, RetrieveItemUrlParams


class BaseCrud(ModelViewSet):
    model = None
    create_request_body = None
    update_request_url_params = None
    update_request_body = None
    list_request_params = None
    list_related_object_type = None
    list_related_object_fk_name = None

    def __init__(self, **kwargs):
        self.queryset = self.model.objects.all()
        super().__init__(**kwargs)

    def create(self, *args, **kwargs):
        body = self._pack_to_req_model(self.create_request_body, self.request.data)

        item_to_create = self.get_queryset().create(**body.dict(), sender_id=self.request.user.id)
        item_to_create.save()
        serializer = self.get_serializer(item_to_create)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, *args, **kwargs):
        params = self._pack_to_req_model(self.list_request_params, self.request.GET)

        related_item = get_object_or_404(self.list_related_object_type, id=params.related_object_id)
        listed_items = self.model.objects.filter(**{self.list_related_object_fk_name: related_item.id})
        serializer = self.get_serializer(listed_items, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, *args, **kwargs):
        url_params = self._pack_to_req_model(RetrieveItemUrlParams, self.kwargs)

        item = get_object_or_404(self.get_queryset(), id=url_params.id)
        serializer = self.get_serializer(item)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, *args, **kwargs):
        url_params = self._pack_to_req_model(self.update_request_url_params, self.kwargs)
        body = self._pack_to_req_model(self.update_request_body, self.request.data)

        item_to_update = get_object_or_404(self.get_queryset(), id=url_params.id)
        if 'sender_id' in model_to_dict(item_to_update) \
                and item_to_update.sender_id != self.request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        item_to_update.__class__.objects.filter(id=item_to_update.id).update(**body.dict())
        item_to_update.refresh_from_db()
        serializer = self.get_serializer(item_to_update)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, *args, **kwargs):
        url_params = self._pack_to_req_model(DestroyItemRequestUrlParams, self.kwargs)

        item_to_delete = get_object_or_404(self.get_queryset(), id=url_params.id)
        if item_to_delete.sender_id != self.request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        item_to_delete.delete()
        return Response(status.HTTP_200_OK)

    @staticmethod
    def _pack_to_req_model(model_class, data):
        if type(data) is not dict:
            data = data.dict()

        try:
            return model_class(**data)

        except pydantic.ValidationError as e:
            error_messages = []
            for error in e.errors():
                field = error.get('loc')[0]
                error_message = error.get('msg')
                error_messages.append(f"{field}: {error_message}")

            raise ValidationError(detail=error_messages)
