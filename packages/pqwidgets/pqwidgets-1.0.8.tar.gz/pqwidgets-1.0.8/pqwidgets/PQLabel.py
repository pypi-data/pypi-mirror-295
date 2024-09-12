import time

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QLabel


class PQLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, size=(0, 0, 0, 0), text="", fontSize=18, fontBold=True, fontAlign=Qt.AlignCenter,
                 styleSheet="background-color:transparent; color:rgb(0,0,0)", radius=0):
        super(PQLabel, self).__init__(parent)
        self.parent = parent
        self.size = size
        self.mouseFocus = False
        self.mousePressTime = 0
        self.radius = radius
        self.fontBold = fontBold
        self.defaultFont = QFont("Malgun Gothic", fontSize)
        self.defaultFont.setBold(fontBold)

        self.setText(text)
        self.setFont(self.defaultFont)
        self.setAlignment(fontAlign)
        self.setStyleSheet(styleSheet)
        self.setGeometry(self.size)

        # 초기 배경색 설정
        self.color = QColor(Qt.transparent)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        painter.setRenderHint(QPainter.Antialiasing)  # 모서리를 부드럽게 렌더링

        # 둥근 배경 그리기
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)  # 테두리 없음
        painter.drawRoundedRect(rect, self.radius, self.radius)  # 둥근 사각형 그리기

        # 텍스트 그리기
        painter.setPen(self.palette().color(self.foregroundRole()))  # 텍스트 색상
        painter.setFont(self.font())
        painter.drawText(rect, self.alignment(), self.text())

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
        if 0 < event.x() < self.width() and 0 < event.y() < self.height():
            if not self.mouseFocus:
                self.mouseFocus = True
        else:
            if self.mouseFocus:
                self.mouseFocus = False

        self.parent.mouseMoveEvent(event)
