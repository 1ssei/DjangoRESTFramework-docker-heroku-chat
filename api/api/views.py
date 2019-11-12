from django.http.response import JsonResponse


def TestView(request):
    return JsonResponse(
        {'test': 'test'})
