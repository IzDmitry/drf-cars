from rest_framework import serializers
from .models import Model


class FieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов Model.
    """
    class Meta:
        model = Model
        fields = '__all__'
