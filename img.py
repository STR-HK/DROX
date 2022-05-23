from PIL import Image, ImageQt
from io import BytesIO

from requests import request
import requests

r = requests.get("https://www.python.org/static/img/python-logo.png")

im = Image.open(BytesIO(r.content))
im2 = im.crop(
    (
        int((im.width - im.height) / 2),
        0,
        int((im.width - im.height) / 2) + im.height,
        im.height,
    )
)
