# import standard library
import sys

# import third party library

# import local library
from core.base import Base, baseApp
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from core.texture import Texture
from material.textureMaterial import TextureMaterial
from geometry.rectangleGeometry import RectangleGeometry
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
        self.camera.setPosition([0, 0, 1.5])

        vertexShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
        }
        """
        fragmentShaderCode = """
        uniform sampler2D texture1;
        uniform sampler2D texture2;
        in vec2 UV;
        uniform float time;
        out vec4 fragColor;

        void main()
        {
            vec4 color1 = texture2D(texture1, UV);
            vec4 color2 = texture2D(texture2, UV);
            float s = abs(sin(time));
            fragColor = s * color1 + (1.0 - s) * color2;
        }
        """

        gridTex = Texture("images/grid.png")
        crateTex = Texture("images/crate.png")
        self.blendMaterial = Material(vertexShaderCode, fragmentShaderCode)
        self.blendMaterial.addUniform("sampler2D", "texture1",[gridTex.textureRef, 1])
        self.blendMaterial.addUniform("sampler2D", "texture2",[crateTex.textureRef, 2])
        self.blendMaterial.addUniform("float", "time", 0.0)
        self.blendMaterial.locateUniforms()

        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, self.blendMaterial)
        self.scene.add(self.mesh)

    def paintGL(self):
        super().paintGL()
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.blendMaterial.uniforms["time"].data += self.deltaTime
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-4")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
