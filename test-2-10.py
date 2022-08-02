# import standard library
import sys

# import third party library
from PySide6.QtCore import Qt

# import local library
from core.base import Base, baseApp


# check input


class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)
        self.timer.stop()


    def initializeGL(self):
        super().initializeGL()

    def paintGL(self):
        super().paintGL()



        # debug printing
        # if len(self.input.keyDownList) > 0:
        #     print( "Keys down:", self.input.keyDownList)
        # if len(self.input.keyPressedList) > 0:
        #     print( "Keys pressed:", self.input.keyPressedList)
        # if len(self.input.keyUpList) > 0:
        #     print( "Keys up:", self.input.keyUpList)
        # typical usage
        if self.input.isKeyDown(Qt.Key_Space):
            print("The 'space' key was just pressed down.")

        if self.input.isKeyPressed(Qt.Key_Right):
            print("The 'right' key is currently being pressed.")




def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-10")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
