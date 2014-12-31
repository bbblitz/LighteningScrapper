from PyQt4 import QtCore, QtGui
from threading import Thread
import os
import sys
import proxyScrapper

class Input(QtGui.QDialog):
    scrapping = False
    css = """
    QWidget
    {
    Background:#111;
    color: #fff;
    font:13px italic;
    font-weight:bold;
    border-radius: 2px;
    border: 1px solid #383838;
    text-align: center;
    vertical-align: middle;
    }
    QDialog{
    background-image:url('http://www.sinister.ly/images/e-red/mainbg.png') top left repeat -x;
    font-size:13px;
    color: #fff;
    border: 1px solid #383838;
    }
    QLineEdit:hover{
    background: #831010;
    font-size: 12px;
    height: 43px;
    color:black;
    }
    QLineEdit{
    Background: #211;
    font-size:12px;
    height:43px;
    color:#383838;
    }
    QPushButton:hover{
    Background:#831010;
    font-size:12px;
    color:black;
    }
    QPushButton{
    Background: #211;
    font-size:12px;
    color:#383838;
    }
    QSpinBox{
    Background: #211;
    font-size:12px;
    height: 43px;
    color:#383838;
    border: 1px solid #383838;
    padding-top: 3px;
    padding-bottom: 3px;
    }
    QSpinBox:hover{
    Background:#831010;
    font-size:12px;
    height:43px;
    color:black;
    }
    """
    def __init__(self):
        super(Input, self).__init__()
        topLayout = QtGui.QHBoxLayout()
        topLayout.addStretch()
        mainLayout = QtGui.QVBoxLayout()
        self.startButton = QtGui.QPushButton("Scrap proxies")
        self.closeButton = QtGui.QPushButton(" X ")
        self.closeButton.clicked.connect(self.exitWindow)
        mainLayout.addLayout(topLayout)
        topLayout.addWidget(self.closeButton)
        self.output = QtGui.QTextEdit()
        self.output.setReadOnly(True)
        self.setStyleSheet(self.css)
        layout = self.createBits()
        mainLayout.addWidget(layout)
        mainLayout.addWidget(self.startButton)
        mainLayout.addWidget(self.output)
        self.startButton.clicked.connect(self.makeConcurrent)
        self.setLayout(mainLayout)
        self.setWindowTitle("Lightening scrapper")
        self.setWindowIcon(QtGui.QIcon("./Lightning.ico"))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.output.append("#######################\n"+
                           "##      Lightening scrapper\n"+
                           "##      By: Alexander Pickering  \n"+
                           "##      Beta version \n"+
                           "#######################\n")
    def exitWindow(self):
        self.close()

    def createBits(self):
        ret = QtGui.QGroupBox("")
        layout = QtGui.QFormLayout()
        
        boxLabel = QtGui.QLabel("\nText file containing proxies\n Proxies must be in the format \"address:port\"")
        self.textInput = QtGui.QLineEdit()
        counterLabel = QtGui.QLabel("\nMaximum number of threads to run")
        self.counterSpin = QtGui.QSpinBox()
        self.counterSpin.setMaximum(5000)
        layout.addRow(boxLabel)
        layout.addRow(self.textInput)
        layout.addRow(counterLabel)
        layout.addRow(self.counterSpin)
        self.delayLabel = QtGui.QLabel("\nOS response delay(ms)")
        self.delayspin = QtGui.QSpinBox()
        layout.addRow(self.delayLabel)
        layout.addRow(self.delayspin)
        ret.setLayout(layout)
        return ret

    def makeConcurrent(self):
        thre = Thread(target=self.startScrap)
        thre.start()
        
    main = None
    def startScrap(self):
        file = self.textInput.text()
        num = self.counterSpin.value()
        if(self.scrapping == False):
            self.scrapping = True
            self.startButton.setText("Stop scrap")
            self.output.append("############\nStarting scrap")
            self.main = proxyScrapper.scrapper(file, num, self.output, delay=self.delayspin.value()/100)
            self.main.scrapProxies(file)
            self.scrapping = False
            self.output.append("Done\n############")
            self.output.moveCursor(QtGui.QTextCursor.End)
            self.startButton.setText("Start scrap")
        else:
            self.output.append("stopping scrap....")
            self.output.moveCursor(QtGui.QTextCursor.End)
            self.main.stopScrap()
            self.startButton.setText("Start scrap")
            self.scrapping = False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = Input()
    try:
        sys.exit(dialog.exec_())
    except:
        pass
