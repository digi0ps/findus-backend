from django.db.models import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
import os

from root.settings import BASE_DIR

from .models import *
from .serializers import *
from utils.facer import recognize_image
from utils.images import TempImage


class PhotoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        photos = Photo.objects.all()
        json = PhotoSerializer(photos, many=True)

        return Response(json.data)

    def post(self, request):
        # TODO: Save Images with custom names
        photo = PhotoSerializer(data=request.data)

        if photo.is_valid():
            photo_obj = photo.save()

            # DO FACE REC Logic
            absolute_path = os.path.join(
                BASE_DIR, 'gallery', str(photo_obj.image))

            for person in recognize_image(absolute_path):
                print(person)
                photo_obj.persons.add(person)

            photo_obj.save()

            return Response(photo.data, status=HTTP_202_ACCEPTED)
        else:
            print('error', photo.errors)
            return Response(photo.errors, status=HTTP_400_BAD_REQUEST)


class PersonView(APIView):
    def get(self, request):
        all_persons = FaceEncoding.objects.all()
        json = PersonSerializer(all_persons, many=True)

        return Response(json.data, status=HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name', '')
        person_id = request.data.get('person_id', '')

        if not name or not person_id:
            return Response({
                'error': 'Bad Params.'
            }, status=HTTP_400_BAD_REQUEST)

        try:
            person = FaceEncoding.objects.get(id=person_id)
            person.person_name = name
            person.save()

            person_serialiser = PersonSerializer(person)
            return Response(person_serialiser.data, status=HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                'error': 'Photo or Person not found.'
            }, status=HTTP_404_NOT_FOUND)


class SearchView(APIView):
    def post(self, request):
        try:
            file = request.FILES['image']
        except KeyError:
            return Response({
                'error': 'Bad Params.'
            }, status=HTTP_400_BAD_REQUEST)

        image = TempImage(file)
        image.save()

        result = {}

        for person in recognize_image(image.path):
            images = person.photo_set.all()
            images_json = PhotoSerializer(images, many=True).data
            result[person.person_name] = images_json

        image.delete()

        return Response({
            'found': bool(len(result.keys())),
            'result': result,
        }, status=HTTP_200_OK)
