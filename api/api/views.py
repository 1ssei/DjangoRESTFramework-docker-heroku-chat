import users.models as users_models
from django.http.response import JsonResponse
# from django.shortcuts import redirect
from chats.models import ThreadMember
from chats.serializer import ThreadMemberThreadREADSerializer


def SessionView(request):
    if request.user.is_anonymous:
        return JsonResponse(
            {'msg': 'please login from /v1/auth/login/google-oauth2'})
    user = users_models.User.objects.get(pk=request.user.id)
    my_threads = ThreadMember.objects.filter(user=user)
    my_threads = ThreadMemberThreadREADSerializer(my_threads, many=True).data

    user_info = {
        'id': user.id,
        'name': user.username,
        'sessionid': request.COOKIES.get('sessionid'),
        'csrftoken': request.COOKIES.get('csrftoken'),
        'isSignedIn': True,
        'my_thread': my_threads
    }
    return JsonResponse(user_info)


# def RedirectView(request):
#     if 'url' not in request.GET:
#         return redirect('http://front.****.herokuapp.com:3000/auth')
#     url = request.GET['url']
    # return redirect(
    #     'http://front.****.herokuapp.com:3000/auth?nextUrl=' + url)
