import sys
import math

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QApplication, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sqlite3
import re


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


def moll_mass(k):
    formula = k

    sFormula = formula

   # print("Original Formula: ", sFormula)

    # Search data inside()

    myRegEx = re.compile(r"(\()(\w*)(\))(\d*)", re.I)

    myMatches = myRegEx.findall(sFormula)

    while myMatches:
        myMatches = myRegEx.findall(sFormula)
        for match in myMatches:
           # print(match[1], match[3])
            count = match[3]
            text = ""
            if count == "":
                count = 1
            else:
                count = int(match[3])
            while count >= 1:
                text = text + match[1]
                count -= 1
               # print(text)
            sFormula = sFormula.replace('(' + match[1] + ')' + match[3], text)
           # print("Replaced formula: ", sFormula)

    myRegEx = re.compile("(C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?"
                         "|P[drmtboau]?|H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G"
                         "[""aed]|I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|U|V|W|Xe|Yb?|Z[nr])(\d*)")

    myMatches = myRegEx.findall(sFormula)

    molecularFormula = ""
    MW = 0
    text = ""

    for match in myMatches:
        # Search symbol
        symbol = match[0]
        atom_mass = find_atom(symbol)
        # Search numbers
        number = match[1]
       # print(atom_mass, number)
        if number == "":
            number = 1
        else:
            number = int(match[1])
        MW = MW + float(atom_mass) * number
        while number >= 1:
            molecularFormula = molecularFormula + symbol
            number -= 1
    #  print(molecularFormula)
    #  print("formula: " + formula + " MW = " + str(MW))
    s = round(MW, 2)
    return s


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

    def clickMethod(self,):
        # переменная с значением введеных атомов
        text1 = self.line.text()
        q = str(text1)
        b = moll_mass(q)
        self.nameLabel_4.setText('Result: ' + 'Formula: ' + str(q) + '\n' +
                                 'Molecular Mass: ' + str(q) + ' = ' + str(b) + ' g/mol')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
