# import standard library
import sys
from math import sin

# import third party library
from numpy import arange

# import local library
from core.base import Base, baseApp
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial


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

        geometry = Geometry()
        posData = []
        for x in arange(-3.2, 3.2, 0.3):
            posData.append([x, sin(x), 0])
        geometry.addAttribute("vec3", "vertexPosition", posData)
        geometry.countVertices()

        pointMaterial = PointMaterial(
            {"baseColor": [1, 1, 0], "pointSize": 10})
        pointMesh = Mesh(geometry, pointMaterial)

        lineMaterial = LineMaterial({"baseColor": [1, 0, 1], "lineWidth": 4})
        lineMesh = Mesh(geometry, lineMaterial)

        self.scene.add(pointMesh)
        self.scene.add(lineMesh)

    def paintGL(self):
        super().paintGL()
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)


def main():
    app = baseApp(sys.argv)
    window = Test([800, 600], "Test-4-3")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
