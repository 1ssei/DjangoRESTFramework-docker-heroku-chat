from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from . import views as login_views
from chats.urls import router as chats_router
from rest_framework import routers


api_router = routers.DefaultRouter()
api_router.registry.extend(chats_router.registry)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', login_views.SessionView, name='test'),
    url(r'^v1/', include(api_router.urls)),
    path('v1/logout/', views.LogoutView.as_view(), name='logout'),
    path('v1/auth/', include('social_django.urls', namespace='social')),
    path('silk/', include('silk.urls', namespace='silk'))
]
