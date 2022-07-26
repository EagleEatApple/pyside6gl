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

# render six points in a hexagon arrangement
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print ("Initializing program...")

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        gl.glLineWidth(4)

        ### set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)

        ### set up vertex attribute ###
        self.positionData = [[0.8, 0.0, 0.0], [0.4, 0.6, 0.0],
                             [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0],
                             [-0.4, -0.6, 0.0], [0.4, -0.6, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

    def paintGL(self):
        # select program to use when rendering
        gl.glUseProgram(self.programRef)
        
        # renders geometric objects using selected program
        #gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertexCount)
        #gl.glDrawArrays(gl.GL_LINES, 0, self.vertexCount)
        #gl.glDrawArrays(gl.GL_LINE_STRIP, 0, self.vertexCount)
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, self.vertexCount)
        

def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

