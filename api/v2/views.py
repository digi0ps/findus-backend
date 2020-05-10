from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models import *
from api.serializers import *
from utils.facer import FaceRecogniser
from utils.images import TempImage


class FindView(APIView):
    def post(self, request):
        try:
            file = request.FILES['image']
        except KeyError:
            return Response({
                'error': 'Bad Params.'
            }, status=HTTP_400_BAD_REQUEST)

        image = TempImage(file)
        image.save()

        matches = []
        facer = FaceRecogniser(image.path)

        for [person, _] in facer.get_matched_persons():
            # If person is an unknown guy, skip
            if not person:
                continue

            matches.append(person)

        image.delete()

        result = PersonSerializer(matches, many=True).data

        return Response({
            'found': bool(len(matches)),
            'matches': result,
        }, status=HTTP_200_OK)
