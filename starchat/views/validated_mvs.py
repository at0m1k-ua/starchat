import pydantic
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet


class ValidatedModelViewSet(ModelViewSet):
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
