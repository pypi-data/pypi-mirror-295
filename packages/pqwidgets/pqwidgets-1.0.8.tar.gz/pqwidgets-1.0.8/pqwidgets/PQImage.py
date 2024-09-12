import time

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt, pyqtSignal


class PQImage(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, area=(0, 0, 0, 0), pixmap=""):
        super(PQImage, self).__init__(parent)
        self.parent = parent
        self.rectImg = area
        self.mouseFocus = False
        self.mousePressTime = 0
        self.pixmap = pixmap
        self.setStyleSheet("background-color:transparent; color:transparent;")
        self.Update()

    def Update(self):
        img = QPixmap(self.pixmap)
        self.setGeometry(self.rectImg)

        if img.size().isNull():
            self.setPixmap(img)
        else:
            self.scaledImg = img.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(self.scaledImg)

    def setImage(self, pixmap):
        self.pixmap = pixmap
        self.Update()

    def setImgRotate(self, degree):
        img = QPixmap(self.pixmap)
        self.scaledImg = img.transformed(QTransform().rotate(degree))
        self.setPixmap(self.scaledImg)

    def mousePressEvent(self, event):
        self.mouseFocus = True
        self.mousePressTime = time.time()

        self.parent.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mouseFocus:
            self.mousePressTime = round(time.time() - self.mousePressTime, 1)
            self.clicked.emit()
            self.mouseFocus = False
        else:
            self.parent.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if 0 < event.x() < self.width() and \
                0 < event.y() < self.height():
            if not self.mouseFocus:
                self.mouseFocus = True
        else:
            if self.mouseFocus:
                self.mouseFocus = False

        self.parent.mouseMoveEvent(event)
