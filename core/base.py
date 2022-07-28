# import standard library
import sys
import time

# import third party library
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtCore import QTimer
from OpenGL.GL import *

# import local library


class Base(QOpenGLWidget):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__()
        # set the title and size of window
        self.setWindowTitle("Graphics Window - " + title)
        self.setFixedSize(screenSize[0], screenSize[1])
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
        self.time = 0

    def initializeGL(self):
        self.last_time = time.time()
        print("Initializing program...")

    def paintGL(self):
        self.deltaTime = time.time() - self.last_time
        self.time += self.deltaTime
        self.last_time = time.time()


class baseApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        # initialize OpenGL features
        """ Original Pygame code in base.py, the OpenGL version is 2.1
        #use a core opengl profile for cross-plataform compatibility
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE)
        """
        self.format = QSurfaceFormat()
        self.format.setDepthBufferSize(24)
        self.format.setVersion(2, 1)
        self.format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(self.format)


def main():
    app = baseApp(sys.argv)
    window = Base([800, 600], "Base")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
