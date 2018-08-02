import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import urllib
import requests
from PIL import Image
from io import BytesIO
from colormap import rgb2hex, hex2rgb
from easydev.tools import check_param_in_list, swapdict, check_range
from skimage.color import rgb2lab, deltaE_cie76


def get_hex_url(num_clusters, img_url):
    """return the dominant hex code for an image--from url"""

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    get_hex(num_clusters, img)


def get_hex(num_clusters, img):
    """return the dominant hex code for an image"""

    # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image/3242290
    np.random.seed(42)
    # turn image into numpy array
    ar = np.asarray(img)
    # (num_row, num_column, num_colors)
    shape = ar.shape
    # (num_pixel, num_color)
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # create center for each color cluster, in the number of clusters specified in the param
    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

    # determine the which pixel belongs to which cluster based on the distance
    # between the pixel and the culster center
    vecs, dist = scipy.cluster.vq.vq(ar, codes)

    # gives us the number of pixels that belong in each cluster
    counts, bins = scipy.histogram(vecs, num_clusters)

    # find the index of the cluster that has the most pixels
    index_max = scipy.argmax(counts)

    # find which cluster is at that index
    peak = codes[index_max]

    return rgb2hex(int(peak[0]), int(peak[1]), int(peak[2]))


def match_foundation_shade(face_hex, foundation_hex_lst):
    """return the 6 closest distance hex codes"""

    # https://stackoverflow.com/questions/44428315/similar-color-detection-in-python

    # turn face_hex into rgb
    face_rgb = hex2rgb(face_hex)
    # turn this rgb color into a numpy array
    face_arr = np.uint8(np.asarray([[face_rgb]]))
    # convert to lab space
    face_lab = rgb2lab(face_arr)

    rgb_lst = []
    # append each rgb color to a list
    for hex_code in foundation_hex_lst:
        foundation_rgb = hex2rgb(hex_code)
        rgb_lst.append(foundation_rgb)

    # make this spectrum of foundation colors a numpy array
    foundation_arr = np.uint8(np.asarray([rgb_lst]))

    #convert the array to lab space
    foundation_lab = rgb2lab(foundation_arr)

    # get the distance between the face and each foundation color in the lab space
    distance_colors = deltaE_cie76(face_lab, foundation_lab)

    # sort the distance from smallest to biggest
    # the distance will not correspond with your foundation_hex_lst
    # so we have to use argsort, indexes where the distance was before we sorted it
    # back when the distance corresponded with the foundation hex list
    sort_distance = np.argsort(distance_colors)

    sort_distance = sort_distance.squeeze()

    # list of the indexes of the top 6 closest distances, where they were when they lined up
    # with the foundation_hex_lst
    closest_6 = sort_distance[0:6]

    top_6_hex = []

    # no we have to find out which foundation corresponds to these indexes
    for index in closest_6:
        top_6_hex.append(foundation_hex_lst[index])

    return top_6_hex
