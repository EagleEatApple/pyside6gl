# import standard library
import sys
from math import pi

# import third party library
from OpenGL import GL as gl
from PySide6.QtCore import Qt

# import local library
from core.base import Base, baseApp
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from core.input import Input


# move a triangle around the screen
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)
        self.input = Input()

    def initializeGL(self):
        super().initializeGL()

        ### initialize program ###
        vsCode = """
        in vec3 position;
        uniform mat4 projectionMatrix;
        uniform mat4 modelMatrix;
        void main()
        {
            gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
        }
        """

        fsCode = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### Render settings ###
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)

        ### Set up vertex array object ###
        self.vaoRef = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vaoRef)

        ### Set up vertex attribute: three points of triangle ###
        self.positionData = [[0.0, 0.2, 0.0], [
            0.1, -0.2, 0.0], [-0.1, -0.2, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

        ### set up uniforms ###
        mMatrix = Matrix.makeTranslation(0, 0, -1)
        self.modelMatrix = Uniform("mat4", mMatrix)
        self.modelMatrix.locateVariable(self.programRef, "modelMatrix")

        pMatrix = Matrix.makeIdentity()
        self.projectionMatrix = Uniform("mat4", pMatrix)
        self.projectionMatrix.locateVariable(
            self.programRef, "projectionMatrix")

        # movement speed, units per second
        self.moveSpeed = 0.5
        # rotation speed, radians per second
        self.turnSpeed = 90 * (pi / 180)

    def paintGL(self):
        super().paintGL()
        self.input.update()

        # update data
        moveAmount = self.moveSpeed * self.deltaTime
        turnAmount = self.turnSpeed * self.deltaTime

        #global translations
        if self.input.isKeyPressed(Qt.Key_W):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_S):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_A):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_D):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_Z):
            m = Matrix.makeTranslation(0, 0, moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_X):
            m = Matrix.makeTranslation(0, 0, -moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data

        #global rotation
        if self.input.isKeyPressed(Qt.Key_Q):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(Qt.Key_E):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data

        # local translation
        if self.input.isKeyPressed(Qt.Key_I):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(Qt.Key_K):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(Qt.Key_J):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(Qt.Key_L):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        # local rotation
        if self.input.isKeyPressed(Qt.Key_U):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(Qt.Key_O):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m

        ### render scene ###
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(self.programRef)
        self.projectionMatrix.uploadData()
        self.modelMatrix.uploadData()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)

    def keyPressEvent(self, event):
        self.input.receiveKeyEvent(event.key(), event.type())
        self.update()

    def keyReleaseEvent(self, event):
        self.input.receiveKeyEvent(event.key(), event.type())
        self.update()


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-3")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
