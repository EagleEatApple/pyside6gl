import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from core.OpenGLUtils import OpenGLUtils

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

# render a single point
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print ("Initializing program...")

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)

        ### render settings (optional) ###

        # set point width and height
        gl.glPointSize(10)

    def paintGL(self):
        # select program to use when rendering
        gl.glUseProgram(self.programRef)
        
        # renders geometric objects using selected program
        gl.glDrawArrays(gl.GL_POINTS, 0, 1)

def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

