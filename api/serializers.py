from rest_framework import serializers

from base.models import Room, Topic, User


class RoomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['host', 'topic', 'name', 'description', 'participants', 'updated', 'created']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'bio', 'avatar']