import sys
import math

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QApplication, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sqlite3


con = sqlite3.connect("chemi.db")
con.row_factory = sqlite3.Row
cur = con.cursor()


def find_atom(simbol):
    # функция которая с помощью магии ищет масу атома в БД и возвращает её
    cur.execute('SELECT * FROM chemical')
    simbol = (simbol,)
    sql_find = 'SELECT Weight FROM Chemical WHERE simbol=?'
    cur.execute(sql_find, simbol)
    simbol_notes = cur.fetchone()
    atom = simbol_notes['Weight']
    float(atom)
    return atom


def mol_mas(s1, n1, s2, n2):
    # принемает значение первого атома
    x = find_atom(s1)
    # принемает значение второго атома
    y = find_atom(s2)
    # формула вычисления молекулярной масы
    # n1 and n2 принемают значения количества атомов
    # функция возвращает результат вычисления формулы(молекулярную масу)
    c = x * float(n1) + y * float(n2)
    return c


def mass_fraction_one(s1, n1, s2, n2):
    # функция которая возвращает масовую долю первого элемента
    one = find_atom(s1)

    two = find_atom(s2)

    atom_mass = one * float(n1) + two * float(n2)

    elone = one * float(n1) / atom_mass * 100
    w = round(elone, 2)
    return w


def mass_fraction_two(s1, n1, s2, n2):
    # функция которая возвращает мосовую долю второго элемента
    one = find_atom(s1)

    two = find_atom(s2)

    atom_mass = one * float(n1) + two * float(n2)

    eltwo = two * float(n2) / atom_mass * 100
    q = round(eltwo, 2)
    return q


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # icon in window
        self.setWindowIcon(QIcon('atom.png'))
        # параметры робочого окна
        self.setMinimumSize(QSize(340, 300))
        self.setWindowTitle("Chemical Calculator")
        # отображение полей ввода
        # enter formula line
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter formula')
        self.line = QLineEdit(self)

        # print label
        self.nameLabel_4 = QLabel(self)
        self.nameLabel_4.setText('Result')

        # параметры полей ввода
        # first atom line
        self.line.move(100, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        # print label

        self.nameLabel_4.move(20, 60)
        self.nameLabel_4.resize(200, 62)
        # метод нажатия на кнопку
        pushbutton = QPushButton('to count', self)
        pushbutton.clicked.connect(self.clickMethod)
        pushbutton.resize(200, 32)
        pushbutton.move(80, 250)

    def clickMethod(self):
        # переменная с значением введеных атомов
        text1 = self.line.text()
        q = str(text1)
        w = q.rsplit(sep=None, maxsplit=-1)
        p, o, i, u = w

        self.nameLabel_4.setText('Result: ' + 'Formula: ' + str(p) + str(o) + str(i) + str(u) + '\n' +
                                 'Mass = ' + str(mol_mas(p, o, i, u)) + '\n' +
                                 'W1:' + str(p) + str(o) + ' = ' + str(mass_fraction_one(p, o, i, u)) + '%' + '\n' +
                                 'W2:' + str(i) + str(u) + ' = ' + str(mass_fraction_two(p, o, i, u)) + '%')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
