# import standard library

# import third party library
from OpenGL.GL import *

# import local library
from core.mesh import Mesh


class Renderer(object):
    def __init__(self, clearColor=[0, 0, 0]):
        glEnable(GL_DEPTH_TEST)
        # required for antialiasing
        glEnable(GL_MULTISAMPLE)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)

    def render(self, scene, camera):

        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Update camera view (calculate inverse)
        camera.updateViewMatrix()

        # extract list of all Mesh objects in scene
        descendantList = scene.getDescendantList()
        def meshFilter(x): return isinstance(x, Mesh)
        meshList = list(filter(meshFilter, descendantList))

        for mesh in meshList:
            # if this object is not visible,
            #  continue to next object in list
            if not mesh.visible:
                continue

            glUseProgram(mesh.material.programRef)

            # bind VAO
            glBindVertexArray(mesh.vaoRef)

            # update uniform values stored outside of material
            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            # update uniforms stored in material
            for variableName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
            # update render settings
            mesh.material.updateRenderSettings()
            glDrawArrays(
                mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount)
