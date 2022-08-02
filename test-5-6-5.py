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

        vsCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;

        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            UV = vertexUV;
        }
        """

        fsCode = """
        // return a random value in [0, 1]
        float random(vec2 UV)
        {
            return fract(235711.0 * sin(14.337*UV.x + 42.418*UV.y));
        }

        float boxRandom(vec2 UV, float scale)
        {
            vec2 iScaleUV = floor(scale * UV);
            return random(iScaleUV);
        }

        float smoothRandom(vec2 UV, float scale)
        {
            vec2 iScaleUV = floor(scale * UV);
            vec2 fScaleUV = fract(scale * UV);
            float a = random(iScaleUV);
            float b = random(round(iScaleUV + vec2(1, 0)));
            float c = random(round(iScaleUV + vec2(0, 1)));
            float d = random(round(iScaleUV + vec2(1, 1)));
            return mix(mix(a, b, fScaleUV.x), mix(c, d, fScaleUV.x), fScaleUV.y);
        }

        // add smooth random values at different scales
        //   wighted (amplitudes) so that sum is approximately 1.0
        float fractalRandom(vec2 UV, float scale)
        {
            float value = 0.0;
            float amplitude = 0.5;

            for (int i = 0; i < 6; i++)
            {
                value += amplitude * smoothRandom(UV, scale);
                scale *= 2.0;
                amplitude *= 0.5;
            }

            return value;
        }

        in vec2 UV;
        out vec4 fragColor;
        // lava
        void main()
        {
            float r = fractalRandom(UV, 40); 
            vec4 color1 = vec4(1, 0.8, 0, 1); 
            vec4 color2 = vec4(0.8, 0, 0, 1); 
            fragColor = mix(color1, color2, r);  
        }
        """

        material = Material(vsCode, fsCode)
        material.locateUniforms()

        geometry = RectangleGeometry()
        mesh = Mesh(geometry, material)
        self.scene.add(mesh)

    def paintGL(self):
        super().paintGL()
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-6-5")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
