import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sqlite3

class Student_Dialog(QDialog):
    def __init__(self):
        super(Student_Dialog, self).__init__()
        loadUi("Trainer Dialog.ui", self)
        self.CancelButton.clicked.connect(self.cancel)

    def id(self,id):
        self.nameLabel.setText("Student Deatils with id "+id+" Saved Successfully")

    def delete(self,id):
        self.nameLabel.setText("Student Deatils with id "+id+" Deleted Successfully")

    def cancel(self):
        self.close()

class Student_Details(QMainWindow):
    def __init__(self,widget):
        super(Student_Details,self).__init__()
        loadUi("Student.ui",self)
        self.widget=widget
        self.BackButton.clicked.connect(self.back)
        self.SaveButton.clicked.connect(self.save)
        date=self.dOBDateEdit.date()
        
        d=str(date)
        l=len(d)
        d=d[19:l-1].split(',')
        
    def save(self):
        if self.nameLineEdit.text()=="" or self.addressLineEdit.text()=="" or self.ageLineEdit.text()=="" or self.mobileNumberLineEdit.text()=="" or self.pickupLineEdit.text()=="" or self.dropLineEdit.text()=="":
            self.error.setText("Enter all inputs")
        else:
            name=self.nameLineEdit.text()
            address=self.addressLineEdit.text()
            age=self.ageLineEdit.text()
            mobilenumber=self.mobileNumberLineEdit.text()
            DOB=self.dOBDateEdit.date()
            dob=str(DOB)
            l=len(dob)
            dob=dob[19:l-1].split(',')
            date=dob[2]
            mon=dob[1]
            year=dob[0]
            dateofjoining=self.dateOfJoiningDateEdit.date()
            doj=str(dateofjoining)
            l=len(doj)
            doj=doj[19:l-1].split(',')
            date1=doj[2]
            mon1=doj[1]
            year1=doj[0]
            trainerid=self.idLineEdit.text()
            trainername=self.trainerNameLineEdit.text()
            pickup=self.pickupLineEdit.text()
            drop=self.dropLineEdit.text()
            fr=self.trtimeEdit.time()
            to=self.totimeEdit.time()
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
            query = """INSERT INTO student VALUES (null,?,?,?,?,?,?,?,?)"""
            query2="""SELECT * FROM session WHERE Trainer_id=?"""
            query3="""SELECT Student_id FROM student WHERE Name=? and Address=?"""
            c.execute(query2,(trainerid,))
            ss=c.fetchall()
            for session in ss:
                if session[2]==timefr and session[3]==timeto and session[4]==pickup and session[5]==drop:
                    c.execute(query,(name,str(date[1:]+"/"+mon[1:]+"/"+year),address,int(age),str(date1[1:]+"/"+mon1[1:]+"/"+year1),int(mobilenumber),trainerid,session[0]))
                    c.execute(query3,(name,address,))
                    st=c.fetchone()
                    dialog=Student_Dialog()
                    dialog.id(str(st[0]))
                    x=dialog.exec_()
                    conn.commit()
                    conn.close() 
                    break 


            else:
                self.error.setText("No Such Session Found")

           

    def back(self):
        self.widget.setCurrentIndex(1)

class Student_Search(QMainWindow):
    def __init__(self,widget):
        self.widget=widget
        super(Student_Search,self).__init__()
        loadUi("Student Search.ui",self)
        
        self.BackButton.clicked.connect(self.back)
        self.SearchButton.clicked.connect(self.search)
        self.SeeDetailsButton.clicked.connect(self.details)

    def back(self):
        self.widget.setCurrentIndex(1)

    def details(self):
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """SELECT * FROM student WHERE Student_id=?"""
        c.execute(query,(self.idlineEdit.text(),))
        stu=c.fetchall()
        
        if stu==[]:
            self.error_2.setText("Invalid Student ID")
            
        else:
            
            self.view=Student_View(self.idlineEdit.text())
            self.view.show()
            self.idlineEdit.setText("")

    def search(self):
        if self.namelineEdit.text()=="":
            self.error.setText("Enter the Student name")
        else:
            name=self.namelineEdit.text()
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM student WHERE Name=?"""
            
            c.execute(query,(name,))
            st=c.fetchall()
            if st==[]:
                self.error.setText("Invalid Student")
            else:
                row=0
                self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                rowPosition = self.table.setRowCount(len(st))
                for student in st:
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(student[0])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(student[1])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(student[6])))
                    row+=1

                conn.commit()
                conn.close()



class Student_View(QMainWindow):
    def __init__(self,Studentid):
        super(Student_View,self).__init__()
        self.id=Studentid
        
        loadUi("Student View.ui",self)
        self.initialize()
        self.EditButton.clicked.connect(self.edit)
        self.SaveButton.setEnabled(False)
        self.SaveButton.clicked.connect(self.save)
        self.DeleteButton.clicked.connect(self.delete)

    def delete(self):
        
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """DELETE FROM trainer WHERE Trainer_id=?"""
        
        c.execute(query,(self.id,))
        conn.commit()
        conn.close()
        dialog=Student_Dialog()
        dialog.delete(self.id)
        x=dialog.exec_()

        self.close()

    def save(self):
        if self.nameLineEdit.text()=="" or self.addressLineEdit.text()=="" or self.ageLineEdit.text()=="" or self.mobileNumberLineEdit.text()=="" or self.pickupLineEdit.text()=="" or self.dropLineEdit.text()=="":
            self.error.setText("Enter all inputs")
        else:
            name=self.nameLineEdit.text()
            address=self.addressLineEdit.text()
            age=self.ageLineEdit.text()
            mobilenumber=self.mobileNumberLineEdit.text()
            DOB=self.dOBDateEdit.date()
            dob=str(DOB)
            l=len(dob)
            dob=dob[19:l-1].split(',')
            date=dob[2]
            mon=dob[1]
            year=dob[0]
            dateofjoining=self.dateOfJoiningDateEdit.date()
            doj=str(date)
            l=len(doj)
            doj=doj[19:l-1].split(',')
            date1=doj[2]
            mon1=doj[1]
            year1=doj[0]
            trainerid=self.idLineEdit.text()
            trainername=self.trainerNameLineEdit.text()
            pickup=self.pickupLineEdit.text()
            drop=self.dropLineEdit.text()
            fr=self.trtimeEdit.time()
            to=self.totimeEdit.time()
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
            query = """UPDATE student SET Name=?,Address=?,Age=?,MobileNumber=?,DOB=?,JoinigDate=?,Trainer_id=?,Session_id=? WHERE Student_id=?"""
            query2="""SELECT * FROM session WHERE Trainer_id=?"""
            c.execute(query2,(trainerid,))
            ss=c.fetchall()
            for session in ss:
                if session[2]==timefr and session[3]==timeto and Picking_location==pickup and Droping_location==drop:
                    c.execute(query,(name,address,int(age),int(mobilenumber),str(date[1:]+"/"+mon[1:]+"/"+year),str(date1[1:]+"/"+mon1[1:]+"/"+year1),trainerid,session[0],int(self.id)))
                    break
            else:
                self.error.setText("No Such Session Found")

            conn.commit()
            conn.close()



    def edit(self):
        self.nameLineEdit.setEnabled(True)
        self.addressLineEdit.setEnabled(True)
        self.ageLineEdit.setEnabled(True)
        self.mobileNumberLineEdit.setEnabled(True)
        self.dOBDateEdit.setEnabled(True)
        self.dateOfJoiningDateEdit.setEnabled(True)
        self.idLineEdit.setEnabled(True)
        self.pickupLineEdit.setEnabled(True)
        self.dropLineEdit.setEnabled(True)
        self.frtimeEdit.setEnabled(True)
        self.totimeEdit.setEnabled(True)
        
        self.SaveButton.setEnabled(True)


    def initialize(self):
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """SELECT * FROM student WHERE Student_id=?"""
        query2="""SELECT * FROM session WHERE Session_id=?"""
        query3="""SELECT Name FROM trainer WHERE Trainer_id=?"""
        c.execute(query,(self.id,))
        details=c.fetchone()
        _id=details[0]
        name = details[1]
        address = details[3]
        age = details[4]
        mobilenumber = details[6]
        dob=details[2]
        dob=dob.split('/')
        doj=details[5]
        doj=doj.split('/')
        trainer=details[7]
        session=details[8]
        self.nameLineEdit.setText(str(name))
        self.addressLineEdit.setText(str(address))
        self.ageLineEdit.setText(str(age))
        self.mobileNumberLineEdit.setText(str(mobilenumber))
        self.dOBDateEdit.setDate(QtCore.QDate(int(dob[2]),int(dob[1]),int(dob[0])))
        self.dateOfJoiningDateEdit.setDate(QtCore.QDate(int(doj[2]),int(doj[1]),int(doj[0])))
        self.idLineEdit.setText(str(trainer))
        c.execute(query2,(session,))
        details=c.fetchone()
        totime=str(details[3])
        totime=totime.split(':')
        frtime=str(details[2])
        frtime=frtime.split(':')
        self.pickupLineEdit.setText(str(details[4]))
        self.dropLineEdit.setText(str(details[5]))
        self.frtimeEdit.setTime(QtCore.QTime(int(frtime[0]),int(frtime[1])))
        self.totimeEdit.setTime(QtCore.QTime(int(totime[0]),int(totime[1])))
        c.execute(query3,(trainer,))
        details=c.fetchone()
        self.trainerNameLineEdit.setText(details[0])
        conn.commit()
        conn.close()
        self.nameLineEdit.setEnabled(False)
        self.addressLineEdit.setEnabled(False)
        self.ageLineEdit.setEnabled(False)
        self.mobileNumberLineEdit.setEnabled(False)
        self.dOBDateEdit.setEnabled(False)
        self.dateOfJoiningDateEdit.setEnabled(False)
        self.idLineEdit.setEnabled(False)
        self.pickupLineEdit.setEnabled(False)
        self.dropLineEdit.setEnabled(False)
        self.frtimeEdit.setEnabled(False)
        self.totimeEdit.setEnabled(False)
        self.trainerNameLineEdit.setEnabled(False)


        
        


