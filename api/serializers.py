from rest_framework import serializers
from .models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'id']


class PhotoSerializer(serializers.ModelSerializer):
    persons = PersonSerializer(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = ['id', 'image', 'persons']
