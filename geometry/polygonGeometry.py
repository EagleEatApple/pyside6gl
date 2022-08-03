# import standard library
from math import sin, cos, pi

# import third party library

# import local library
from geometry.geometry import Geometry


class PolygonGeometry(Geometry):

    def __init__(self, sides=3, radius=1):
        super().__init__()

        A = 2*pi/sides
        positionData = []
        colorData = []

        uvData = []
        uvCenter = [0.5, 0.5]

        normalData = []
        normalVector = [0, 0, 1]

        for n in range(sides):
            positionData.append([0, 0, 0])
            positionData.append([radius*cos(n*A), radius*sin(n*A), 0])
            positionData.append([radius*cos((n+1)*A), radius*sin((n+1)*A), 0])
            colorData.append([1, 1, 1])
            colorData.append([1, 0, 0])
            colorData.append([0, 0, 1])

            # textures coordinates
            uvData.append(uvCenter)
            uvData.append([cos(n*A)*0.5 + 0.5, sin(n*A)*0.5 + 0.5])
            uvData.append([cos((n+1)*A)*0.5 + 0.5, sin((n+1)*A)*0.5 + 0.5])

            normalData.append(normalVector)
            normalData.append(normalVector)
            normalData.append(normalVector)

        self.addAttribute("vec2", "vertexUV", uvData)

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec3", "vertexNormal", normalVector)
        self.addAttribute("vec3", "faceNormal", normalVector)

        self.countVertices()
