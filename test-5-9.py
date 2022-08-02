# import standard library
import sys
from math import floor 

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
from material.spriteMaterial import SpriteMaterial 
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
        self.camera = Camera(aspectRatio=800 / 600)
        self.camera.setPosition([0, 0, 4])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 0.5, 3])
        self.scene.add(self.rig)

        geometry = RectangleGeometry()
        tileSet = Texture("images/rolling-ball.png")
        spriteMaterial = SpriteMaterial(tileSet, {
            "billboard":1,
            "tileCount":[4,4],
            "tileNumber":0
        })
        self.tilesPerSecond = 8
        self.sprite = Mesh(geometry, spriteMaterial)
        self.scene.add(self.sprite)

        grid = GridHelper()
        grid.rotateX(-3.1415*0.5)
        self.scene.add(grid)

    def paintGL(self):
        super().paintGL()

        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        tileNumber = floor(self.time * self.tilesPerSecond)
        self.sprite.material.uniforms["tileNumber"].data = tileNumber
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)



def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-5-9")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
