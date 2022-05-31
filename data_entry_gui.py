# Data Entry GUI for more_features.json

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont
import json
from bs4 import BeautifulSoup
import sys
import re
from pprint import pprint as p
import inspect

NUM_WINDOWS = 9

class TweetDataEntryTool(QWidget):
        
        def __init__(self,parent=None):
                super().__init__(parent)
                
                self.this_font = QFont('cm', 16)
                
                # Load labels
                with open("more_features.json") as f:
                    self.dict_features = json.load(f)
                self.this_tweet_num = self.dict_features.pop("last_position")
                
                # Load feature whitelist
                with open("feature_whitelist.json") as f:
                    self.feature_whitelist = list(json.load(f))
                
                # Load tweets
                with open("high_rt_tweets.json") as f:
                    self.tweets = json.load(f)
                
                # Setup reverse lookup for tweets
                split_id_tweet = [re.split(":", self.tweets[str(i)], maxsplit=2) for i in range(len(self.tweets))]
                self.tweet_id_lookup = {split_id_tweet[i][0]: str(i) for i in range(len(self.tweets))}
                
                # Set window
                self.setWindowTitle("Trump Tweet Data Entry Tool")
                self.resize(1008, 756)
                
                # Create forward/back buttons
                self.btnPressFwd = QPushButton("Forward")
                self.btnPressFwd.setFont(self.this_font)
                self.btnPressBack = QPushButton("Back")
                self.btnPressBack.setFont(self.this_font)
                self.btnPressFwd.clicked.connect(self.btnPressFwd_Clicked)
                self.btnPressBack.clicked.connect(self.btnPressBack_Clicked)
                
                # Add layouts
                self.layout_main = QHBoxLayout()
                self.layout_left = QVBoxLayout()
                self.layout_right = QVBoxLayout()
                self.layout_main.addLayout(self.layout_left)
                self.layout_main.addLayout(self.layout_right)
                
                # Add forward/back buttons
                self.layout_right.addWidget(self.btnPressFwd)
                self.layout_right.addWidget(self.btnPressBack)
                
                # Select current tweet
                self.this_tweet = QLabel()
                self.this_tweet.setFixedSize(756, 250) 
                split_id_tweet = re.split(":", self.tweets[str(self.this_tweet_num)], maxsplit=1)
                self.this_id = split_id_tweet[0]
                self.this_tweet.setText(split_id_tweet[1])
                self.this_tweet.setFont(self.this_font)
                self.this_tweet.setWordWrap(True)
                self.layout_left.addWidget(self.this_tweet)
                
                # Add whitelist features 
                self.whitelist_features_label = QTextEdit()
                self.whitelist_features_label.setText("Whitelist Features: " + ", ".join(self.feature_whitelist))
                self.whitelist_features_label.setFont(self.this_font)
                self.whitelist_features_label.setFixedSize(500, 700)
                self.layout_right.addWidget(self.whitelist_features_label)
                
                #tAdd tweet number from top RT tweets (0 = highest RTs)
                self.tweet_num = QLabel()
                self.tweet_num.setText("\nTweet Number From Top By RT:")
                self.tweet_num.setFont(self.this_font)
                self.layout_right.addWidget(self.tweet_num)
                self.tweet_num_enter = QTextEdit()
                self.tweet_num_enter.setText(str(self.this_tweet_num))
                self.layout_right.addWidget(self.tweet_num_enter)
                self.tweet_num_enter.textChanged.connect(self.txtTweetNum_Change)
                
                # Add tweet ID
                self.tweet_id = QLabel()
                self.tweet_id.setText("Tweet ID:")
                self.tweet_id.setFont(self.this_font)
                self.layout_right.addWidget(self.tweet_id)
                self.enter_id = QTextEdit()
                self.enter_id.setText(self.this_id)
                self.layout_right.addWidget(self.enter_id)
                self.enter_id.textChanged.connect(self.txtTweetId_Change)

                # Load features into cells
                for i in range(NUM_WINDOWS):
                    exec("self.textEdit{i} = QTextEdit()".format(i=i))
                    exec("self.layout_left.addWidget(self.textEdit{i})".format(i=i))
                    exec("self.textEdit{i}.resize(100, 250)".format(i=i))
                self.populate_features()
                
                self.setLayout(self.layout_main)
      
        # Reload features and references into the text edit boxes
        def populate_features(self):
            
            features_and_references = self.dict_features[self.this_id] 
            list_keys = list(features_and_references.keys())
            
            for i in range(NUM_WINDOWS):
                if i < len(features_and_references):
                    this_reference_list = features_and_references[list_keys[i]]
                    reference_list_str = ", ".join(this_reference_list)
                    set_text = "{feature}\n".format(feature=list_keys[i])
                    set_text += "{reference_list}".format(reference_list=reference_list_str)
                    exec("self.textEdit{i}.setPlainText(set_text)".format(i=i))
                else:
                    set_text = ""
                    exec("self.textEdit{i}.setPlainText(set_text)".format(i=i))
                    
            split_id_tweet = re.split(":", self.tweets[self.tweet_id_lookup[self.this_id]], maxsplit=1)
            self.this_tweet.setText(split_id_tweet[1])
            self.enter_id.setText(self.this_id)
            self.tweet_num_enter.setText(self.tweet_id_lookup[self.this_id])

            
        # Set Tweet num
        def set_tweet_num(self, tweet_num):
            self.this_tweet_num = tweet_num
            self.this_id = re.split(":", self.tweets[str(self.this_tweet_num)], maxsplit=1)[0]
            self.populate_features()

            
        # Set Tweet ID
        def set_tweet_id(self, tweet_id):
            self.this_id = tweet_id.replace("\n", "")
            self.this_tweet_num = int(self.tweet_id_lookup[self.this_id])
            self.populate_features()
        
        # Advance to next tweet by decreasing RT
        def btnPressFwd_Clicked(self):
                self.set_tweet_num(int(self.tweet_num_enter.toPlainText()) + 1)

        # Go back to previous tweet
        def btnPressBack_Clicked(self):
                self.set_tweet_num(int(self.tweet_num_enter.toPlainText()) - 1)   
                
        # Select tweet by tweet ID
        def txtTweetId_Change(self):
            if len(inspect.stack()) > 3:
                return
            
            if inspect.stack()[0][3] in ["txtTweetId_Change"]:
                self.set_tweet_id(self.enter_id.toPlainText())
                            
        # Select tweet by RT order
        def txtTweetNum_Change(self):
            if len(inspect.stack()) > 3:
                return
            
            if inspect.stack()[0][3] in ["txtTweetNum_Change"]:
                self.set_tweet_num(int(self.tweet_num_enter.toPlainText()))
                        
        # Update self.dict_features and save the file once a change is made to the feature or reference URL
        def onFeatureChange(self):
            pass

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TweetDataEntryTool()
        win.show()
        sys.exit(app.exec_())