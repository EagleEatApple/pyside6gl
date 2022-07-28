# import standard library

# import third party library

# import local library
from geometry.geometry import Geometry
from core.attribute import Attribute


class RectangleGeometry(Geometry):

    def __init__(self, width=1, height=1):

        super().__init__()

        P0 = [-width/2, -height/2, 0]
        P1 = [width/2, -height/2, 0]
        P2 = [-width/2,  height/2, 0]
        P3 = [width/2,  height/2, 0]
        C0, C1, C2, C3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        positionData = [P0, P1, P3, P0, P3, P2]
        colorData = [C0, C1, C3, C0, C3, C2]

        self.addAttribute("vec3", "vertexPositon", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.countVertices()
