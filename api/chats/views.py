from rest_framework import viewsets
from . import models
from . import serializer
from api import permission
from django.contrib.auth.mixins import UserPassesTestMixin


class ThreadPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        if not permission.OwnerPermission(self, models.Thread):
            return False
        if (self.request.method == 'GET') and ('pk' in self.kwargs):
            thread = models.Thread.objects.get(id=self.kwargs['pk'])
            if not thread.is_public:
                return False
        return True


class ThreadViewSet(ThreadPermission, viewsets.ModelViewSet):
    """
    Thread CRUD, only owner can patch and delete thread.
    """
    def get_queryset(self):
        if self.request.method == 'GET':
            return models.Thread.objects.all().filter(is_public=True)
        return models.Thread.objects.all().order_by('id')
    serializer_class = serializer.ThreadSerializer
