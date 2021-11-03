import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from Login_Dashboard import MainWindow, Dashboard
from Student import Student_Details, Student_Search,Student_View
from Trainer import Trainer_Details, Trainer_Search, Trainer_View
from Fees import Fees_Details, Session_Details, Exam_Details



app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=MainWindow(widget)
dashboard=Dashboard(widget)
student=Student_Details(widget)
trainer=Trainer_Details(widget)
student_search=Student_Search(widget)
trainer_search=Trainer_Search(widget)
session=Session_Details(widget)
exam=Exam_Details(widget)
fees=Fees_Details(widget)
widget.addWidget(mainwindow)
widget.addWidget(dashboard)
widget.addWidget(student)
widget.addWidget(trainer)
widget.addWidget(student_search)
widget.addWidget(trainer_search)
widget.addWidget(fees)
widget.addWidget(session)
widget.addWidget(exam)
widget.setFixedHeight(800)
widget.setFixedWidth(1100)

widget.show()
try:
    sys.exit(app.exec_())
except:
    print('exiting')