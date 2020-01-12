import sqlite3

con = sqlite3.connect("chemi.db")
con.row_factory = sqlite3.Row
cur = con.cursor()


def find_atom(simbol):
    cur.execute('SELECT * FROM chemical')
    # simbol = str(input('Введите первый атом: '))
    simbol = (simbol,)
    sql_find = 'SELECT Weight FROM Chemical WHERE simbol=?'
    cur.execute(sql_find, simbol)
    simbol_notes = cur.fetchone()
    atom = simbol_notes['Weight']
    float(atom)
    # print(atom)
    return atom


def molecular_mass(first_atom, quantilite1, second_atom, quantilite2):
    # first_atom = str(input('Введите второй атом: '))
    # quantilite1 = int(input('Введите число атомов: '))
    # second_atom = str(input('Введите второй атом: '))
    # quantilite2 = int(input('Введите число атомов: '))

    x = find_atom(first_atom)
    y = find_atom(second_atom)

    c = x * float(quantilite1) + y * float(quantilite2)
    print('Молекулярная Маса: ' + str(first_atom) + str(quantilite1) + str(second_atom) + str(quantilite2) + ' = ' + str(c))
    return c


a = map(str, input('Введите формулу: ').split())
q, w, e, r = a

molecular_mass(q, w, e, r)

con.close()
input('Press Enter')
