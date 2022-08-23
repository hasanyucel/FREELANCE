from PIL import Image, ImageDraw, ImageFont
import textwrap

class Meme:

    basewidth = 1200            #Width to make the meme
    fontBase = 100              #Font size
    letSpacing = 9              #Space between letters
    fill = (255, 255, 255)      #TextColor
    stroke_fill = (0,0,0)       #Color of the text outline
    lineSpacing = 10            #Space between lines
    stroke_width=9              #How thick the outline of the text is
    fontfile = './impact.ttf'

    def __init__(self, caption, image):
        self.img = self.createImage(image)
        self.d = ImageDraw.Draw(self.img)

        self.splitCaption = textwrap.wrap(caption, width=20)  # The text can be wider than the img. If thats the case split the text into multiple lines
        self.splitCaption.reverse()                           # Draw the lines of text from the bottom up

        fontSize = self.fontBase+10 if len(self.splitCaption) <= 1 else self.fontBase   #If there is only one line, make the text a bit larger
        self.font = ImageFont.truetype(font=self.fontfile, size=fontSize)
        # self.shadowFont = ImageFont.truetype(font='./impact.ttf', size=fontSize+10)

    def draw(self):
        '''
        Draws text onto this objects img object
        :return: A pillow image object with text drawn onto the image
        '''
        (iw, ih) = self.img.size
        (_, th) = self.d.textsize(self.splitCaption[0], font=self.font) #Height of the text
        y = (ih - (ih / 10)) - (th / 2) #The starting y position to draw the last line of text. Text in drawn from the bottom line up

        for cap in self.splitCaption:   #For each line of text
            (tw, _) = self.d.textsize(cap, font=self.font)  # Getting the position of the text
            x = ((iw - tw) - (len(cap) * self.letSpacing))/2  # Center the text and account for the spacing between letters

            self.drawLine(x=x, y=y, caption=cap)
            y = y - th - self.lineSpacing  # Next block of text is higher up

        wpercent = ((self.basewidth/2) / float(self.img.size[0]))
        hsize = int((float(self.img.size[1]) * float(wpercent)))
        return self.img.resize((int(self.basewidth/2), hsize))

    def createImage(self, image):
        '''
        Resizes the image to a resonable standard size
        :param image: Path to an image file
        :return: A pil image object
        '''
        img = Image.open(image)
        wpercent = (self.basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        return img.resize((self.basewidth, hsize))

    def drawLine(self, x, y, caption):
        '''
        The text gets split into multiple lines if it is wider than the image. This function draws a single line
        :param x: The starting x coordinate of the text
        :param y: The starting y coordinate of the text
        :param caption: The text to write on the image
        :return: None
        '''
        for idx in range(0, len(caption)):  #For each letter in the line of text
            char = caption[idx]
            w, h = self.font.getsize(char)  #width and height of the letter
            self.d.text(
                (x, y),
                char,
                fill=self.fill,
                stroke_width=self.stroke_width,
                font=self.font,
                stroke_fill=self.stroke_fill
            )  # Drawing the text character by character. This way spacing can be added between letters
            x += w + self.letSpacing #The next character must be drawn at an x position more to the right



caption = "Now I Have a Caption"
image = './2.png'
outputImage = './my_captioned_image.jpg'

meme = Meme(caption, image)
img = meme.draw()
if img.mode in ("RGBA", "P"):   #Without this the code can break sometimes
    img = img.convert("RGB")
img.save(outputImage, optimize=True, quality=80)    #Save with some image optimization