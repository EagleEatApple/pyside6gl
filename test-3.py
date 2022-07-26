import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from core.OpenGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
import time
from math import sin, cos, pi

### initialize program ###
# vertex shader code
vsCode = """
in vec3 position;
uniform mat4 projectionMatrix;
uniform mat4 modelMatrix;
void main()
{
    gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
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

# move a triangle around the screen
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

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### Render settings ###
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        ### Set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)


        ### Set up vertex attribute: three points of triangle ###
        self.positionData = [[0.0, 0.2, 0.0], [0.1, -0.2, 0.0], [-0.1, -0.2, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

        ### set up uniforms ###
        mMatrix = Matrix.makeTranslation(0, 0, -1)
        self.modelMatrix = Uniform("mat4", mMatrix)
        self.modelMatrix.locateVariable(self.programRef, "modelMatrix")

        pMatrix = Matrix.makeIdentity()
        self.projectionMatrix = Uniform("mat4", pMatrix)
        self.projectionMatrix.locateVariable(self.programRef, "projectionMatrix")

        # movement speed, units per second
        self.moveSpeed = 0.5
        # rotation speed, radians per second
        self.turnSpeed = 90 * (pi / 180)

    def paintGL(self):
        # seconds since iteration of run loop
        self.deltaTime = time.time() - self.last_time
        # increment time application has been running
        self.time += self.deltaTime

        # update data
        moveAmount = self.moveSpeed * self.deltaTime
        turnAmount = self.turnSpeed * self.deltaTime

        #global translations
        if self.isKeyPressed(Qt.Key_W):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_S):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_A):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_D):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_Z):
            m = Matrix.makeTranslation(0, 0, moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_X):
            m = Matrix.makeTranslation(0, 0, -moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        #global rotation
        if self.isKeyPressed(Qt.Key_Q):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.isKeyPressed(Qt.Key_E):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        
        #local translation
        if self.isKeyPressed(Qt.Key_I):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.isKeyPressed(Qt.Key_K):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.isKeyPressed(Qt.Key_J):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.isKeyPressed(Qt.Key_L):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        #local rotation
        if self.isKeyPressed(Qt.Key_U):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.isKeyPressed(Qt.Key_O):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        
        ### render scene ###
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(self.programRef)
        self.projectionMatrix.uploadData()
        self.modelMatrix.uploadData()
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

