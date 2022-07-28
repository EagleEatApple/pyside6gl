# import standard library
from math import sin, cos, pi

# import third party library

# import local library

from geometry.parametricGeometry import ParametricGeometry


class EllipsoidGeometry(ParametricGeometry):

    def __init__(self, width=1, height=1, depth=1,
                 radiusSegments=32, heightSegments=16):
        def S(u, v):
            return [width*0.5 * sin(u) * cos(v),
                    height*0.5 * sin(v),
                    depth*0.5 * cos(u) * cos(v)]
        super().__init__(0, 2 * pi, radiusSegments, -pi*0.5, pi*0.5, heightSegments, S)
