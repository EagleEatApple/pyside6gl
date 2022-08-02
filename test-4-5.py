# import standard library
import sys

# import third party library

# import local library
from core.base import Base, baseApp
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.sphereGeometry import SphereGeometry
from material.material import Material


# render a basic scene
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        self.renderer = Renderer(self)
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800 / 600)
        self.camera.setPosition([0, 0, 7])

        geometry = SphereGeometry(
            radius=3, radiusSegments=128, heightSegments=64)
        vsCode = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;
        uniform float time;
        void main()
        {
            float offset = 0.2 * sin(8.0 * vertexPosition.x + time);
            vec3 pos = vertexPosition + vec3(0.0, offset, 0.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos,1);
            color = vertexColor;
        }
        """

        fsCode = """
        in vec3 color;
        uniform float time;
        out vec4 fragColor;
        void main()
        {
            float r = abs(sin(time));
            vec4 c = vec4(r, -0.5*r, -0.5*r, 0.0);
            fragColor = vec4(color, 1.0) + c;
        }
        """

        material = Material(vsCode, fsCode)
        material.addUniform("float", "time", 0)
        material.locateUniforms()

        self.time = 0

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def paintGL(self):
        super().paintGL()
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.time += 1/60
        self.mesh.material.uniforms["time"].data = self.time
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-4-5")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
