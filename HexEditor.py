import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

class HexEdit(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()
		self.openfilename = ''

	def initUI(self):
		# TODO EditBoard
		self.textEdit = QTextEdit()
		self.setCentralWidget(self.textEdit)
		self.statusBar()

		# MenuBar - New
		# newfileAction = QAction("New", self)
		# newfileAction.setShortcut("Ctrl+N")
		# newfileAction.setStatusTip('Create New File')
		# newfileAction.triggered.connect(self.newFile)

		# MenuBar - Open file
		openfileAction = QAction('Open', self)
		openfileAction.setShortcut('Ctrl+O')
		openfileAction.setStatusTip('Open New File')
		openfileAction.triggered.connect(self.openFile)

		# MenuBar - Save
		savefileAction = QAction('Save', self)
		savefileAction.setShortcut('Ctrl+S')
		savefileAction.setStatusTip('Save File')
		savefileAction.triggered.connect(self.saveFile)

		# MenuBar - Save as
		saveAsfileAction = QAction('Save as', self)
		saveAsfileAction.setShortcut('F12')
		saveAsfileAction.setStatusTip('Save as File')
		saveAsfileAction.triggered.connect(self.saveAsFile)

		# MenuBar - Exit
		exitAction = QAction('Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit apllication')
		exitAction.triggered.connect(qApp.quit)

		# Set MenuBar
		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)

		filemenu = menubar.addMenu('&File')
		# filemenu.addAction(newfileAction)
		filemenu.addAction(openfileAction)
		filemenu.addAction(savefileAction)
		filemenu.addAction(saveAsfileAction)
		filemenu.addAction(exitAction)

		# Set Window
		self.setWindowTitle('HexEdit')
		self.setGeometry(0,0,800,600)
		self.show()

	def openFile(self):
		# Open a file using the getOpenFileName() method
		# The third parameter allows you to set the default path.('./')
		# It is also set to open all files ( * ) by default.
		fname = QFileDialog.getOpenFileName(self, 'Open file', './')

		if fname[0]: #Error prevention when there is no file selection
			self.openfilename = fname[0]
			file = open(fname[0], 'r') #rb
			self.setWindowTitle(fname[0])

			with file:
				#TODO Modify this part to import as hex and string
				# Called into the text editing widget via the setText() method.
				bindata = file.read()
				self.textEdit.setText(bindata)

	def saveFile(self):
		#TODO Must be stored in binary format ('wb')
		file = open(self.openfilename, 'w') # -> Modify this part
		text = self.textEdit.toPlainText() # -> Modify this part
		file.write(text)
		file.close()

	def saveAsFile(self):
		fname = QFileDialog.getSaveFileName(self, 'Save as file')

		if fname[0]:
			file = open(fname[0], 'w')

			#TODO Must be stored in binary format ('wb')
			text = self.textEdit.toPlainText() # -> Modify this part
			file.write(text)
			file.close()

	# Implemented to select a location and filename when creating a new file
	# def newFile(self):
	# 	#TODO Implemented by dividing hex and string
	# 	self.textEdit = QTextEdit()
	# 	self.setCentralWidget(self.textEdit)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = HexEdit()
	sys.exit(app.exec_())