from rest_framework.decorators import api_view
from rest_framework.response import Response
from network.models import Haltestelle
from .serializers import HaltestelleSerializer

@api_view(['GET'])
def getStops(request):
    stops = [
        'GET /api',
        'GET /api/Haltestellen',
        'GET /api/Haltestellen/:id'
    ]
    return Response(stops)


@api_view(['GET'])
def getHaltestellen(request):
    Stop = Haltestelle.objects.all()
    serializer = HaltestelleSerializer(Stop, many=True)
    return Response(serializer.data)