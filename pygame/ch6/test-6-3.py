from core.base import Base
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
from extras.movementRig import MovementRig
from extras.postprocessor import Postprocessor 
from effects.tintEffect import TintEffect
from effects.colorReduceEffect import ColorReduceEffect
from effects.pixelateEffect import PixelateEffect
from effects.brightFilterEffect import BrightFilterEffect
from effects.horizontalBlurEffect import HorizontalBlurEffect
from effects.verticalBlurEffect import VerticalBlurEffect
from effects.additiveBlendEffect import AdditiveBlendEffect

# render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")

        self.renderer = Renderer(clearColor=[0, 0, 0])
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 4])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0, 1, 4])
        skyGeometry = SphereGeometry(radius=50)
        skyMaterial = TextureMaterial(Texture("images/sky-earth.jpg"))
        sky = Mesh(skyGeometry, skyMaterial)
        self.scene.add(sky)
        grassGeometry = RectangleGeometry(width=100, height=100)
        grassMaterial = TextureMaterial(
            Texture("images/grass.jpg"), {"repeatUV": [50, 50]})
        grass = Mesh(grassGeometry, grassMaterial)
        grass.rotateX(-3.14/2)
        self.scene.add(grass)

        sphereGeometry = SphereGeometry()
        sphereMaterial = TextureMaterial(Texture("images/grid.png"))
        self.sphere = Mesh(sphereGeometry, sphereMaterial)
        self.sphere.setPosition([0, 1, 0])
        self.scene.add(self.sphere)

        self.postprocessor = Postprocessor(
            self.renderer, self.scene, self.camera)

        # combined effects to create light bloom
        self.postprocessor.addEffect(BrightFilterEffect(2.4))
        self.postprocessor.addEffect(HorizontalBlurEffect(
            textureSize=[800, 600], blurRadius=50))
        self.postprocessor.addEffect(VerticalBlurEffect(
            textureSize=[800, 600], blurRadius=50))
        mainScene = self.postprocessor.renderTargetList[0].texture
        self.postprocessor.addEffect(AdditiveBlendEffect(
            mainScene, originalStrength=2, blendStrength=1))


    def update(self):
        self.rig.update(self.input, self.deltaTime)
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.postprocessor.render()


# inistantiate this class and run the program
Test(screenSize=[800, 600]).run()
