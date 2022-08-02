# import standard library


# import third party library
from OpenGL.GL import *
from PIL import Image
import numpy

# import local library


# use Pillow library to replace pygame to operate Image
class Texture(object):

    def __init__(self, fileName=None, properties={}):

        # store pixel data
        self.surface = None

        # reference of available texture from GPU
        self.textureRef = glGenTextures(1)

        # default property values
        self.properties = {
            "magFilter": GL_LINEAR,
            "minFilter": GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL_REPEAT
        }

        # overwrite defatult property values
        self.setProperties(properties)

        if fileName is not None:
            image = Image.open(fileName).transpose(Image.FLIP_TOP_BOTTOM)

            # store image dimansions
            self.width, self.height = image.size

            # convert image data to string buffer
            image = image.convert("RGBA")
            self.surface = numpy.asarray(image, dtype=numpy.uint8)
            self.uploadData()

    # set property values
    def setProperties(self, properties):
        for name, data in properties.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else:
                raise Exception("Texture has no property named: " + name)

    # upload pixel data to GPU
    def uploadData(self):
        glBindTexture(GL_TEXTURE_2D, self.textureRef)
        glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, self.width, self.height)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width,
                        self.height, GL_RGBA, GL_UNSIGNED_BYTE, self.surface)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        self.properties["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        self.properties["minFilter"])
