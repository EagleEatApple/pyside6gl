# import standard library
import sys

# import third party library
from OpenGL.GL import *

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute


# render shapes with vertext colors
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        ### initialize program ###
        vsCode = """
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;
        void main()
        {
            gl_Position = vec4(position.x,
                position.y, position.z, 1.0);
            color = vertexColor;
        }
        """

        fsCode = """
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        glPointSize(10)
        glLineWidth(4)

        ### set up vertex array object ###
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        ### set up vertex attributes ###
        self.positionData = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0],
                             [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0],
                             [-0.4, -0.6, 0.0], [0.4, -0.6, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")
        self.colorData = [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0],
                          [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0], [0.5, 0.0, 1.0]]
        self.colorAttribute = Attribute("vec3", self.colorData)
        self.colorAttribute.associateVariable(self.programRef, "vertexColor")

    def paintGL(self):
        super().paintGL()

        # select program to use when rendering
        glUseProgram(self.programRef)

        glDrawArrays(GL_POINTS, 0, self.vertexCount)
        #glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)
        #glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-5")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
