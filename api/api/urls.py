from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from . import views
from chats.urls import router as chats_router
from rest_framework import routers


api_router = routers.DefaultRouter()
api_router.registry.extend(chats_router.registry)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.TestView, name='test'),
    url(r'^v1/', include(api_router.urls)),
]
