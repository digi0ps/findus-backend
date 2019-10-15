from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .models import *
from .serializers import *


class PhotoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        photos = Photo.objects.all()
        print('photos', photos)
        json = PhotoSerializer(photos, many=True)

        return Response(json.data)

    def post(self, request):
        photos = PhotoSerializer(data=request.data)

        if photos.is_valid():
            photos.save()

            return Response(photos.data, status=HTTP_202_ACCEPTED)
        else:
            print('error', photos.errors)
            return Response(photos.errors, status=HTTP_400_BAD_REQUEST)
