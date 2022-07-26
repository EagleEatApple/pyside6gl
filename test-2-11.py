import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from core.OpenGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
import time

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

# animate triangle moving along a circular path
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphics Window")
        self.setFixedSize(512, 512)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
        self.time = 0
        self.KeyDownList = []
        self.keyPressedList = []
        self.keyUpList = []
        self.speed = 0.5

    def initializeGL(self):
        print ("Initializing program...")
        self.last_time = time.time()

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
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
        # seconds since iteration of run loop
        self.deltaTime = time.time() - self.last_time
        # increment time application has been running
        self.time += self.deltaTime

        ### update data ###
        distance = self.speed * self.deltaTime
        # distance = 0.01

        if self.isKeyPressed(Qt.Key_Left):
            self.translation.data[0] -= distance
        if self.isKeyPressed(Qt.Key_Right):
            self.translation.data[0] += distance
        if self.isKeyPressed(Qt.Key_Down):
            self.translation.data[1] -= distance
        if self.isKeyPressed(Qt.Key_Up):
            self.translation.data[1] += distance

        ### render scene ###
        # reset color buffer with specified color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # using same program to render both shapes
        gl.glUseProgram(self.programRef)
        self.translation.uploadData()
        self.baseColor.uploadData()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)
        self.last_time = time.time()

    def keyPressEvent(self, event):
        keyName = event.key()
        self.KeyDownList.append(keyName)
        self.keyPressedList.append(keyName)
        self.update()

    def keyReleaseEvent(self, event):
        keyName = event.key()
        self.keyPressedList.remove(keyName)
        self.keyUpList.append(keyName)
        self.update()
    
    # functions to check key states
    def isKeyDown(self, keyCode):
        return keyCode in self.KeyDownList
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList

        
def main():
    app = QApplication(sys.argv)

    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

