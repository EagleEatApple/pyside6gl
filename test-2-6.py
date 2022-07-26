import sys
from OpenGL import GL as gl
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
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

# render tow triangles with different positions and colors
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

        ### set up vertex attributes ###
        self.positionData = [[0.0, 0.2, 0.0], [0.2, -0.2, 0.0],
                             [-0.2, -0.2, 0.0]]
        self.vertexCount = len(self.positionData)
        self.positionAttribute = Attribute("vec3", self.positionData)
        self.positionAttribute.associateVariable(self.programRef, "position")

        ### set up uniform ###
        self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation1.locateVariable(self.programRef, "translation")

        self.translation2 = Uniform("vec3",[0.5, 0.0, 0.0])
        self.translation2.locateVariable(self.programRef, "translation")

        self.baseColor1 = Uniform("vec3", [1.0, 0.0, 0.0])
        self.baseColor1.locateVariable(self.programRef, "baseColor")

        self.baseColor2 = Uniform("vec3", [0.0, 0.0, 1.0])
        self.baseColor2.locateVariable(self.programRef, "baseColor")


    def paintGL(self):
        # using same program to render both shapes
        gl.glUseProgram(self.programRef)

        # draw the first triangle
        self.translation1.uploadData()
        self.baseColor1.uploadData()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)
        # draw the second triangle
        self.translation2.uploadData()
        self.baseColor2.uploadData()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertexCount)
        
def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

