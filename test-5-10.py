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
from extras.movementRig import MovementRig 
from extras.gridHelper import GridHelper

# render a basic scene
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        self.renderer = Renderer(self)
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 0.5, 3])
        self.scene.add(self.rig)
        
        crateGeometry = BoxGeometry()
        crateTexture = Texture("images/crate.png")
        crateMateril = TextureMaterial(crateTexture)
        crate = Mesh(crateGeometry, crateMateril)
        self.scene.add(crate)

        grid = GridHelper(gridColor=[1,1,1], centerColor=[1,1,0])
        grid.rotateX(-3.14 / 2)
        self.scene.add(grid)

        self.hudScene = Scene()
        self.hudCamera = Camera()
        self.hudCamera.setOrthographic(0, 800, 0, 600, 1, -1)
        labelGeo1 = RectangleGeometry(width=600, height=80, position=[0,600], alignment=[0,1])

        labelMat1 = TextureMaterial(Texture("images/crate-sim.png"))
        label1 = Mesh(labelGeo1, labelMat1)
        self.hudScene.add(label1)

        labelGeo2 = RectangleGeometry(width=400, height=80, position=[800,0], alignment=[1,0])
        labelMat2 = TextureMaterial(Texture("images/version-1.png"))
        label2 = Mesh(labelGeo2, labelMat2)
        self.hudScene.add(label2)

    def paintGL(self):
        super().paintGL()

        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-10")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
