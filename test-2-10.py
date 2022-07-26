import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt

# check input
class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphics Window")
        self.setFixedSize(512, 512)
        self.KeyDownList = []
        self.keyPressedList = []
        self.keyUpList = []

    def initializeGL(self):
        print ("Initializing program...")

    def paintGL(self):
        # debug printing
        # if len(self.KeyDownList) > 0:
        #     print( "Keys down:", self.KeyDownList)
        # if len(self.keyPressedList) > 0:
        #     print( "Keys pressed:", self.keyPressedList)
        # if len(self.keyUpList) > 0:
        #     print( "Keys up:", self.keyUpList)
        # typical usage
        if self.isKeyDown(Qt.Key_Space):
            print("The 'space' key was just pressed down.")

        if self.isKeyPressed(Qt.Key_Right):
            print("The 'right' key is currently being pressed.")
        self.KeyDownList = []
        self.keyUpList = []

    def keyPressEvent(self, event):
        keyName = event.key()
        self.KeyDownList.append(keyName)
        self.keyPressedList.append(keyName)
        self.update()

    def keyReleaseEvent(self, event):
        keyName = event.key()
        self.keyPressedList.remove(keyName)
        self.keyUpList.append(keyName)
        self.update()
    
    # functions to check key states
    def isKeyDown(self, keyCode):
        return keyCode in self.KeyDownList
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList


def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

