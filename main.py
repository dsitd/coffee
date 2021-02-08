import widget
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem
import sys
import sqlite3


class App(PyQt5.QtWidgets.QWidget, widget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        self.result = cur.execute(f"SELECT * FROM main").fetchall()
        print(self.result)
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        # Заполнили таблицу полученными элементами
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', ' степень обжарки', 'молотый/в зернах', 'описание вкуса',
             'цена', ' объем упаковки'])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    start_window = App()
    start_window.show()
    sys.excepthook = except_hook
    app.exec_()
