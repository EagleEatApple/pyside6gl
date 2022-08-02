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
from core.matrix import Matrix 
from extras.textTexture import TextTexture 
from extras.movementRig import MovementRig 
from geometry.rectangleGeometry import RectangleGeometry 


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

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0,1,5])
        self.scene.add(self.rig)

        labelTexture = TextTexture(text="This is a Crate.", systemFontName="arial",
                                    fontSize=40, fontColor=(0,0,200), imageWidth=256, 
                                    imageHeight=128, alignHorizontal=0.5, alignVertical=0.5,
                                    imageBorderWidth=4, imageBorderColor=(255,0,0))
        labelMaterial = TextureMaterial(labelTexture)
        labelGeometry = RectangleGeometry(width=1, height=0.5)
        labelGeometry.applyMatrix(Matrix.makeRotationY(3.14))
        self.label = Mesh(labelGeometry, labelMaterial)
        self.label.setPosition([0,1,0])
        self.scene.add(self.label)

        crateGeometry = BoxGeometry()
        crateTexture = Texture("images/crate.png")
        crateMaterial = TextureMaterial(crateTexture)
        crate = Mesh(crateGeometry, crateMaterial)
        self.scene.add(crate)

    def paintGL(self):
        super().paintGL()

        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.rig.update(self.input, self.deltaTime)
        self.label.lookAt(self.camera.getWorldPosition())
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-8")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
