import cv2
import face_recognition as fr
import numpy as np
import json

from api.models import Person
import namegenerator

# TODO: Merge Multiple Encodings into one


class FaceRecogniser:
    def __init__(self, filename):
        self.filename = filename

        self.image = self.get_mod_image()

    def get_mod_image(self):
        image = cv2.imread(self.filename)
        small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        rgb_small_image = small_image[:, :, ::-1]

        return rgb_small_image

    def get_encodings(self):
        face_locations = fr.face_locations(self.image)
        face_encodings = fr.face_encodings(self.image, face_locations)

        return face_encodings

    def dump(self, nparray):
        return json.dumps(nparray.tolist())

    def load(self, strarray):
        return np.asarray(json.loads(strarray))

    def get_matched_persons(self):
        encodings = self.get_encodings()  # From the user uploaded image

        stored_persons = Person.objects.all()  # All encodings in database
        stored_encodings = [load(f.face_encoding) for f in stored_persons]

        matched_person = None

        for encoding in encodings:
            if not len(stored_persons):
                yield [None, encoding]
                continue

            matches = fr.compare_faces(stored_encodings, encoding)
            face_distances = fr.face_distance(stored_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            if True in matches and face_distances[best_match_index] < 0.4:
                matched_person = list(stored_persons)[best_match_index]
            else:
                matched_person = None

            # Convert nparray to string and return
            encoding = dump(encoding)
            yield [matched_person, encoding]
