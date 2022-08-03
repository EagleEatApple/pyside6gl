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
from geometry.sphereGeometry  import SphereGeometry 
from light.ambientLight import AmbientLight 
from light.directionalLight import DirectionalLight 
from light.pointLight import PointLight 
from material.flatMaterial  import FlatMaterial 
from material.lambertMaterial import LambertMaterial 
from material.phongMaterial import PhongMaterial 


# render a basic scene
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        self.renderer = Renderer(self)
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800 / 600)
        self.camera.setPosition([0, 0, 4])

        geometry = BoxGeometry()
        material = SurfaceMaterial(
            {"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def paintGL(self):
        super().paintGL()
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-template")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
