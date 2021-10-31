import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My App")

		# crearing a layout for window
		self.setLayout(qtw.QVBoxLayout())

		# creating a label and adding to the layout
		my_label=qtw.QLabel("Hi Welcome !")
		self.layout().addWidget(my_label)

		# seting the font
		my_label.setFont(qtg.QFont('Helvetica',20))

		# text widget
		my_entry=qtw.QLineEdit()
		my_entry.setObjectName("name field")
		my_entry.setText("OM")
		self.layout().addWidget(my_entry)

		#creating a combo box
		my_combo=qtw.QComboBox(editable=True , insertPolicy=qtw.QComboBox.InsertAtBottom )
		self.layout().addWidget(my_combo)
		my_combo.addItem("one",'something')#one is the item and something is the data for item
		my_combo.addItem("two")
		my_combo.addItems(['three','four'])
		my_combo.insertItem(1,'six')

		# creating a spin box
		
		my_button=qtw.QPushButton("Click Here",clicked=lambda : press_it())
		self.layout().addWidget(my_button)

		self.show()

		def press_it():
			my_label.setText(f"Hi Wecome {my_entry.text()}!")
			my_entry.setText("")


app=qtw.QApplication([])
mw=MainWindow()
app.exec_()