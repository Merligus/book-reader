import base64
import io
import numpy as np
import cv2
from PIL import Image, ImageColor
from skimage.color import rgb2lab, rgba2rgb


# utility function to convert type of image
def base64_to_np(b64_img):
    base64_decoded = base64.b64decode(b64_img.split(",")[1])
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image, dtype=np.float32)
    
    # monochromatic
    if len(image_np.shape) == 2:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    
    # if alpha is included
    if image_np.shape[-1] > 3:
        image_np = rgba2rgb(image_np)
    return image_np

def numpy_to_base64(image) -> str:
    # Save image to a BytesIO object
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")

    # Encode to base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_str

def hex2lab(hex):
    rgb = ImageColor.getcolor(hex, "RGB")
    rgb = np.expand_dims(np.array(rgb), axis=0) / 255.0
    lab = rgb2lab(rgb)
    return lab[0]


def media_ponderada(input):
    return sum(x * y for x, y in input) / sum([percentage for lab, percentage in input])


def rgb2hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


RGB_SCALE = 255
CMYK_SCALE = 100


def rgb2cmyk(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return np.array([c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE])


def get_intermediate_indexes(colors_lab):
    all = np.arange(colors_lab.shape[0])
    id_max = np.argmax(colors_lab[:, 0], axis=0)
    id_min = np.argmin(colors_lab[:, 0], axis=0)
    elements_to_remove = [id_min, id_max]
    t = np.setdiff1d(all, elements_to_remove)
    return t
