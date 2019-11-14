from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'threads', views.ThreadViewSet, base_name='thread')
router.register(r'thread_members', views.ThreadMemberViewSet,
                base_name='thread_member')
