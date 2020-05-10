from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET


def relative2absolute(coords, img_size):
    """
    transform relative coordinates to absolute ones
    input 
        coords : object bndbox coordinate ordered [xmin, ymin, xmax, ymax]
        img_size : image size (width, height)
    """
    width, height = img_size
    coords[0] *= width
    coords[1] *= height
    coords[2] *= width
    coords[3] *= height
    return coords    
    

def corrds_to_centerAndWH(coord, img_size):
    """
    transform coords[(left-top X, left-top Y), (right-bottom X, right-bottom Y)]
    to [center-x, center-y, width, height] 
    coords : tuple
    """
    width    = coord[0] - coord[1]
    height   = coord[2] - coord[3]
    center_x = int(round(width / 2))
    center_y = int(round(height / 2))
    return [center_x, center_y, width, height]


def xml2bndbox(path):
    """
    input : xml annotation file path
    output : bndbox list [[name, xmin, xmax, ymin, ymax],
                          [name, xmin, xmax, ymin, ymax],
                                     , , ,              ]
    """
    def _sort(child):
        ground_truth = []

        # append class name of object
        ground_truth.append(child[0].text)

        # append coord objeect in the order of Xmin, Ymin, Xmax, Ymax
        ground_truth.append(float(child[1][0].text))    # Xmin
        ground_truth.append(float(child[1][2].text))    # Ymin
        ground_truth.append(float(child[1][1].text))    # Xmax
        ground_truth.append(float(child[1][3].text))    # Ymax

        return ground_truth

    tree = ET.parse(path)
    root = tree.getroot()
    
    bndboxes = [_sort(child) for child in root if child.tag == "object"]

    return bndboxes


def show_bndboxes(img, bndboxes, to_absolute=False):
    """
    show bounding boxes on PIL image. if coords values are relative (0~1) set 
    to_absolut=True
    input
        img : PIL image
        bndboxes : [[name, xmin, xmax, ymin, ymax],
                    [name, xmin, xmax, ymin, ymax],
                               , , ,              ]
        to_absolute : Boolean
    TODO : move font path to config file 
    """
    with Image.open(img) as img:
        draw = ImageDraw.Draw(img)
        path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
        font = ImageFont.truetype(path, size=13)
        img_size = img.size

        for bndbox in bndboxes:
            
            if to_absolute:
                bndbox[1:] = relative2absolute(bndbox[1:], img_size)

            class_name = bndbox[0]
            box = bndbox[1:]
            draw.rectangle(bndbox[1:], outline="red")
            left_top_on_the_bndbox = (box[0], box[1]-15)
            draw.text(left_top_on_the_bndbox, class_name, fill="red",
                      spacing=0, font=font)
        img.show()



