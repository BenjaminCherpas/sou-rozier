# -*- coding: utf-8 -*-

import os
import os.path
import sys
from PIL import Image


from photologue.utils import EXIF

# Orientation necessary mapped to EXIF data
# IMAGE_EXIF_ORIENTATION_MAP = {
#     1: 0,
#     8: 2,
#     3: 3,
#     6: 4,
# }

IMAGE_EXIF_ORIENTATION_MAP = {
    1: 0,
    8: 90,
    3: 180,
    6: 270,
}

def exif(path):
    try:
        return EXIF.process_file(open(path, 'rb'))
    except:
        try:
            return EXIF.process_file(open(path, 'rb'), details=False)
        except:
            return {}


def resize(dirname, filename):
    size = 600, 600

    fullname = os.path.join(dirname, filename)

    # dest_dir = os.path.absparg(__file__)
    # outname = os.path.join(dest_dir, 'resized', filename)

    dest_dir = os.path.join(dirname, 'resized')
    try:
        os.mkdir(dest_dir)
    except OSError:
        pass
    outname = os.path.join(dest_dir, filename)

    try:
        orientation = ""
        im = Image.open(fullname)

        if exif(fullname).get('Image Orientation', None) is not None:
            # print(">>", exif(fullname).get('Image Orientation', 1).values)
            orientation = IMAGE_EXIF_ORIENTATION_MAP[exif(fullname).get('Image Orientation', 1).values[0]]
            # im = im.transpose(orientation)
            im = im.rotate(orientation, expand=True)

        im.thumbnail(size, Image.ANTIALIAS)

        print(outname, orientation)

        im.save(outname, "PNG")
    except IOError as err:
        print("cannot create thumbnail for '{0}' : {1}".format(fullname, err))

dirname = sys.argv[1]
for filename in os.listdir(dirname):
    resize(dirname, filename)



