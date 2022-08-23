from PIL import Image, ImageDraw, ImageFont


img_src = Image.open('kodlama.jpg') #open your original image
xsize, ysize = img_src.size #get it's width
img_text = Image.new("RGB",(xsize,ysize+30)) #create a new image that's just a little bit taller than the src image
img_text.paste(img_src,(0,0)) #paste the old image into the new one, flush at the top



font = ImageFont.truetype("impact.ttf", 10) #Load font, draw to the bottom of the new image
draw = ImageDraw.Draw(img_text)
draw.text((0, xsize),"hasanyucel.com",(100,100,100),font=font)

img_text.save("appended_image5.jpg")