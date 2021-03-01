from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from release.main_ui import Ui_MainWindow
from release.addEditCoffeeForm import Ui_EditWindow
import sqlite3
import sys


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Coffee, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Латте макиато')
        self.refresh()
        self.pushButton.clicked.connect(self.new)

    def refresh(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        result = cur.execute('''SELECT * FROM "coffee"''').fetchall()
        con.close()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i, elem in enumerate(result):
            for j in range(len(elem)):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem[j])))
                self.tableWidget.item(i, j).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.itemClicked.connect(self.change)

    def new(self):
        self.editor = Editor()
        self.editor.show()

    def change(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        self.editor = Editor(id=int(ids[0]))
        self.editor.show()


class Editor(QMainWindow, Ui_EditWindow):
    def __init__(self, id=None):
        super(Editor, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Измение значений')
        self.id = id
        if id:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            result = cur.execute(f'''SELECT * FROM "coffee" WHERE id = {id}''').fetchall()
            self.result = result
            con.close()
            self.lineEdit.setText(result[0][1])
            self.lineEdit_2.setText(result[0][2])
            self.lineEdit_3.setText(result[0][3])
            self.lineEdit_4.setText(result[0][4])
            self.lineEdit_5.setText(result[0][5])
            self.lineEdit_6.setText(result[0][6])
        self.pushButton.clicked.connect(self.push)
        self.pushButton_2.clicked.connect(self.remove)

    def push(self):
        if self.id:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f'''UPDATE "coffee" SET name="{self.lineEdit.text()}", 
                            degree="{self.lineEdit_2.text()}", type="{self.lineEdit_3.text()}", 
                            description="{self.lineEdit_4.text()}", price="{self.lineEdit_5.text()}", 
                            vol="{self.lineEdit_6.text()}" WHERE id={self.result[0][0]}''')
            con.commit()
            con.close()
        else:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f'''INSERT INTO "coffee" VALUES (NULL, "{self.lineEdit.text()}", 
                            "{self.lineEdit_2.text()}", "{self.lineEdit_3.text()}",
                            "{self.lineEdit_4.text()}", "{self.lineEdit_5.text()}", 
                            "{self.lineEdit_6.text()}")''')
            con.commit()
            con.close()
        ex.refresh()

    def remove(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        cur.execute(f'''DELETE FROM "coffee" WHERE id={self.result[0][0]}''')
        con.commit()
        con.close()
        ex.refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
