import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from core.OpenGLUtils import OpenGLUtils
from core.attribute import Attribute

### initialize program ###
# vertex shader code
vsCode = """
in vec3 position;
void main()
{
  gl_Position = vec4(position.x,
      position.y, position.z, 1.0);
}
"""

# fragment shader code
fsCode = """
out vec4 fragColor;
void main()
{
  fragColor = vec4(1.0, 1.0, 0.0, 1.0);
}
"""

# render two shapes
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print ("Initializing program...")

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        gl.glLineWidth(4)

        ### set up vertex array object - triangle ###
        self.vaoTri = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoTri)
        self.positionDataTri = [[-0.5, 0.8, 0.0], [-0.2, 0.2, 0.0],
                            [-0.8, 0.2, 0.0]]
        self.vertexCountTri = len(self.positionDataTri)
        self.positionAttributeTri = Attribute("vec3", self.positionDataTri)
        self.positionAttributeTri.associateVariable(self.programRef, "position")

        ### set up vertex array object - square ###
        self.vaoSquare = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoSquare)
        self.positionDataSquare = [[0.8, 0.8, 0.0], [0.8, 0.2, 0.0],
                            [0.2, 0.2, 0.0], [0.2, 0.8, 0.0]]
        self.vertexCountSquare = len(self.positionDataSquare)
        self.positionAttributeSquare = Attribute("vec3", self.positionDataSquare)
        self.positionAttributeSquare.associateVariable(self.programRef, "position")

    def paintGL(self):
        # using same program to render both shapes
        gl.glUseProgram(self.programRef)
        
        # draw the triangle
        gl.glBindVertexArray(self.vaoTri)
        gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertexCountTri)

        # draw the triangle
        gl.glBindVertexArray(self.vaoSquare)
        gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertexCountSquare)


def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

