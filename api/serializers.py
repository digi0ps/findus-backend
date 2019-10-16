from rest_framework import serializers
from .models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceEncoding
        fields = ['person_name']


class PhotoSerializer(serializers.ModelSerializer):
    persons = PersonSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'image', 'persons']