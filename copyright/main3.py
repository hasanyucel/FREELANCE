from pynter.pynter import generate_captioned
from PIL import Image

image_path = './qr.png'

im = generate_captioned('hasanyucel com'.upper(), image_path=image_path, font_path='./impact.ttf', filter_color=(0, 0, 0, 0))
im.show()
im.convert('RGB').save('drawn_image.jpg')