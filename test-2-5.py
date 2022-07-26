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
in vec3 vertexColor;
out vec3 color;
void main()
{
    gl_Position = vec4(position.x,
      position.y, position.z, 1.0);
    color = vertexColor;
}
"""

# fragment shader code
fsCode = """
in vec3 color;
out vec4 fragColor;
void main()
{
    fragColor = vec4(color.r, color.g, color.b, 1.0);
}
"""

# render shapes with vertext colors
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print ("Initializing program...")

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        gl.glPointSize(10)
        gl.glLineWidth(4)

        ### set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)

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
        # using same program to render both shapes
        gl.glUseProgram(self.programRef)

        #gl.glDrawArrays(gl.GL_POINTS, 0, self.vertexCount)
        #gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertexCount)
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, self.vertexCount)
        
def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

