import widget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
import dialog
import sys
import sqlite3


class App(QtWidgets.QMainWindow, widget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.modified = {}
        self.titles = None
        self.update_result()
        self.pushButton.clicked.connect(self.add_film)
        self.pushButton_2.clicked.connect(self.change_film)
        self.pushButton_3.clicked.connect(self.delete_film)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        self.result = cur.execute(f"SELECT * FROM main").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_film(self):
        self.dlg = Dialog()
        self.dlg.show()

    def change_film(self):
        current = self.tableWidget.selectedItems()
        if len(current) == 1:
            self.dlg = Dialog(list(map(str, self.result[current[0].row()])))
            self.dlg.show()

    def delete_film(self):
        current = self.tableWidget.selectedItems()
        if len(current) > 0:
            ids = [f'id = {self.result[i.row()][0]}' for i in current]
            cur = self.con
            sql = f"DELETE FROM main WHERE {' OR '.join(ids)}"
            cur.execute(sql)
            self.con.commit()
            self.update_result()


class Dialog(QtWidgets.QDialog, dialog.Ui_Dialog):
    def __init__(self, data=None):
        super().__init__()
        self.setupUi(self)
        self.data = data
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        if data is None:
            self.accepted.connect(self.ok)
        else:
            self.lineEdit.setText(data[1])
            self.lineEdit_2.setText(data[2])
            self.lineEdit_3.setText(data[3])
            self.lineEdit_4.setText(data[4])
            self.lineEdit_5.setText(data[5])
            self.lineEdit_6.setText(data[6])
            self.accepted.connect(self.change)

    def change(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        sql = f'UPDATE main SET gradeName = "{self.lineEdit.text()}", ' \
              f'roast = "{self.lineEdit_2.text()}", type = "{self.lineEdit_3.text()}"' \
              f', taste = "{self.lineEdit_4.text()}", price = "{self.lineEdit_5.text()}" ' \
              f', volume = "{self.lineEdit_6.text()}"WHERE id = {self.data[0]}'
        cur.execute(sql)
        con.commit()
        start_window.tableWidget.clear()
        start_window.update_result()
        self.close()

    def ok(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        sql = 'SELECT MAX(id) from main'
        cur.execute(sql)
        print(2)
        next_id = cur.fetchall()[0][0] + 1
        sql = f'INSERT INTO main(id, gradeName, roast, type, taste, price, volume) ' \
              f'VALUES({next_id}, "{self.lineEdit.text()}", "{self.lineEdit_2.text()}", ' \
              f'"{self.lineEdit_3.text()}", "{self.lineEdit_4.text()}", ' \
              f'"{self.lineEdit_5.text()}", "{self.lineEdit_6.text()}");'
        cur.execute(sql)
        con.commit()
        print(3)
        start_window.tableWidget.clear()
        start_window.update_result()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QtWidgets.QApplication(sys.argv)
    global start_window
    start_window = App()
    start_window.show()
    sys.excepthook = except_hook
    app.exec_()


if __name__ == "__main__":
    main()
