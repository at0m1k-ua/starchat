from rest_framework.serializers import ModelSerializer


class DefaultSerializerFactory:
    @staticmethod
    def of(model_type):
        class Serializer(ModelSerializer):
            class Meta:
                model = model_type
                fields = '__all__'

        return Serializer
