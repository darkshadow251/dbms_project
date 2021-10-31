import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sqlite3

class Trainer_Dialog(QDialog):
    def __init__(self):
        super(Trainer_Dialog, self).__init__()
        loadUi("Trainer Dialog.ui", self)
        self.CancelButton.clicked.connect(self.cancel)

    def id(self,id):
        self.nameLabel.setText("Trainer Deatils with id "+id+" Saved Successfully")

    def delete(self,id):
        self.nameLabel.setText("Trainer Deatils with id "+id+" Deleted Successfully")

    def update(self,id):
        self.nameLabel.setText("Trainer Deatils with id "+id+" Updated Successfully")


    def cancel(self):
        self.close()

class Trainer_View(QMainWindow):
    def __init__(self, trainerid):
        super(Trainer_View, self).__init__()
        loadUi("Trainer View.ui", self)
        self.id = trainerid
        self.intialize()
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
        dialog=Trainer_Dialog()
        dialog.delete(self.id)
        x=dialog.exec_()

        self.close()
    def save(self):
        if self.nameLineEdit.text()=="" or self.addressLineEdit.text()=="" or self.ageLineEdit.text()=="" or self.mobileNumberLineEdit.text()=="":
            self.error.setText("Enter all inputs")
        elif self.table.rowCount==0:
            self.error.setText("Enter atleast one Session")

       
        else:
            name = self.nameLineEdit.text()
            address = self.addressLineEdit.text()
            age = int(self.ageLineEdit.text())
            mobilenumber = int(self.mobileNumberLineEdit.text())
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """UPDATE trainer SET Name=?,Address=?,Age=?,MobileNumber=? WHERE Trainer_id=?"""
            

            # try:
            c.execute(query,(name,address,age,mobilenumber,int(self.id)))
            
            
               

            dialog=Trainer_Dialog()
            dialog.update(self.id)
            x=dialog.exec_()


            # except:
            #   self.error.setText("Error Ocurred")
            conn.commit()
            conn.close()





    def edit(self):
        self.nameLineEdit.setEnabled(True)
        self.addressLineEdit.setEnabled(True)
        self.ageLineEdit.setEnabled(True)
        self.mobileNumberLineEdit.setEnabled(True)
        self.pickupLineEdit.setEnabled(True)
        self.dropLineEdit.setEnabled(True)
        self.frtimeEdit.setEnabled(True)
        self.totimeEdit.setEnabled(True)
        self.AddSessionButton.setEnabled(True)
        self.SaveButton.setEnabled(True)

    def intialize(self):
        conn = sqlite3.connect('Driving_School.db')
        c = conn.cursor()
        query = """SELECT * FROM trainer WHERE Trainer_id=?"""
        query2="""SELECT * FROM session WHERE Trainer_id=?"""
        c.execute(query,(self.id,))
        details=c.fetchone()
        _id=details[0]
        name = details[1]
        address = details[2]
        age = details[3]
        mobilenumber = details[4]
        self.nameLineEdit.setText(str(name))
        self.addressLineEdit.setText(str(address))
        self.ageLineEdit.setText(str(age))
        self.mobileNumberLineEdit.setText(str(mobilenumber))
        c.execute(query2,(self.id,))
        details=c.fetchall()
        row=0
        self.table.setRowCount(len(details))
        for session in details:
            self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(session[2])+" to "+str(session[3])))
            self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(session[4])))
            self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(session[5])))
            row+=1

        conn.commit()
        conn.close()
        self.nameLineEdit.setEnabled(False)
        self.addressLineEdit.setEnabled(False)
        self.ageLineEdit.setEnabled(False)
        self.mobileNumberLineEdit.setEnabled(False)
        self.pickupLineEdit.setEnabled(False)
        self.dropLineEdit.setEnabled(False)
        self.frtimeEdit.setEnabled(False)
        self.totimeEdit.setEnabled(False)
        self.AddSessionButton.setEnabled(False)




        
    #     self.BackButton.clicked.connect(self.back)

    # def back(self):
    #     self.widget.setCurrentIndex(1)


class Trainer_Search(QMainWindow):
    def __init__(self, widget):
        super(Trainer_Search, self).__init__()
        loadUi("Trainer Search.ui", self)
        self.widget = widget
        self.BackButton.clicked.connect(self.back)
        self.SearchButton.clicked.connect(self.search)
        self.SeeDetailsButton.clicked.connect(self.details)

    def back(self):
        self.widget.setCurrentIndex(1)

    def search(self):
        if self.namelineEdit.text()=="":
            self.error.setText("Enter the Trainer name")
        else:
            name=self.namelineEdit.text()
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """SELECT * FROM trainer WHERE Name=?"""
            try:
                c.execute(query,(name,))
                tr=c.fetchall()
                row=0
                self.table.setRowCount(len(tr))
                for trainer in tr:
                    self.table.setItem(row , 0, QtWidgets.QTableWidgetItem(str(trainer[0])))
                    self.table.setItem(row , 1, QtWidgets.QTableWidgetItem(str(trainer[1])))
                    self.table.setItem(row , 2, QtWidgets.QTableWidgetItem(str(trainer[4])))
                    row+=1
            except:
                self.error.setText("Invalid Trainer")

    def details(self):
        if self.lineEdit.text()=="":
            self.error1.setText("Enter the Trainer id")

        else:
            # self.view=QtWidgets.QMainWindow()
            self.view=Trainer_View(self.lineEdit.text())
            self.view.show()



class Trainer_Details(QMainWindow):
    def __init__(self, widget):
        super(Trainer_Details, self).__init__()
        loadUi("Trainer.ui", self)
        self.widget = widget
        self.BackButton.clicked.connect(self.back)
        self.SaveButton.clicked.connect(self.save)
        
    def back(self):
        self.widget.setCurrentIndex(1)


    



    def save(self):
        if self.namelineEdit.text()=="" or self.addressLineEdit.text()=="" or self.ageLineEdit.text()=="" or self.mobileNumberLineEdit.text()=="":
            self.error.setText("Enter all inputs")


       
        else:
            name = self.namelineEdit.text()
            address = self.addressLineEdit.text()
            age = int(self.ageLineEdit.text())
            mobilenumber = int(self.mobileNumberLineEdit.text())
            conn = sqlite3.connect('Driving_School.db')
            c = conn.cursor()
            query = """INSERT INTO trainer VALUES(null,?,?,?,?)"""
            query2 ="""SELECT Trainer_id  FROM trainer WHERE Name=? AND Address=?"""

            try:
                c.execute(query,(name,address,age,mobilenumber,))
                c.execute(query2 ,(name,address))
                tr=c.fetchone()
               

                dialog=Trainer_Dialog()
                dialog.id(str(tr[0]))
                x=dialog.exec_()


            except:
              self.error.setText("Error Ocurred")
            conn.commit()
            conn.close()

            self.namelineEdit.setText("")
            self.addressLineEdit.setText("")
            self.ageLineEdit.setText("")
            self.mobileNumberLineEdit.setText("")
            

