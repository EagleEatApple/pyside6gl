# import standard library
import sys

# import third party library

# import local library
from core.base import Base, baseApp
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig
from extras.postprocessor import Postprocessor
from effects.vignetteEffect import VignetteEffect


# render a basic scene
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()
        self.renderer = Renderer(self)
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
        self.postprocessor.addEffect(VignetteEffect())

    def paintGL(self):
        super().paintGL()

        self.rig.update(self.input, self.deltaTime)
        self.postprocessor.render()


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-12-3")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
