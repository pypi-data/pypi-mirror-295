import time

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont


class PQButton(QAbstractButton):
    def __init__(self, parent=None, size=QRect(0, 0, 150, 50), text="", fontSize=18, fontBold=False,
                 ColorNormal=QColor(200, 200, 200), ColorPress=QColor(150, 150, 150), ColorText=QColor(0, 0, 0),
                 radius=0):
        super(PQButton, self).__init__(parent)

        self.defaultFont = QFont("Malgun Gothic", fontSize)
        self.defaultFont.setBold(fontBold)

        self.colorNormal = ColorNormal
        self.ColorPress = ColorPress
        self.colorText = ColorText
        self.radius = radius

        self.mouseFocus = False
        self.mousePressTime = 0

        self.setGeometry(size)
        self.setText(text)
        self.setFixedSize(size.width(), size.height())  # 버튼의 크기 설정

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # 버튼 배경 색 설정
        if self.isDown():
            painter.setBrush(self.ColorPress)
        else:
            painter.setBrush(self.colorNormal)

        painter.setRenderHint(QPainter.Antialiasing)  # 모서리를 부드럽게 렌더링
        painter.setPen(Qt.NoPen)  # 테두리 제거
        painter.drawRoundedRect(rect, self.radius, self.radius)  # 둥근 직사각형 그리기

        # 버튼 텍스트 그리기
        painter.setFont(self.defaultFont)
        painter.setPen(self.colorText)
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def mousePressEvent(self, event):
        self.setDown(True)  # paintEvent 때문에 사용 되어야 함 (self.isDown())

        self.mouseFocus = True
        self.mousePressTime = time.time()

        self.parent().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDown(False)  # paintEvent 때문에 사용 되어야 함 (self.isDown())

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
        self.parent().mouseMoveEvent(event)
