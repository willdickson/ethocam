import inky
import font_fredoka_one
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict

class Display:

    def __init__(self,config):
        self.font_size = config['Display']['font_size']
        self.xpos_init = config['Display']['xpos_init']
        self.device = inky.auto()
        self.font = ImageFont.truetype(font_fredoka_one.FredokaOne, self.font_size)
        if self.device.colour == 'red':
            self.color = self.device.RED
        else:
            self.color = self.device.YELLOW

    def show(self, msg):
        image = Image.new("P",self.device.resolution)
        draw = ImageDraw.Draw(image)
        _, font_height = self.font.getsize('Sample Text')
        x, y = self.xpos_init, 0
        for item in msg:
            draw.text((x,y), item, self.device.BLACK, self.font)
            y += font_height 
        image = image.transpose(Image.ROTATE_180)
        self.device.set_border(self.color)
        self.device.set_image(image)
        self.device.show()

