# import standard library
import sys

# import third party library
from OpenGL.GL import *

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute


# render two shapes
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        ### initialize program ###
        vsCode = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x,
                position.y, position.z, 1.0);
        }
        """

        fsCode = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        glLineWidth(4)

        ### set up vertex array object - triangle ###
        self.vaoTri = glGenVertexArrays(1)
        glBindVertexArray(self.vaoTri)
        self.positionDataTri = [[-0.5, 0.8, 0.0], [-0.2, 0.2, 0.0],
                                [-0.8, 0.2, 0.0]]
        self.vertexCountTri = len(self.positionDataTri)
        self.positionAttributeTri = Attribute("vec3", self.positionDataTri)
        self.positionAttributeTri.associateVariable(
            self.programRef, "position")

        ### set up vertex array object - square ###
        self.vaoSquare = glGenVertexArrays(1)
        glBindVertexArray(self.vaoSquare)
        self.positionDataSquare = [[0.8, 0.8, 0.0], [0.8, 0.2, 0.0],
                                   [0.2, 0.2, 0.0], [0.2, 0.8, 0.0]]
        self.vertexCountSquare = len(self.positionDataSquare)
        self.positionAttributeSquare = Attribute(
            "vec3", self.positionDataSquare)
        self.positionAttributeSquare.associateVariable(
            self.programRef, "position")

    def paintGL(self):
        super().paintGL()

        # select program to use when rendering
        glUseProgram(self.programRef)

        # draw the triangle
        glBindVertexArray(self.vaoTri)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountTri)

        # draw the triangle
        glBindVertexArray(self.vaoSquare)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountSquare)


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-4")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
