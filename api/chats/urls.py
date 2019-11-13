from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'thread', views.ThreadViewSet, base_name='thread')
