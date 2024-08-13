import sys
import inky
import font_fredoka_one
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict

class Display:

    def __init__(self,config):
        self.font_size = config['Display'].getint('font_size')
        self.xpos_init = config['Display'].getint('xpos_init')
        self.enabled = config['Display'].getboolean('enabled')
        if self.enabled:
            try:
                self.device = inky.auto()
            except RuntimeError as e:
                print('Display: {}'.format(e), file=sys.stderr)
                self.enabled = False
        if self.enabled:
           self.font = ImageFont.truetype(font_fredoka_one.FredokaOne, self.font_size)
           if self.device.colour == 'red':
               self.color = self.device.RED
           else:
               self.color = self.device.YELLOW

    def show(self, msg):
        if self.enabled:
            image = Image.new("P",self.device.resolution)
            draw = ImageDraw.Draw(image)
            # _, font_height = self.font.getsize('Sample Text')
            x, y = self.xpos_init, 0
            for item in msg:
                draw.text((x,y), item, self.device.BLACK, self.font)
                y += self.font_size
            image = image.transpose(Image.ROTATE_180)
            self.device.set_border(self.color)
            self.device.set_image(image)
            self.device.show()


