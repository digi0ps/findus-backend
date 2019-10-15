import cv2
import face_recognition as fr
import numpy as np
import json

from api.models import FaceEncoding


def get_image(filename):
    image = cv2.imread(filename)
    small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    rgb_small_image = small_image[:, :, ::-1]

    return rgb_small_image


def get_encodings(image):
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    return face_encodings


def dump(nparray):
    return json.dumps(nparray.tolist())


def load(strarray):
    return np.asarray(json.loads(strarray))


def match_encodings(encodings):
    # Retreive encodings from DB
    all_encodings = FaceEncoding.objects.all()
    known_encodings = [load(f.encoding) for f in all_encodings]
    known_faces = [f.person_name for f in all_encodings]

    print('SFGADF', known_encodings, known_faces)

    face_encoding = None

    for encoding in encodings:
        matches = fr.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            face_distances = fr.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_faces[best_match_index]
                print(all_encodings)
                face_encoding = list(all_encodings)[best_match_index]
        else:
            face_encoding = FaceEncoding()
            face_encoding.encoding = dump(encoding)
            face_encoding.save()

        print(name)
    # TODO: Return all the matched encodings
    return face_encoding


def recognize_image(filename):
    img = get_image(filename)
    encodings = get_encodings(img)
    fenc = match_encodings(encodings)

    return fenc


# TODO: Merge Multiple Encodings into one
