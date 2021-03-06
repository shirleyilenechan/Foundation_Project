import face_recognition
from PIL import Image
import os


def crop_face(upload_folder, filename):
    """ returns the location of the face as [(x, x, x, x),(x, x, x, x)] """
    # specify the image file and use PIL library to open the image
    # encode the image into base64 in case we need byte data later
    image_file = os.path.join(upload_folder, filename)
    image_content = Image.open(image_file)

    # face_locations is a tuple that contains 4 pixels corresponding to the corners of the face
    # in the form of top, right, bottom, left
    image = face_recognition.load_image_file(image_file)
    face_locations = face_recognition.face_locations(image)

    # if there is no face in the image, return none
    # else, use PIL library to crop your image according to the 4 pixels specified in face_lcoations
    if len(face_locations) > 1:
        return None
    # if there are multiple faces in the image, return none, so that we can process this
    # as an invalid image
    elif len(face_locations) == 0:
        return None
    else:
        left = face_locations[0][3]
        top = face_locations[0][0]
        right = face_locations[0][1]
        bottom = face_locations[0][2]

        cropped_face = image_content.crop((left, top, right, bottom))

        return cropped_face
