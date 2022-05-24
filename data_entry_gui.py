from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
import json
from bs4 import BeautifulSoup
import sys
from pprint import pprint as p

class TweetDataEntryTool(QWidget):
        
        def __init__(self,parent=None):
                super().__init__(parent)
                
                # Load labels
                with open("more_features.json") as f:
                    self.dict_features = json.load(f)
                
                # Load feature whitelist
                with open("feature_whitelist.json") as f:
                    self.feature_whitelist = list(json.load(f))
                
                # Load tweets
                with open("high_rt_tweets.json") as f:
                    self.tweets = json.load(f)
                
                # Set window
                self.setWindowTitle("Trump Tweet Data Entry Tool")
                self.resize(1344, 756)
                
                # Add buttons
                self.btnPress1 = QPushButton("Forward")
                self.btnPress2 = QPushButton("Back")
                self.btnPress3 = QPushButton("Exit")

                self.btnPress1.clicked.connect(self.btnPress1_Clicked)
                self.btnPress2.clicked.connect(self.btnPress2_Clicked)
                
                # Add layouts
                layout_main = QHBoxLayout()
                layout_left = QVBoxLayout()
                layout_right = QVBoxLayout()
                layout_main.addLayout(layout_left)
                layout_main.addLayout(layout_right)
                    
                # Add elements
                layout_right.addWidget(self.btnPress1)
                layout_right.addWidget(self.btnPress2)
                layout_right.addWidget(self.btnPress3)
                layout_right.addWidget(QTextEdit())
                layout_right.addWidget(QTextEdit())
                
                # Select current tweet
                self.this_tweet = QLabel()
                self.this_tweet.setText(self.tweets["0"])
                layout_left.addWidget(self.this_tweet)
                
                # Add feature entry windows
                for i in range(10):
                    exec("self.textEdit{i} = QTextEdit()".format(i=i))
                    exec("layout_left.addWidget(self.textEdit{i})".format(i=i))
                    p(exec("list(self.dict_features.keys())[{i}]".format(i=i)))
                    if i < len(self.dict_features.keys()):
                        exec("self.textEdit{i}.setText(self.dict_features[list(self.dict_features.keys())[{i}]][0])".format(i=i))
                
                self.setLayout(layout_main)


        def btnPress1_Clicked(self):
                self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

        def btnPress2_Clicked(self):
                self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TweetDataEntryTool()
        win.show()
        sys.exit(app.exec_())