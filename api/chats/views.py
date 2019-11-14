from rest_framework import viewsets, mixins
from . import models
from . import serializer
from api import permission
from django.contrib.auth.mixins import UserPassesTestMixin
from django_filters.rest_framework import DjangoFilterBackend


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


class ThreadMemberPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        if not permission.OwnerPermission(self, models.Thread):
            return False
        if (self.request.method == 'GET') and ('pk' in self.kwargs):
            thread = models.Thread.objects.get(id=self.kwargs['pk'])
            if not thread.is_public:
                return False
        return True


class ThreadMemberViewSet(ThreadMemberPermission,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    ThreadMember CRUD, only owner can create and delete threadmember.
    patch and put is not allowed.
    list is ok, but you need to add filter ,for e.g.
    /v1/threadmembers/?thread=1
    """

    queryset = models.ThreadMember.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.ThreadMemberREADSerializer
        return serializer.ThreadMemberSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['thread']
