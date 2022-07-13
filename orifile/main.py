import PyQt5
import sys

from PyQt5.QtWidgets import QApplication, QWidget

app=QApplication(sys.argv)
w=QWidget()
w.setWindowTitle("the first")
w.show()
app.exec_()
