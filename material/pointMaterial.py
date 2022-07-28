# import standard library

# import third party library
from OpenGL.GL import *

# import local library
from material.basicMaterial import BasicMaterial


class PointMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        # render vertices as points
        self.settings["drawStyle"] = GL_POINTS
        # Width and height of points in pixels
        self.settings["pointSize"] = 8
        # draw points as rounded
        self.settings["roundedPoints"] = False
        self.setProperties(properties)

    def updateRenderSettings(self):
        glPointSize(self.settings["pointSize"])

        if self.settings["roundedPoints"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)
