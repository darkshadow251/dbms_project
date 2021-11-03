import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sqlite3



class MainWindow(QMainWindow):
    def __init__(self,widget):
        super(MainWindow,self).__init__()
        loadUi("Admin Login.ui",self)
        self.widget=widget
        self.loginButton.clicked.connect(self.nextscreen)

    def nextscreen(self,widget):
        if self.usernamelineEdit.text()=="" or self.passwordlineEdit.text()=="":
            self.error.setText("Enter all inputs")
        
        else:
            user=self.usernamelineEdit.text()
            
            passw=self.passwordlineEdit.text()
            conn=sqlite3.connect('Driving_School.db')
            c=conn.cursor()
            query="""SELECT * FROM admin WHERE Username=?"""
            try:
                c.execute(query,(user,))
                password=c.fetchone()
                       
                if passw==str(password[2]):
                    self.widget.setCurrentIndex(1)
                else:
                    self.error.setText("Invalisernd Uame or Password")
            except:
                self.error.setText("Error Ocurred")
            conn.commit()
            conn.close()

class Dashboard(QMainWindow):
    def __init__(self,widget):
        super(Dashboard,self).__init__()
        loadUi("Dashboard.ui",self)
        self.widget=widget
        self.AddStudentButton.clicked.connect(self.addstudent)
        self.AddTrainerButton.clicked.connect(self.addtrainer)
        self.SearchStudentButton.clicked.connect(self.searchstudent)
        self.SearchTrainerButton.clicked.connect(self.searchtrainer)
        self.FeesButton.clicked.connect(self.feesdetails)
        self.ExitButton.clicked.connect(self.exit)
        self.SessionButton.clicked.connect(self.session)
        self.ExamButton.clicked.connect(self.exam)
        conn=sqlite3.connect('Driving_School.db')
        c=conn.cursor()
        query="""SELECT * FROM student"""
        query2="""SELECT * FROM trainer"""
       
        c.execute(query)
        students=c.fetchall()
        self.StudentNumber.setText(str(len(students)))
        
        c.execute(query2)
        trainer=c.fetchall()
        self.TrainerNumber.setText(str(len(trainer)))
                       
            
        conn.commit()
        conn.close()


    def addstudent(self):
        self.widget.setCurrentIndex(2)

    def addtrainer(self):
        self.widget.setCurrentIndex(3)

    def searchstudent(self):
        self.widget.setCurrentIndex(4)

    def searchtrainer(self):
        self.widget.setCurrentIndex(5)

    def feesdetails(self):
        self.widget.setCurrentIndex(6)

    def session(self):
        self.widget.setCurrentIndex(7)

    def exam(self):
        self.widget.setCurrentIndex(8)

    def exit(self):
        self.widget.setCurrentIndex(0)

