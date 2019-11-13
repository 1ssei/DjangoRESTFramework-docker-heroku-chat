from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed


def OwnerPermission(self, model):
    request = self.request
    userId = request.user.id
    if request.method in permissions.SAFE_METHODS:
        return True
    if request.method == 'PUT':
        raise MethodNotAllowed('PUT')
    if request.method == 'POST':
        if int(request.POST['owner']) != userId:
            raise PermissionDenied("owner in post data is not yours")
    if (request.method == 'PATCH') or (request.method == 'DELETE'):
        original_project = model.objects.get(pk=self.kwargs['pk'])
        owner = original_project.owner.id
        if owner != userId:
            raise PermissionDenied(
                "you can not patch or delete data which other people made")
    return True
