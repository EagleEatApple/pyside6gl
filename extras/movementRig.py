# import standard library

# import third party library
from PySide6.QtCore import Qt
# import local library
from core.object3D import Object3D


class MovementRig(Object3D):
    def __init__(self, unitsPerSecond=1, degreesPerSecond=60):

        # initilize base Object3d; controls movement
        # and turn left/right
        super().__init__()

        # initialize attached Object3d; controls look up/down
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self

        # control rate of movement
        self.unitsPerSecond = unitsPerSecond
        self.degreesPerSecond = degreesPerSecond

        #customizable key mappings
        # defaults: WASDRF (move), QE (turn), TG (look)
        self.KEY_MOVE_FORWARDS = Qt.Key_W
        self.KEY_MOVE_BACKWARDS = Qt.Key_S
        self.KEY_MOVE_LEFT = Qt.Key_A
        self.KEY_MOVE_RIGHT = Qt.Key_D
        self.KEY_MOVE_UP = Qt.Key_R
        self.KEY_MOVE_DOWN = Qt.Key_F
        self.KEY_TURN_LEFT = Qt.Key_Q
        self.KEY_TURN_RIGHT = Qt.Key_E
        self.KEY_LOOK_UP = Qt.Key_T
        self.KEY_LOOK_DOWN = Qt.Key_G

    # adding and removing objects applies to look attachment;
    # override funtions from Object3d class
    def add(self, child):
        self.lookAttachment.add(child)

    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObejct, deltaTime):
        moveAmount = self.unitsPerSecond * deltaTime
        rotateAmount = self.degreesPerSecond * 3.1415926 / 180.0 * deltaTime

        if inputObejct.isKeyPressed(self.KEY_MOVE_FORWARDS):
            self.translate(0, 0, -moveAmount)
        if inputObejct.isKeyPressed(self.KEY_MOVE_BACKWARDS):
            self.translate(0, 0, moveAmount)
        if inputObejct.isKeyPressed(self.KEY_MOVE_LEFT):
            self.translate(-moveAmount, 0, 0)
        if inputObejct.isKeyPressed(self.KEY_MOVE_RIGHT):
            self.translate(moveAmount, 0, 0)
        if inputObejct.isKeyPressed(self.KEY_MOVE_UP):
            self.translate(0, moveAmount, 0)
        if inputObejct.isKeyPressed(self.KEY_MOVE_DOWN):
            self.translate(0, -moveAmount, 0)

        if inputObejct.isKeyPressed(self.KEY_TURN_RIGHT):
            self.rotateY(-rotateAmount)
        if inputObejct.isKeyPressed(self.KEY_TURN_LEFT):
            self.rotateY(rotateAmount)

        if inputObejct.isKeyPressed(self.KEY_LOOK_UP):
            self.lookAttachment.rotateX(rotateAmount)
        if inputObejct.isKeyPressed(self.KEY_LOOK_DOWN):
            self.lookAttachment.rotateX(-rotateAmount)