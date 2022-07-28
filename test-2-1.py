# import standard library
import sys

# import third party library

# import local library
from core.base import Base, baseApp


class Test(Base):
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__(screenSize, title)

    def initializeGL(self):
        super().initializeGL()

    def paintGL(self):
        super().paintGL()


def main():
    app = baseApp(sys.argv)
    window = Test(title="Test-2-1")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
