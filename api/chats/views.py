from rest_framework import viewsets
from . import models
from . import serializer


class ThreadViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for CRUD thread
    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer
