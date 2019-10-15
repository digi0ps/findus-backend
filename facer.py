def show_image(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_image(filename):
    image = cv2.imread(filename)
    small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    rgb_small_image = small_image[:, :, ::-1]

    return rgb_small_image

def get_encodings(image):
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    return face_encodings

def match_encodings(encodings):
    # Retreive encodings from DB
    for encoding in encodings:
        matches = fr.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            face_distances = fr.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)
            print(matches, face_distances, best_match_index)
            if matches[best_match_index]:
                name = known_faces[best_match_index]

        # Do the save to DB here
        print(name)

# Feed location to uploaded file
def process(filename):
    img = get_image(filename)
    encodings = get_encodings(img)
    match_encodings(encodings)

process('images/sriram_2.jpg')


# TODO: Merge Multiple Encodings into one