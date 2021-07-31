import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QWidget, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QFont

class HexEdit(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.openfilename = ''

    def initUI(self):

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

        centralWidget = QWidget()
        centralWidget.setLayout(self.createMain())
        self.setCentralWidget(centralWidget)

        # Set Window
        self.setWindowTitle('HexEdit')
        self.setGeometry(0,0,800,600)
        self.show()

    def createMain(self):
        # Main view
        # offsetArea, hexArea, stringArea: devide by 3-Widget 

        qhBox = QHBoxLayout()
        self.offsetArea = QTextEdit()
        self.hexArea = QTextEdit()
        self.stringArea = QTextEdit()

        self.offsetArea.setReadOnly(True)

        syncScroll(self.hexArea, self.stringArea, self.offsetArea)

        qhBox.addWidget(self.offsetArea, 1)
        qhBox.addWidget(self.hexArea, 6)
        qhBox.addWidget(self.stringArea, 2)

        return qhBox

    def openFile(self):
        # Open a file using the getOpenFileName() method
        # The third parameter allows you to set the default path.('./')
        # It is also set to open all files ( * ) by default.
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

        if fname[0]: #Error prevention when there is no file selection
            self.openfilename = fname[0]
            file = open(fname[0], 'rb') #rb
            self.setWindowTitle(fname[0])

            with file:
                #TODO Modify this part to import as hex and string
                bindata = file.read()
                hexView(self, bindata) # Hex Viewer for opened file

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

def hexView(self, text):

    hexa = text.hex()
    offset = 0

    offsetText = ''
    hexaText = ''
    stringText = ''
    
    rowlength = 16

    for i in range(0, len(text)):
        
        # for formating String Text
            # char = chr(text[i])
            # stringText += char
            # hexaText += hexa[i*2] + hexa[i*2+1] + '  '

        hexaText += '{0:>6}'.format(hexa[i*2] + hexa[i*2+1])
        buf = text[i]

        if (buf >= 0 and buf <= 32) or buf == 127 or buf == 10:
            stringText += ' '
        
        elif buf >= 127:
            stringText += '.'
        
        else:
            stringText += chr(text[i])

        if i % rowlength == 15:
            hexaText += '\n'
            stringText += '\n'
            offsetText += format(offset, '08x') + '\n'
            offset += 16

    offsetText += format(offset, '08x') + '\n'
    offsetText = offsetText.upper()
    hexaText = hexaText.upper() 

    # Called into the text editing widget via the setText() method.
    self.offsetArea.setText(offsetText)
    self.hexArea.setText(hexaText)
    self.stringArea.setText(stringText)	

def syncScroll(textArea0, textArea1, textArea2):
    # Synchronize scrolls for 3-Widget
    scroll0 = textArea0.verticalScrollBar()
    scroll1 = textArea1.verticalScrollBar()
    scroll2 = textArea2.verticalScrollBar()

    scroll0.valueChanged.connect(    
        scroll1.setValue
    )

    scroll0.valueChanged.connect(    
        scroll2.setValue
    )

    scroll1.valueChanged.connect(    
        scroll0.setValue
    )

    scroll1.valueChanged.connect(    
        scroll2.setValue
    )
    
    scroll2.valueChanged.connect(    
        scroll0.setValue
    )
    
    scroll2.valueChanged.connect(    
        scroll1.setValue
    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HexEdit()
    sys.exit(app.exec_())