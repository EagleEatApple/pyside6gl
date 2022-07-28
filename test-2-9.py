# import standard library
import sys
from math import sin, cos

# import third party library
from OpenGL.GL import *

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform


# animate the color shifting of the triangle
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        ### initialize program ###
        vsCode = """
        in vec3 position;
        uniform vec3 translation;
        void main()
        {
            vec3 pos = position + translation;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """

        fsCode = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###

        # specify color used when clearly
        glClearColor(0.0, 0.0, 0.0, 1.0)

        ### set up vertex array object ###
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        ### set up vertex attributes ###
        self.positionData = [[0.0, 0.2, 0.0], [0.2, -0.2, 0.0],
                             [-0.2, -0.2, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

        ### set up uniforms ###
        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation.locateVariable(self.programRef, "translation")
        self.baseColor = Uniform("vec3", [1.0, 0.0, 0.0])
        self.baseColor.locateVariable(self.programRef, "baseColor")

    def paintGL(self):
        super().paintGL()

        ### update data ###

        # self.baseColor.data[0] = (sin(3 * (self.time)) + 1) / 2
        self.baseColor.data[0] = (sin(3 * (self.time)) + 1) / 2
        self.baseColor.data[1] = (sin(3 * (self.time)) + 2.1) / 2
        self.baseColor.data[2] = (sin(3 * (self.time)) + 4.2) / 2

        ### render scene ###
        # reset color buffer with specified color
        glClear(GL_COLOR_BUFFER_BIT)

        # using same program to render both shapes
        glUseProgram(self.programRef)
        self.translation.uploadData()
        self.baseColor.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-9")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
