import os
import sys
from pprint import pprint

from PIL import Image, ImageDraw


import util


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")


img = os.path.join(DATA_DIR, "lg-2267728-aug-beethoven--page-2.png")
xml = os.path.join(DATA_DIR, "lg-2267728-aug-beethoven--page-2.xml")

bndboxes = util.xml2bndbox(xml)
# pprint(bndboxes)

# with Image.open(img) as img:
#     draw = ImageDraw.Draw(img)
#     img_size = img.size
#     for bndbox in bndboxes:
#         bndbox[1:] = util.relative2absolute(bndbox[1:], img_size)
#         print(bndbox)
#         draw.rectangle(bndbox[1:], outline="red")
#     img.show()

util.show_bndboxes(img, bndboxes, to_absolute=True)