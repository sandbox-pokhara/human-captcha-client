import base64
from io import BytesIO

from PIL import Image
from PIL import ImageTk


def b64_to_tk(img: str):
    # remove the data:image/png;base64 portion of image
    img = img.split(",")[1]
    return ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(img))))
