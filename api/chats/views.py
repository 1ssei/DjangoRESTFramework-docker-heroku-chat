from rest_framework import viewsets, permissions
from . import models
from . import serializer
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed


class ThreadPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        request = self.request
        userId = request.user.id
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')  # pragma: no cover
        if request.method == 'POST':
            param_user_id = request.POST['owner']
            if int(param_user_id) != userId:
                raise PermissionDenied("owner in post data is not yours")
        if (request.method == 'PATCH') or (request.method == 'DELETE'):
            original_project = models.Thread.objects.get(pk=self.kwargs['pk'])
            owner = original_project.owner.id
            if owner != userId:
                raise PermissionDenied(
                    "you can not patch projects which other people made")
        return True


class ThreadViewSet(ThreadPermission, viewsets.ModelViewSet):
    """
    A simple ViewSet for CRUD thread
    """
    queryset = models.Thread.objects.all()
    serializer_class = serializer.ThreadSerializer
