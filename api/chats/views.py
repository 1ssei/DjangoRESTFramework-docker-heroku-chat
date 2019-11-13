from rest_framework import viewsets
from . import models
from . import serializer
from api import permission
from django.contrib.auth.mixins import UserPassesTestMixin


class ThreadPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return permission.OwnerPermission(self, models.Thread)


class ThreadViewSet(ThreadPermission, viewsets.ModelViewSet):
    """
    Thread CRUD, only owner can patch and delete thread.
    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer
