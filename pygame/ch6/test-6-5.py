from core.base import Base 
from core.renderer import Renderer 
from core.scene  import Scene 
from core.camera import Camera 
from core.mesh import Mesh 
from core.texture  import Texture 
from light.ambientLight import AmbientLight 
from light.directionalLight import DirectionalLight 
from material.phongMaterial import PhongMaterial 
from geometry.rectangleGeometry import RectangleGeometry 
from geometry.sphereGeometry import SphereGeometry 
from extras.movementRig import MovementRig 
from extras.directionalLightHelper import DirectionalLightHelper 
from material.textureMaterial import TextureMaterial

# testing shadows
class Test(Base):

    def initialize(self):
        print("Initializing program...")

        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        # self.camera.setPosition([0, 0, 6])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0, 2, 5])

        ambLight = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(ambLight)

        self.dirLight = DirectionalLight(direction=[-1, -1, 0])
        self.dirLight.setPosition([2, 4, 0])
        self.scene.add(self.dirLight)
        directHelper = DirectionalLightHelper(self.dirLight)
        self.dirLight.add(directHelper)

        sphereGeometry = SphereGeometry()
        phongMaterial = PhongMaterial(
            texture=Texture("images/grid.png"),
            useShadow=True)

        sphere1 = Mesh(sphereGeometry, phongMaterial)
        sphere1.setPosition([-2, 1, 0])
        self.scene.add(sphere1)

        sphere2 = Mesh(sphereGeometry, phongMaterial)
        sphere2.setPosition([1, 2.2, -0.5])
        self.scene.add(sphere2)

        self.renderer.enableShadows(self.dirLight)

        # optional: render depth texture to mesh in scene
        depthTexture = self.renderer.shadowObject.renderTarget.texture
        shadowDisplay = Mesh( RectangleGeometry(),TextureMaterial(depthTexture) )
        shadowDisplay.setPosition([-1,3,0])
        self.scene.add( shadowDisplay )

        floor = Mesh(RectangleGeometry(width=20, height=20), phongMaterial)
        floor.rotateX(-3.14/2)
        self.scene.add(floor)

    def update(self):
        # view dynamic shadows -- need to increase shadow camera range
        self.dirLight.rotateY(0.01337, False)
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)
        # render scene from shadow camera
        # shadowCam = self.renderer.shadowObject.camera
        # self.renderer.render( self.scene, shadowCam )

# inistantiate this class and run the program
Test(screenSize=[800, 600]).run()