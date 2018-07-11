import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import urllib
import requests
from PIL import Image
from io import BytesIO
from colormap import rgb2hex
from easydev.tools import check_param_in_list, swapdict, check_range


def get_hex(num_clusters, img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    ar = np.asarray(img)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    index_max = scipy.argmax(counts)
    peak = codes[index_max]

    return rgb2hex(int(peak[0]), int(peak[1]), int(peak[2]))


# counts = [10, 4, 22]
# codes = [(255, 0, 255), (0, 255,0), (0, 0, 255)]
# index_max = 2
# peak = (0, 0, 255)
