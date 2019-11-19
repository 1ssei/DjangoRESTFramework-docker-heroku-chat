from rest_framework import serializers
from . import models
import users.serializer as users_serializer


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = '__all__'


class ThreadMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThreadMember
        fields = '__all__'


class ThreadMemberREADSerializer(serializers.ModelSerializer):
    user = users_serializer.UserMinSerializer

    class Meta:
        model = models.ThreadMember
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class CommentREADSerializer(serializers.ModelSerializer):
    user = users_serializer.UserMinSerializer

    class Meta:
        model = models.ThreadMember
        fields = '__all__'