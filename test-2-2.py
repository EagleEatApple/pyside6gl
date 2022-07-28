# import standard library
import sys

# import third party library
from OpenGL.GL import *

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils



# render a single point
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        ### initialize program ###

        # vertex shader code
        vsCode = """
        void main()
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
        }
        """

        # fragment shader code
        fsCode = """
        void main()
        {
            gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### set up vertex array object ###
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        ### render settings (optional) ###

        # set point width and height
        glPointSize(10)

    def paintGL(self):
        super().paintGL()

        # select program to use when rendering
        glUseProgram(self.programRef)

        # renders geometric objects using selected program
        glDrawArrays(GL_POINTS, 0, 1)


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-2")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
