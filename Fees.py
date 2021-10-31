import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sqlite3

class General_Dialog(QDialog):
    def __init__(self):
        super(General_Dialog, self).__init__()
        loadUi("Trainer Dialog.ui", self)
        self.CancelButton.clicked.connect(self.cancel)

    def id(self,id):
        self.nameLabel.setText("Session Deatils with id "+id+" Saved Successfully")

    def cancel(self):
        self.close()

class Fees_Details(QMainWindow):
    def __init__(self,widget):
        super(Fees_Details,self).__init__()
        loadUi("Fees.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)

    def back(self):
        self.widget.setCurrentIndex(1)





class Session_Details(QMainWindow):
    def __init__(self,widget):
        super(Session_Details,self).__init__()
        loadUi("Session.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)
        self.AddSessionButton.clicked.connect(self.session)
        self.SearchButton.clicked.connect(self.search)
        self.table.setColumnWidth(4,250)
        self.table.setColumnWidth(5,250)
        print(self.frtimeEdit_2.time())
    def search(self):
        if self.idLineEdit_2.text()=="" and str(self.frtimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)":
            self.error1.setText("Enter the Trainer name")


        elif self.idLineEdit_2.text()!="" and str(self.frtimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" :
            tid=self.idLineEdit_2.text()
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM session WHERE Trainer_id=?"""
            # try:
            c.execute(query,(tid,))
            se=c.fetchall()
            row=0
            self.table.setRowCount(len(se))
            for session in se:
                print('here')
                print(str(session[4]))
                self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(session[0])))
                self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(session[1])))
                self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(session[2])))
                self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(session[3])))
                self.table.setItem(row , 4, QtWidgets.QTableWidgetItem(str(session[4])))
                self.table.setItem(row , 5, QtWidgets.QTableWidgetItem(str(session[5])))
                row+=1
            # except:
            #     self.error.setText("Invalid Trainer")

        elif self.idLineEdit_2.text()!="" and str(self.frtimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)":
            fr=str(self.frtimeEdit_2.time())
            to=str(self.totimeEdit_2.time())
            l=len(fr)
            fr=fr[19:l-1].split(',')
            
            mi=fr[1]
            timefr=fr[0]+":"+mi[1:]
            to=str(to)
            l=len(to)
            to=to[19:l-1].split(',')
            mi=to[1]
            timeto=to[0]+":"+mi[1:]
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM session WHERE Start_time=? and End_time=?"""
            try:
                c.execute(query,(timefr,timeto,))
                se=c.fetchall()
                row=0
                self.table.setRowCount(len(se))
                for session in se:
                    if session[1]==int(self.idLineEdit_2Edit.text()):
                        self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(session[0])))
                        self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(session[1])))
                        self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(session[2])))
                        self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(session[3])))
                        self.table.setItem(row , 4, QtWidgets.QTableWidgetItem(str(session[4])))
                        self.table.setItem(row , 5, QtWidgets.QTableWidgetItem(str(session[5])))
                    row+=1
            except:
                self.error.setText("Invalid Trainer")

        elif self.idLineEdit_2.text()=="" and str(self.frtimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)":
            fr=str(self.frtimeEdit_2.time())
            to=str(self.totimeEdit_2.time())
            l=len(fr)
            fr=fr[19:l-1].split(',')
            
            mi=fr[1]
            timefr=fr[0]+":"+mi[1:]
            to=str(to)
            l=len(to)
            to=to[19:l-1].split(',')
            mi=to[1]
            timeto=to[0]+":"+mi[1:]
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM session WHERE Start_time=? and End_time=?"""
            try:
                c.execute(query,(timefr,timeto,))
                se=c.fetchall()
                row=0
                self.table.setRowCount(len(se))
                for session in se:
                    
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(session[0])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(session[1])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(session[2])))
                    self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(session[3])))
                    self.table.setItem(row , 4, QtWidgets.QTableWidgetItem(str(session[4])))
                    self.table.setItem(row , 5, QtWidgets.QTableWidgetItem(str(session[5])))
                    row+=1
            except:
                self.error.setText("Invalid Trainer")


        

    def back(self):
        self.widget.setCurrentIndex(1)

    def session(self):       
        # if self.table.rowCount==0:
        #     self.error.setText("Enter atleast one Session")
        # else:
        pickup=self.pickupLineEdit.text()
        drop=self.dropLineEdit.text()
        tid=self.idLineEdit.text()   
        to=self.totimeEdit.time()
        fr=self.frtimeEdit.time()
        fr=str(fr)
        l=len(fr)
        fr=fr[19:l-1].split(',')
        print(fr)
        mi=fr[1]
        timefr=fr[0]+":"+mi[1:]
        to=str(to)
        l=len(to)
        to=to[19:l-1].split(',')
        mi=to[1]
        timeto=to[0]+":"+mi[1:]
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """INSERT INTO session VALUES(null,?,?,?,?,?)"""
        query2="""SELECT seq FROM sqlite_sequence WHERE name='session' """
        
        try:
            c.execute(query2)
            sid=c.fetchone()
            c.execute(query,(tid,timefr,timeto,pickup,drop))
            msg=General_Dialog()
            msg.id(str(sid[0]))
            x=msg.exec_()

        except:
            self.error.setText("Error Occured")


        conn.commit()
        conn.close()


