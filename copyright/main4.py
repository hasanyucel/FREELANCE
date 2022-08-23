from PIL import Image, ImageDraw, ImageFont

caption = 'hasanyucel.com'
img = Image.open('./drawn_image.jpg')
xsize, ysize = img.size 
d = ImageDraw.Draw(img)
font = ImageFont.truetype('impact.ttf', size = 30)

d.text((xsize - 220, ysize - 50), caption, fill='white', font=font, stroke_width=2, stroke_fill='black')
img.save('example-output.jpg')