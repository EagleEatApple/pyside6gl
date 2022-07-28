# import standard library

# import third party library
from OpenGL.GL import *

# import local library
from material.basicMaterial import BasicMaterial


class SurfaceMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        # render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES
        # render both sides? default: front side only
        # (vertices ordered counterclockwise)
        self.settings["doubleSide"] = False
        # render triangles as wireframe?
        self.settings["wireframe"] = False
        # line thickeness for wireframe rendering
        self.settings["lineWidth"] = 1
        self.setProperties(properties)

    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])
