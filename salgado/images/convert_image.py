from io import BytesIO
import uuid
from django.core.files import File
from PIL import Image

BASE_WIDTH = 640
BASE_HEIGHT = 384

PALLETE = [
    0, 0, 0,
    255, 0, 0,
    255, 255, 255,
] + [0,] * 253 * 3

def resize_and_convert(image):
    """Makes thumbnails of given size from given image"""

    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(PALLETE)

    im = Image.open(image)
    im.convert('RGB') # convert mode

    if im.height > im.width:
        print("transposing image")
        im = im.transpose(Image.ROTATE_90)
    
    im.thumbnail((BASE_WIDTH, BASE_HEIGHT), Image.ANTIALIAS) # resize image
    im = im.quantize(palette=pimage)

    thumb_io = BytesIO() # create a BytesIO object

    im.save(thumb_io, 'BMP') # save image to BytesIO object

    thumbnail = File(thumb_io, name=f"{uuid.uuid4()}.bmp") # create a django friendly File object

    return thumbnail