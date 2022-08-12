from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
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

    def initialize(self):
        print("Initializing program...")

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 2.5])

        ambientLight = AmbientLight(color=[0.3, 0.3, 0.3])
        self.scene.add(ambientLight)
        self.pointLight = PointLight(color=[1, 1, 1], position=[1.2, 1.2, 0.3])
        self.scene.add(self.pointLight)

        colorTex = Texture("images/brick-color.png")
        bumpTex = Texture("images/brick-bump.png")

        geometry = RectangleGeometry(width=2, height=2)

        bumpMaterial = LambertMaterial(texture=colorTex,
                                       bumpTexture=bumpTex, properties={"bumpStrength": 1})

        mesh = Mesh(geometry, bumpMaterial)
        self.scene.add(mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)


# inistantiate this class and run the program
Test(screenSize=[800, 600]).run()
