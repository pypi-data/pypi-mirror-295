import time

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QFont, QColor


class PQImageButton(QAbstractButton):
    def __init__(self, parent, btnRect=None, pixmap=None, pixmap_hover=None, pixmap_pressed=None,
                 text=None, textRect=None, fontSize=20, fontBold=True, fontAlign=Qt.AlignCenter,
                 defaultColor=QColor(0, 0, 0), downColor=QColor(0, 0, 0)):
        super(PQImageButton, self).__init__(parent)

        self.btnRect = btnRect
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
        self.setFixedSize(btnRect.width(), btnRect.height())

        self.text = text
        if textRect is None:
            self.textRect = QRect(0, 0, btnRect.width(), btnRect.height()-5)
        else:
            self.textRect = textRect
        self.fontSize = fontSize
        self.fontBold = fontBold
        self.defaultFont = QFont("Malgun Gothic", self.fontSize)
        self.defaultFont.setBold(self.fontBold)
        self.fontAlign = fontAlign
        self.defaultColor = defaultColor
        self.downTextColor = downColor

        self.mouseFocus = False
        self.mousePressTime = 0

    def setImgMap(self, pixmap, pixmap_hover, pixmap_pressed):
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed
        self.update()

    def paintEvent(self, event):
        curPixmap = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            curPixmap = self.pixmap_pressed

        btnRectX = self.btnRect.x()
        btnRectY = self.btnRect.y()
        btnRectW = self.btnRect.width()
        btnRectH = self.btnRect.height()

        painter = QPainter(self)
        painter.drawPixmap(0, 0, btnRectW, btnRectH, curPixmap)
        self.move(btnRectX, btnRectY)

        if self.text is not None:
            painter.setFont(self.defaultFont)
            if self.isDown():
                painter.setPen(self.downTextColor)
            else:
                painter.setPen(self.defaultColor)
            painter.drawText(self.textRect, self.fontAlign, self.text)

    def setText(self, text):
        self.text = text
        self.update()

    def setTextColor(self, defaultColor, downColor):
        self.defaultColor = defaultColor
        self.downTextColor = downColor
        self.update()

    def text(self):
        return self.textMsg

    def mousePressEvent(self, event):
        self.setDown(True)
        self.mouseFocus = True
        self.mousePressTime = time.time()
        self.parent().mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDown(False)
        if self.mouseFocus:
            self.mousePressTime = round(time.time() - self.mousePressTime, 1)
            self.clicked.emit()
            self.mouseFocus = False
        else:
            self.parent().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if 0 < event.x() < self.width() and \
                0 < event.y() < self.height():
            if not self.mouseFocus:
                self.mouseFocus = True
        else:
            if self.mouseFocus:
                self.mouseFocus = False
        self.parent().mouseReleaseEvent(event)
