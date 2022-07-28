# import standard library
import sys

# import third party library
from OpenGL.GL import *

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute


# render six points in a hexagon arrangement
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

        ### set up vertex array object ###
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        ### set up vertex attribute ###
        self.positionData = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0],
                             [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0],
                             [-0.4, -0.6, 0.0], [0.4, -0.6, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

    def paintGL(self):
        super().paintGL()

        # select program to use when rendering
        glUseProgram(self.programRef)

        # renders geometric objects using selected program
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)
        #glDrawArrays(GL_LINES, 0, self.vertexCount)
        #glDrawArrays(GL_LINE_STRIP, 0, self.vertexCount)
        #glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
        #glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-3")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
