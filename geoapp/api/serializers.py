from rest_framework.serializers import ModelSerializer
from network.models import Haltestelle

class HaltestelleSerializer(ModelSerializer):
    class Meta:
        model = Haltestelle
        fields = '__all__'