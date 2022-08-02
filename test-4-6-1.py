# import standard library
import sys
from math import pi

# import third party library

# import local library
from core.base import Base, baseApp
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig


# render axes
class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

        self.renderer = Renderer(self)
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800 / 600)
        self.camera.setPosition([0.5, 1, 5])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0.5, 1, 5])
        self.scene.add(self.rig)

        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)

        grid = GridHelper(size=20, gridColor=[1, 1, 1], centerColor=[1, 1, 0])
        grid.rotateX(-pi*0.5)
        self.scene.add(grid)

    def paintGL(self):
        super().paintGL()

        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-4-6-1")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
