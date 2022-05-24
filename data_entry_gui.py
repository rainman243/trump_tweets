from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout
import json
from bs4 import BeautifulSoup
import sys
from pprint import pprint as p

class TweetDataEntryTool(QWidget):
        def __init__(self,parent=None):
                super().__init__(parent)

                with open("more_features.json") as f:
                    self.dict_features = json.load(f)
                    
                self.setWindowTitle("Trump Tweet Data Entry Tool")
                self.resize(1344, 756)
                
                self.btnPress1 = QPushButton("Forward")
                self.btnPress2 = QPushButton("Back")
                self.btnPress1.clicked.connect(self.btnPress1_Clicked)
                self.btnPress2.clicked.connect(self.btnPress2_Clicked)
                
                layout = QVBoxLayout()
                layout.addWidget(self.btnPress1)
                layout.addWidget(self.btnPress2)
                self.setLayout(layout)
                
                for i in range(20):
                    exec("self.textEdit{i} = QTextEdit()".format(i=i))
                    exec("layout.addWidget(self.textEdit{i})".format(i=i))

        def btnPress1_Clicked(self):
                self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

        def btnPress2_Clicked(self):
                self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TweetDataEntryTool()
        win.show()
        sys.exit(app.exec_())