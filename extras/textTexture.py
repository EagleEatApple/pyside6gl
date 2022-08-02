# import standard library

# import third party library
from PIL import Image, ImageDraw, ImageFont
import numpy

# import local library
from core.texture import Texture


class TextTexture(Texture):
    def __init__(self, text="Enter text here!", systemFontName="arial",
                 fontFileName=None, fontSize=24, fontColor=(0, 0, 0),
                 backgroundColor=(255, 255, 255), transparent=False,
                 imageWidth=None, imageHeight=None, alignHorizontal=0.0,
                 alignVertical=0.0, imageBorderWidth=0, imageBorderColor=(0, 0, 0)):
        super().__init__()

        # default font, can override by loading font file
        self.font = ImageFont.truetype(systemFontName + ".ttf", fontSize)

        if fontFileName is not None:
            self.font = ImageFont.truetype(fontFileName, fontSize)
        else:
            self.font = ImageFont.truetype(systemFontName + ".ttf", fontSize)
            if self.font is None:
                raise Exception("Cannot find the font: " + systemFontName)
        # determine size of rendered text for aligment purpose
        self.textWidth, self.textHeight = self.font.getsize(text)

        # if image dimensions are not specified use font surface size default
        if imageWidth is None:
            imageWidth = self.textWidth
        if imageHeight is None:
            imageHeight = self.textHeight
        self.width = imageWidth
        self.height = imageHeight

        # alignHorizontal, alignVertical are percentages,
        # measured from top-left corner
        cornerPoint = (alignHorizontal * (imageWidth-self.textWidth),
                       alignVertical * (imageHeight-self.textHeight))

        # create surface to store image of text
        image = Image.new(
            'RGBA', size=[imageWidth, imageHeight], color=backgroundColor)
        draw = ImageDraw.Draw(image)
        draw.text(cornerPoint, text, font=self.font, fill=fontColor)
        draw.rectangle([(0, 0), (imageWidth, imageHeight)],
                       outline=imageBorderColor, width=imageBorderWidth)

        temp = numpy.asarray(image, dtype=numpy.uint8)
        # Flip so text is right side up
        self.surface = temp[::-1, :, :]
        self.uploadData()
