import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        self.spn = 0.002
        self.ll1 = 37.587945442466825
        self.ll2 = 55.73402552478429

        self.form = 'map'
        self.counterform = 0
        super().__init__()
        self.image = QLabel(self)
        self.getImage()

    def keyPressEvent(self, event):
        if str(event.key()) == '16777235':
            if self.spn < 0.008:
                self.spn += 0.002
            elif self.spn >= 90:
                self.spn = 0.002
            else:
                self.spn += 0.003
        elif str(event.key()) == '16777237':
            self.spn -= 0.001
            if self.spn <= 0:
                self.spn = 0.002
            elif self.spn < 0.08 and self.spn > 0:
                self.spn -= 0.002
            else:
                self.spn -= 0.03
        elif str(event.key()) == '16777220':
            if self.counterform == 3:
                self.counterform = 0
            if self.counterform == 0:
                self.form = 'map'
            elif self.counterform == 1:
                self.form = 'sat'
            elif self.counterform == 2:
                self.form = 'sat,skl'
            self.counterform += 1
        elif event.key() == 1042:
            if self.ll1 < 180:
                self.ll1 += 1
            if self.ll1 >= 180:
                self.ll1 = 37.587945442466825
        elif event.key() == 1060:
            if self.ll1 > -180:
                self.ll1 -= 1
            if self.ll1 <= -180:
                self.ll1 = 37.587945442466825
        elif event.key() == 1062:
            if self.ll2 < 85:
                self.ll2 += 1
            if self.ll2 >= 85:
                self.ll2 = 55.73402552478429
        elif event.key() == 1067:
            if self.ll2 > -85:
                self.ll2 -= 1
            if self.ll2 <= -85:
                self.ll2 = 55.73402552478429

        self.image.clear()
        self.getImage()


    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.ll1},{self.ll2}&spn={self.spn},{self.spn}&l=map"
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.ll1},{self.ll2}&spn={self.spn},{self.spn}&l={self.form}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
