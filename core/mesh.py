# import standard library

# import third party library
from OpenGL.GL import *

# import local library
from core.object3D import Object3D


class Mesh(Object3D):

    def __init__(self, geometry, material):
        super().__init__()

        self.geometry = geometry
        self.material = material

        # should this object be rendered?
        self.visible = True

        # set up associations between
        #   attributes stored in geometry and
        #   shader program stored in material
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)
        for variableName, attributeObject in geometry.attributes.items():
            attributeObject.associateVariable(
                material.programRef, variableName)
        # unbind vertex array object
        glBindVertexArray(0)
