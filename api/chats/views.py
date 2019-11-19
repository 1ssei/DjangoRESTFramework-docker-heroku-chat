from rest_framework import viewsets, mixins
from . import models
from . import serializer
from api import permission
from django.contrib.auth.mixins import UserPassesTestMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
import json


class ThreadPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        if not permission.OwnerPermission(self, models.Thread):
            return False
        if (self.request.method == 'GET') and ('pk' in self.kwargs):
            raise MethodNotAllowed('Retrieve is not allowed')
        return True


class ThreadViewSet(ThreadPermission, viewsets.ModelViewSet):
    """
    Thread CRUD, only owner can patch and delete thread.
    """

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.Thread.objects.all().filter(
                is_public=True).order_by('title')
        return models.Thread.objects.all().order_by('id')
    serializer_class = serializer.ThreadSerializer

    def perform_create(self, serializer):
        created_data = serializer.save()
        models.ThreadMember(thread=created_data,
                            user=created_data.owner).save()


class ThreadMemberPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        request = self.request
        userId = request.user.id
        if not request.user.is_authenticated:
            return False
        if self.request.method == 'GET':
            if not ('thread' in request.GET):
                raise PermissionDenied(
                    "you need filtering ,\
                     for e.g. v1/thread_members/?thread=1")
            thread = models.Thread.objects.get(id=request.GET['thread'])
            if not thread.has_permission(userId):
                raise PermissionDenied("you cannot see this data")
        elif request.method == 'POST':
            # ONLY Thread Owner
            thread = models.Thread.objects.get(id=request.POST['thread'])
            # SELECT rerated or user model で比較 performance check
            if thread.owner.id != userId:
                raise PermissionDenied("only owner is allowed")
            # 重複はNG
            if models.ThreadMember.objects.filter(
                    thread=request.POST['thread'],
                    user_id=request.POST['user']).exists():
                raise PermissionDenied("this data is already exist")
        elif request.method == 'DELETE':
            original_data = models.ThreadMember.objects.get(
                pk=self.kwargs['pk'])
            # ONLY Thread Owner ここもselect related かも
            if original_data.thread.owner.id != userId:
                raise PermissionDenied("only owner is allowed")
            # Owner を消すことはできない
            if original_data.user.id == original_data.thread.owner.id:
                raise PermissionDenied("nobody can delete owner data")
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


class CommentPermission(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        request = self.request
        if not permission.OwnerPermission(self, models.Comment):
            return False
        userId = request.user.id
        if request.method == 'GET':
            if not ('thread' in request.GET):
                raise PermissionDenied(
                    "you need filtering ,for e.g. v1/comments/?thread=1")
            thread = models.Thread.objects.get(id=request.GET['thread'])
            if not thread.has_permission(userId):
                raise PermissionDenied("you cannot see this data")
        elif request.method == 'POST':
            thread = models.Thread.objects.get(id=request.POST['thread'])
            if not thread.has_permission(userId):
                raise PermissionDenied("you cannot see this data")
        elif request.method == 'PATCH':
            data = json.loads(request.body)
            for i in ['thread', 'owner']:
                if i in data:
                    raise PermissionDenied("you cannot patch ", i)
        return True


class CommentViewSet(CommentPermission, viewsets.ModelViewSet):
    """
    /comments/ POST
    /comments/?thread=1 GET
    /comments/1/ PATCH
    /comments/1/ DELETE
    """
    queryset = models.Comment.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializer.CommentREADSerializer
        return serializer.CommentSerializer
