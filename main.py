#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication, QLabel, QLineEdit, QTextEdit, QMessageBox)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        lbl1 = QLabel('Введите скорость машины (м/с):')
        grid.addWidget(lbl1, 0, 0)
        self.v0 = QLineEdit()
        grid.addWidget(self.v0, 0, 1)
        lbl2 = QLabel('Введите расстояние до препятствия (м):')
        grid.addWidget(lbl2, 1, 0)
        self.l0 = QLineEdit()
        grid.addWidget(self.l0, 1, 1)
        lbl3 = QLabel('Масса машины (кг):')
        grid.addWidget(lbl3, 2, 0)
        self.massa = QLineEdit()
        self.massa.setText('1200')
        grid.addWidget(self.massa, 2, 1)
        lbl4 = QLabel('Предельная допустимая энергия (Дж):')
        grid.addWidget(lbl4, 3, 0)
        self.emax = QLineEdit()
        self.emax.setText('-')
        grid.addWidget(self.emax, 3, 1)

        startbutton = QPushButton('Моделировать')
        startbutton.clicked.connect(self.model)
        grid.addWidget(startbutton, 4, 0, 1, 2)
        self.output_field = QTextEdit()
        grid.addWidget(self.output_field, 5, 0, 1, 2)
        self.setGeometry(400, 300, 350, 300)
        self.setWindowTitle('Нечёткий контроллер')
        self.show()

    def model(self):
        try:
            v = int(self.v0.text())
            l = int(self.l0.text())
            m = int(self.massa.text())
        except:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Некорректные входные данные")
            button = dlg.exec()

            if button == QMessageBox.Ok:
                return
        try:
            emax = int(self.emax.text())
        except:
            emax = 2 * 10 ** 9

        time = 0
        E = m * v ** 2 / 2
        ebrake = m / 2 * (v ** 3 / l - v ** 4 / 4 / l ** 2)
        if ebrake > emax:
            ebrake = emax
        answer = f'Рассчитанная энергия: {ebrake:.3f}\n'
        answer += f'E: {E:.3f}\t t: {time}\t v: {v:.3f}\t l: {l:.3f}\n'
    
        while v > 0 and l > 0:
            time += 1

            E -= ebrake
            if E < 0:
                E = 0
            l -= v * 1
            v = (2 * E / m) ** 0.5
            answer += f'E: {E:.3f}\t t: {time}\t v: {v:.3f}\t l: {l:.3f}\n'

        if l >= 0:
            answer += 'Машина успешно остановилась'
        else:
            answer += 'К сожалению, произошло столкновение'
        self.output_field.setText(answer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

