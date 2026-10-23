from rest_framework import generics

from .models import Sensor, Measurement
from .serializers import (
    SensorSerializer,
    SensorDetailSerializer,
    MeasurementCreateSerializer,
)


class SensorListCreateView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all().prefetch_related('measurements')
    serializer_class = SensorSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        return SensorSerializer


class MeasurementCreateView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer