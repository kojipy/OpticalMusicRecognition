from PIL import ImageDraw
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

