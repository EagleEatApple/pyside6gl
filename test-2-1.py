import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget

class Test(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        print ("Initializing program...")

    def paintGL(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

