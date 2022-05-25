# Data Entry GUI for more_feature.json

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont
import json
from bs4 import BeautifulSoup
import sys
import re
from pprint import pprint as p

class TweetDataEntryTool(QWidget):
        
        def __init__(self,parent=None):
                super().__init__(parent)
                
                this_font = QFont('cm', 16)
                
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
                self.resize(1008, 756)
                
                # Add buttons
                self.btnPressFwd = QPushButton("Forward")
                self.btnPressFwd.setFont(this_font)
                self.btnPressBack = QPushButton("Back")
                self.btnPressBack.setFont(this_font)
                self.btnPressExit = QPushButton("Exit")
                self.btnPressExit.setFont(this_font)

                self.btnPressFwd.clicked.connect(self.btnPressFwd_Clicked)
                self.btnPressBack.clicked.connect(self.btnPressBack_Clicked)
                self.btnPressExit.clicked.connect(self.btnPressExit_Clicked)
                
                # Add layouts
                layout_main = QHBoxLayout()
                layout_left = QVBoxLayout()
                layout_right = QVBoxLayout()
                layout_main.addLayout(layout_left)
                layout_main.addLayout(layout_right)
                
                # Add elements
                layout_right.addWidget(self.btnPressFwd)
                layout_right.addWidget(self.btnPressBack)
                layout_right.addWidget(self.btnPressExit)
                
                # Select current tweet
                self.this_tweet = QLabel()
                self.this_tweet.setFixedSize(756, 250) 
                split_id_tweet = re.split(":", self.tweets["0"], maxsplit=1)
                self.this_id = split_id_tweet[0]
                self.this_tweet.setText(split_id_tweet[1])
                self.this_tweet.setFont(this_font)
                self.this_tweet.setWordWrap(True)
                layout_left.addWidget(self.this_tweet)
                self.this_key = list(self.dict_features.keys())[0]
                
                # Add tweet number from top RT tweets (0 = highest RTs)
                self.tweet_num = QLabel()
                self.tweet_num.setText("Tweet number from top:")
                self.tweet_num.setFont(this_font)
                layout_right.addWidget(self.tweet_num)
                self.tweet_num_enter = QTextEdit()
                self.tweet_num_enter.setText("0")
                layout_right.addWidget(self.tweet_num_enter)
                
                # Add tweet ID
                self.tweet_id = QLabel()
                self.tweet_id.setText("Tweet ID:")
                self.tweet_id.setFont(this_font)
                layout_right.addWidget(self.tweet_id)
                self.enter_id = QTextEdit()
                self.enter_id.setText(self.this_id)
                layout_right.addWidget(self.enter_id)
                
                # Add feature entry windows
                for i in range(9):
                    exec("self.textEdit{i} = QTextEdit()".format(i=i))
                    exec("layout_left.addWidget(self.textEdit{i})".format(i=i))
                    exec("self.textEdit{i}.resize(100, 250)".format(i=i))
                    
                    if i < len(self.dict_features[self.this_key]):
                        exec("self.textEdit{i}.setText(self.dict_features[self.this_key][{i}])".format(i=i))
                        
                self.setLayout(layout_main)

        # Advance to next tweet by decreasing RT.
        def btnPressFwd_Clicked(self):
                self.this_tweet_num++
                self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

        # Go back to previous tweet.
        def btnPressBack_Clicked(self):
                self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")
        
        # Save and exit.
        def btnPressExit_Clicked(self):
                self.textEdit.setHtml("!")
        
        # Select tweet by tweet ID.
        def txtTweetId_Change(self):
            self.tweet_id
        
        # Select tweet by RT order
        def txtTweetNum_Change(self):
            self.tweet_num
        
        # Save the file once a change is made to the feature or reference URL.
        def saveAll(self):
            with open("more_features.json", 'rw') as f:
                json.dump(self.dict_features)


if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TweetDataEntryTool()
        win.show()
        sys.exit(app.exec_())