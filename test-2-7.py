import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer
from core.OpenGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform

### initialize program ###
# vertex shader code
vsCode = """
in vec3 position;
uniform vec3 translation;
void main()
{
    vec3 pos = position + translation;
    gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
}
"""

# fragment shader code
fsCode = """
uniform vec3 baseColor;
out vec4 fragColor;
void main()
{
    fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
}
"""

# animate triangle moving across screen
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)

    def initializeGL(self):
        print ("Initializing program...")

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        # specify color used when clearly
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        
        ### set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)

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
        ### update data ###

        # increase x coordinate of translation
        self.translation.data[0] += 0.01
        # if triangle passes off-screen on the right,
        #    change translation so it reappears on the left
        if self.translation.data[0] > 1.2:
            self.translation.data[0] = -1.2
        ### render scene ###
        # reset color buffer with specified color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # using same program to render both shapes
        gl.glUseProgram(self.programRef)
        self.translation.uploadData()
        self.baseColor.uploadData()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)

        
def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

