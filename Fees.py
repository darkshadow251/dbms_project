import sys
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5 import QtGui
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

    def add(self,id):
        self.nameLabel.setText("Transaction Added Successfully")

    def exam(self,id):
        self.nameLabel.setText("Exam Details Added "+id+" Successfully")

    def delete(self,id):
        self.nameLabel.setText("Session Deatils with id "+id+" Deleted Successfully")

    def cancel(self):
        self.close()

class Fees_Details(QMainWindow):
    def __init__(self,widget):
        super(Fees_Details,self).__init__()
        loadUi("Fees.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)
        self.SeeDetailsButton.clicked.connect(self.details)
        self.AddTransactionButton.clicked.connect(self.add)
        self.table.setColumnWidth(2,300)
        
    def add(self):
        if self.amountLineEdit.text()=="" or self.descriptionLineEdit.text()=="" or self.idlineEdit_2.text()=="":
            self.Error.setText("Enter all inputs")

        else:
            self.Error.setText("")
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """INSERT INTO fees VALUES (null,?,?,?,?)"""
            sid=str(self.idlineEdit_2.text())
            amount=int(self.amountLineEdit.text())
            des=str(self.descriptionLineEdit.text())
            date=self.dateEdit.date() 
            date=str(date)
            l=len(date)
            date=date[19:l-1].split(',')
            Date=date[2]
            mon=date[1]
            year=date[0]
            try:

                c.execute(query,(sid,str(Date+"/"+mon+"/"+year),amount,des))
                conn.commit()
                conn.close()

                msg=General_Dialog()
                msg.add()
                x=msg.exec_()

            except:
                self.Error.setText("Invalid Student")



    def back(self):
        self.widget.setCurrentIndex(1)

    def details(self):
        if self.idlineEdit.text()=="":
            self.error1.setText("Enter the Student id")
        else:
            self.error.setText("")
            
            feespaid=0
            feesremaining=4000
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM fees WHERE Student_id=?"""
            sid=self.idlineEdit.text()
            
            c.execute(query,(int(sid),))
            trans=c.fetchall()
            if trans==[]:
                self.error1.setText("Invalid Student")
            else:
                self.totalAmountLabel.setText("4000")    
                row=0
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                self.table.setRowCount(len(trans))
                for transaction in trans:
                    am=int(transaction[3])
                    feespaid+=am
                    feesremaining-=am
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(transaction[3])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(transaction[2])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(transaction[4])))
                    row+=1

                conn.commit()
                conn.close()
                self.feesPaidLabel.setText(str(feespaid))
                self.feesRemainingLabel.setText(str(feesremaining))

class Session_View(QMainWindow):
    def __init__(self,Sessionid):
        super(Session_View,self).__init__()
        loadUi("Session View.ui",self)
        self.id=Sessionid
        self.EditButton.clicked.connect(self.edit)
        self.SaveButton.clicked.connect(self.save)
        self.DeleteButton.clicked.connect(self.delete)
        self.SessionLineEdit.setText(str(self.id))
        
        self.initialize()

    def initialize(self):
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query="""SELECT * FROM session WHERE Session_id=? """
        c.execute(query,(self.id))
        se=c.fetchone()
        self.pickupLineEdit.setText(str(se[4]))
        self.SessionLineEdit.setText(str(se[0]))
        self.dropLineEdit.setText(str(se[5]))
        self.idLineEdit.setText(str(se[1]))
        time=str(se[2])
        time=time.split(':')
        self.frtimeEdit.setTime(QTime(int(time[0]),int(time[1])))
        time=str(se[3])
        time=time.split(':')
        self.totimeEdit.setTime(QTime(int(time[0]),int(time[1])))
        self.SessionLineEdit.setEnabled(False)
        self.pickupLineEdit.setEnabled(False)
        self.dropLineEdit.setEnabled(False)
        self.idLineEdit.setEnabled(False)
        self.frtimeEdit.setEnabled(False)
        self.totimeEdit.setEnabled(False)
        self.SaveButton.setEnabled(False)



    def save(self):
        if self.pickupLineEdit.text()=="" or  self.dropLineEdit.text()=="" or self.idLineEdit.text()=="":
            self.error.setText("Enter all inputs")    
        else:
            self.error.setText("")
            pickup=self.pickupLineEdit.text()
            drop=self.dropLineEdit.text()
            tid=self.idLineEdit.text()   
            to=self.totimeEdit.time()
            fr=self.frtimeEdit.time()
            fr=str(fr)
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
            query = """UPDATE session SET Trainer_id=?,Start_time=?,End_time=?,Picking_location=?,Droping_location=? WHERE Session_id=?"""
            query2="""SELECT seq FROM sqlite_sequence WHERE name='session' """
            
            try:
                c.execute(query2)
                sid=c.fetchone()
                c.execute(query,(tid,timefr,timeto,pickup,drop,int(self.id)))
                msg=General_Dialog()
                msg.id(str(self.id))
                x=msg.exec_()

            except:
                self.error.setText("Error Occured")


            conn.commit()
            conn.close()

    def delete(self):
        
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """DELETE FROM session WHERE Session_id=?"""
        
        c.execute(query,(self.id,))
        conn.commit()
        conn.close()
        dialog=General_Dialog()
        dialog.delete(self.id)
        x=dialog.exec_()

        self.close()

    def edit(self):
        self.pickupLineEdit.setEnabled(True)
        self.dropLineEdit.setEnabled(True)
        self.idLineEdit.setEnabled(True)
        self.frtimeEdit.setEnabled(True)
        self.totimeEdit.setEnabled(True)
        self.SaveButton.setEnabled(True)

class Session_Details(QMainWindow):
    def __init__(self,widget):
        super(Session_Details,self).__init__()
        loadUi("Session.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)
        self.AddSessionButton.clicked.connect(self.addsession)
        self.SearchButton.clicked.connect(self.search)
        self.ManageSessionButton.clicked.connect(self.managesession)
        self.table.setColumnWidth(4,250)
        self.table.setColumnWidth(5,250)
        
    def search(self):
        if self.idLineEdit_2.text()=="" and str(self.frtimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)":
            self.error1.setText("Enter the Trainer name")


        elif self.idLineEdit_2.text()!="" and str(self.frtimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())=="PyQt5.QtCore.QTime(0, 0)" :
            tid=self.idLineEdit_2.text()
            self.error1.setText("")
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM session WHERE Trainer_id=?"""
            try:
                c.execute(query,(tid,))
                se=c.fetchall()
                row=0
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
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

        elif self.idLineEdit_2.text()!="" and str(self.frtimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)" and str(self.totimeEdit_2.time())!="PyQt5.QtCore.QTime(0, 0)":
            fr=str(self.frtimeEdit_2.time())
            to=str(self.totimeEdit_2.time())
            self.error1.setText("")
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
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
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
            self.error1.setText("")
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
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
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

    def addsession(self):
        if self.pickupLineEdit.text()=="" or  self.dropLineEdit.text()=="" or self.idLineEdit.text()=="":
            self.error.setText("Enter all inputs")    
        else:
            self.error.setText("")
            pickup=self.pickupLineEdit.text()
            drop=self.dropLineEdit.text()
            tid=self.idLineEdit.text()   
            to=self.totimeEdit.time()
            fr=self.frtimeEdit.time()
            fr=str(fr)
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
                self.error.setText("Invalid Trainer")


            conn.commit()
            conn.close()

    def managesession(self):
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """SELECT * FROM session WHERE Session_id=?"""
        c.execute(query,(self.SessionLineEdit.text(),))
        se=c.fetchall()
        
        if se==[]:
            self.error_2.setText("Invalid Session ID")
            
        else:
            
            self.view=Session_View(self.SessionLineEdit.text())
            self.view.show()
            self.SessionLineEdit.setText("")


class Exam_Details(QMainWindow):
    def __init__(self,widget):
        super(Exam_Details,self).__init__()
        loadUi("Exam.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)
        self.SearchButton.clicked.connect(self.search)
        self.SaveButton.clicked.connect(self.save)



    def search(self):
        if self.examLineEdit.text()=="" and self.studentLineEdit.text()=="":
            self.error1.setText("Enter the Student id or Exam id")


        elif self.examLineEdit.text()!="" and self.studentLineEdit.text()=="" :
            self.error1.setText("")
            eid=self.examLineEdit.text()
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM exam WHERE Exam_id=?"""
            try:
                c.execute(query,(eid,))
                ex=c.fetchall()
                row=0
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                self.table.setRowCount(len(ex))
                for exam in ex:
                    
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(exam[1])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(exam[2])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(exam[3])))
                    self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(exam[4])))
                    row+=1
            except:
                self.error1.setText("Invalid Exam id")

        elif self.examLineEdit.text()!="" and self.studentLineEdit.text()!="":
            self.error1.setText("")
            student=str(self.studentLineEdit.text())
            exam=str(self.examLineEdit.text())

            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM exam WHERE Exam_id=? and Student_id=?"""
            try:
                c.execute(query,(student,exam,))
                ex=c.fetchall()
                row=0
                self.table.setRowCount(len(ex))
                for exam in ex:
                    
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(exam[1])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(exam[2])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(exam[3])))
                    self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(exam[4])))
                        
                    row+=1
            except:
                self.error1.setText("Invali Exam id or Student id")

        elif self.examLineEdit.text()=="" and self.studentLineEdit.text()!="":
            self.error1.setText("")
            student=str(self.studentLineEdit.text())
            
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM exam WHERE Student_id=?"""
            try:
                c.execute(query,(student,exam,))
                ex=c.fetchall()
                row=0
                self.table.setRowCount(len(ex))
                for exam in ex:
                    
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(exam[1])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(exam[2])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(exam[3])))
                    self.table.setItem(row , 3, QtWidgets.QTableWidgetItem(str(exam[4])))
                        
                    row+=1
            except:
                self.error1.setText("Invalid Student id")

    def save(self):
        if self.ExamLineEdit.text()=="" or  self.StudentLineEdit.text()=="" or self.ScoreLineEdit.text()=="":
            self.error.setText("Enter all inputs")       
        # if self.table.rowCount==0:
        #     self.error.setText("Enter atleast one Session")
        else:
            self.error.setText("")
            score=self.ScoreLineEdit.text()
            exam=self.ExamLineEdit.text()
            student=self.StudentLineEdit.text()   
     
            Date=self.DateEdit.date()
            doe=str(Date)
            l=len(doe)
            doe=doe[19:l-1].split(',')
            date=doe[2]
            mon=doe[1]
            year=doe[0]
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """INSERT INTO exam VALUES(null,?,?,?,?)"""
            query2="""SELECT seq FROM sqlite_sequence WHERE name='exam' """
            
            try:
                c.execute(query,(exam,student,str(date+"/"+mon+"/"+year),score,))
                c.execute(query2)
                sid=c.fetchone()
               
                msg=General_Dialog()
                msg.exam(str(sid[0]))
                x=msg.exec_()

            except:
                self.error.setText("Invalid Student")


            conn.commit()
            conn.close()       

    def back(self):
        self.widget.setCurrentIndex(1)


