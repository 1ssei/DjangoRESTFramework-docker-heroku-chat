from rest_framework import serializers
from . import models
# import users.serializer as users_serializer


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = '__all__'

# class ProjectMinSerializer(serializers.ModelSerializer):
#     po_detail = serializers.SerializerMethodField()
#     detail = serializers.SerializerMethodField()
#     status = serializers.SerializerMethodField()

#     def get_po_detail(self, instance):
#         po = instance.po
#         return users_serializer.UserMinSerializer(po).data

#     def get_detail(self, instance):
#         return instance.detail[:300]
    
#     def get_status(self, instance):
#         return instance.get_status_display()

#     class Meta:
#         model = models.Project
#         fields = '__all__'