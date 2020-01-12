import sys
import math

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
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
        # параметры робочого окна
        self.setMinimumSize(QSize(640, 600))
        self.setWindowTitle("Chemi Calculator")
        # отображение полей ввода
        # first atom line
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('First Atom')
        self.line = QLineEdit(self)
        # quantity first atom line
        self.nameLabel_1 = QLabel(self)
        self.nameLabel_1.setText('Quantity')
        self.line_1 = QLineEdit(self)
        # second atom line
        self.nameLabel_2 = QLabel(self)
        self.nameLabel_2.setText('Second Atom')
        self.line_2 = QLineEdit(self)
        # quantity second atom line
        self.nameLabel_3 = QLabel(self)
        self.nameLabel_3.setText('Quantity')
        self.line_3 = QLineEdit(self)
        # print label
        self.nameLabel_4 = QLabel(self)
        self.nameLabel_4.setText('Result')

        # параметры полей ввода
        # first atom line
        self.line.move(85, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)
        # quantity first atom
        self.line_1.move(85, 60)
        self.line_1.resize(200, 32)
        self.nameLabel_1.move(20, 60)
        # second atom line
        self.line_2.move(85, 100)
        self.line_2.resize(200, 32)
        self.nameLabel_2.move(20, 100)
        # quantity second atom
        self.line_3.move(85, 140)
        self.line_3.resize(200, 32)
        self.nameLabel_3.move(20, 140)
        # print label

        self.nameLabel_4.move(20, 180)
        self.nameLabel_4.resize(200, 62)
        # метод нажатия на кнопку
        pushbutton = QPushButton('to count', self)
        pushbutton.clicked.connect(self.clickMethod)
        pushbutton.resize(200, 32)
        pushbutton.move(80, 250)

    def clickMethod(self):
        # переменная с значением введеных атомов
        text1 = self.line.text()
        text2 = self.line_1.text()
        text3 = self.line_2.text()
        text4 = self.line_3.text()
        mass = mol_mas(text1, text2, text3, text4)
        mass_two = mass_fraction_two(text1, text2, text3, text4)
        mass_one = mass_fraction_one(text1, text2, text3, text4)

        # print('Formula: ' + text1.title() + text2.title() + text3.title() + text4.title())
        # print('Mass = ' + str(mol_mas(text1.title(), text2.title(), text3.title(), text4.title())))
        self.nameLabel_4.setText('Result: ' + '\n' +
                                 'Formula: ' + text1 + text2 + text3 + text4 + '\n' +
                                 'Mass = ' + str(mass) + ' g/mol' + '\n' +
                                 'W1 :' + text1 + text2 + ' = ' + str(mass_one) + '%' + '\n' +
                                 'W2 :' + text3 + text4 + ' = ' + str(mass_two) + '%')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
