# Data Entry GUI for more_features.json

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont
import json
import pandas as pd
import numpy as np
import sys
import re
from pprint import pprint as p
import inspect

NUM_WINDOWS = 9
NUM_TWEETS = 10000

class TweetDataEntryTool(QWidget):
        
        def __init__(self,parent=None):
                super().__init__(parent)
                
                self.this_font = QFont('cm', 16)
                self.this_list = []
                self.last_feature = ""
                self.last_references = []
                
                # Load labels
                with open("more_features.json") as f:
                    self.dict_features = json.load(f)
                self.this_tweet_num = int(self.dict_features["last_position"])
                
                # Load feature whitelist
                with open("feature_whitelist.json") as f:
                    self.feature_whitelist = list(json.load(f))
                
                # Load tweets
                with open('tweets_01-08-2021.json', encoding='utf-8') as f:
                    self.tweet_df = pd.read_json(f)
                
                # Drop before Trump ran for President
                is_president_or_running_for_president = self.tweet_df['date'] < '2015-06-16'
                self.tweet_df = self.tweet_df.loc[np.invert(is_president_or_running_for_president)]
                
                # Sort by RT descending
                self.tweet_df.sort_values(by=['retweets'], ascending=False, inplace=True, ignore_index=True)
                self.tweet_df.drop(index=range(NUM_TWEETS, len(self.tweet_df)), inplace=True)
                
                list_keys = list(self.dict_features.keys())
                for this_id in self.tweet_df["id"].values:
                    if str(this_id) not in list_keys:
                        self.dict_features[str(this_id)] = {"none": ""}
                    
                # Set window
                self.setWindowTitle("Trump Tweet Data Entry Tool")
                self.resize(1008, 756)
                
                # Create forward/back/save buttons
                self.btnPressFwd = QPushButton("Forward")
                self.btnPressFwd.setFont(self.this_font)
                self.btnPressBack = QPushButton("Back")
                self.btnPressBack.setFont(self.this_font)
                self.btnPressSave = QPushButton("Save")
                self.btnPressSave.setFont(self.this_font)
                self.btnPressFwd.clicked.connect(self.btnPressFwd_Clicked)
                self.btnPressBack.clicked.connect(self.btnPressBack_Clicked)
                self.btnPressSave.clicked.connect(self.btnPressSave_Clicked)
                
                # Add layouts
                self.layout_main = QHBoxLayout()
                self.layout_left = QVBoxLayout()
                self.layout_right = QVBoxLayout()
                self.layout_main.addLayout(self.layout_left)
                self.layout_main.addLayout(self.layout_right)
                
                # Add forward/back buttons
                self.layout_right.addWidget(self.btnPressFwd)
                self.layout_right.addWidget(self.btnPressBack)
                self.layout_right.addWidget(self.btnPressSave)
                
                # Select current tweet
                self.this_tweet = QTextEdit()
                self.this_tweet.setFixedSize(756, 250)
                self.this_tweet.setReadOnly(True)
                self.this_id = str(self.tweet_df.loc[[self.this_tweet_num], ["id"]].values[0, 0])
                self.this_tweet.setText(self.tweet_df.loc[[self.this_tweet_num], ["text"]].values[0, 0])
                self.this_tweet.setFont(self.this_font)
                self.layout_left.addWidget(self.this_tweet)
                
                # Add whitelist features 
                self.whitelist_features_title = QLabel()
                self.whitelist_features_title.setText("Whitelist Features: ")
                self.whitelist_features_title.setFont(self.this_font)
                self.whitelist_features_label = QTextEdit()
                self.whitelist_features_label.setText(", ".join(sorted(self.feature_whitelist)))
                self.whitelist_features_label.setFont(self.this_font)
                self.whitelist_features_label.setFixedSize(500, 500)
                self.whitelist_features_label.setReadOnly(True)
                self.layout_right.addWidget(self.whitelist_features_title)
                self.layout_right.addWidget(self.whitelist_features_label)
                
                # Add tweet number from top RT tweets (0 = highest RTs)
                self.tweet_num = QLabel()
                self.tweet_num.setText("\nTweet Number From Top By RT:")
                self.tweet_num.setFont(self.this_font)
                self.layout_right.addWidget(self.tweet_num)
                self.tweet_num_enter = QTextEdit()
                self.tweet_num_enter.setText(str(self.this_tweet_num))
                self.tweet_num_enter.setFont(self.this_font)
                self.layout_right.addWidget(self.tweet_num_enter)
                self.tweet_num_enter.textChanged.connect(self.txtTweetNum_Change)
                
                # Add tweet ID
                self.tweet_id = QLabel()
                self.tweet_id.setText("Tweet ID:")
                self.tweet_id.setFont(self.this_font)
                self.layout_right.addWidget(self.tweet_id)
                self.enter_id = QTextEdit()
                self.enter_id.setText(self.this_id)
                self.enter_id.setFont(self.this_font)
                self.layout_right.addWidget(self.enter_id)
                self.enter_id.textChanged.connect(self.txtTweetId_Change)

                # Load features into cells
                for i in range(NUM_WINDOWS):
                    exec("self.textEdit{i} = QTextEdit()".format(i=i))
                    exec("self.textEdit{i}.textChanged.connect(self.onFeatureChange)".format(i=i))
                    exec("self.textEdit{i}.cursorPositionChanged.connect(self.onCursorChange)".format(i=i))
                    exec("self.textEdit{i}.setObjectName('textEdit{i}')".format(i=i))
                    exec("self.textEdit{i}.setFont(self.this_font)".format(i=i))
                    exec("self.layout_left.addWidget(self.textEdit{i})".format(i=i))
                    exec("self.textEdit{i}.resize(100, 250)".format(i=i))
                self.populate_features()
                self.onCursorChange()
                self.setLayout(self.layout_main)
      
        # Reload features and references into the text edit boxes
        def populate_features(self):
            
            features_and_references = self.dict_features[self.this_id]
            list_keys = list(features_and_references.keys())
            
            for i in range(NUM_WINDOWS):
                if i < len(features_and_references):
                    set_text = "{feature}\n".format(feature=list_keys[i])
                    set_text += "{reference_str}".format(reference_str=features_and_references[list_keys[i]])
                    exec("self.textEdit{i}.setPlainText(set_text)".format(i=i))
                    
                else:
                    set_text = ""
                    exec("self.textEdit{i}.setPlainText(set_text)".format(i=i))
                    
            tweet_str = str(self.tweet_df.loc[[self.this_tweet_num], ["text"]].values[0, 0]) + " "
            tweet_str += str(self.tweet_df.loc[[self.this_tweet_num], ["date"]].values[0, 0])[0:10]
            self.this_tweet.setText(tweet_str)
            self.enter_id.setText(self.this_id)
            self.tweet_num_enter.setText(str(self.this_tweet_num))
            self.dict_features["last_position"] = str(self.this_tweet_num)
            
        # Set Tweet num
        def set_tweet_num(self, tweet_num):
            self.this_tweet_num = tweet_num
            self.this_id = str(self.tweet_df.loc[[self.this_tweet_num], ["id"]].values[0, 0])
            self.populate_features()
            
        # Set Tweet ID
        def set_tweet_id(self, tweet_id):
            self.this_id = tweet_id.replace("\n", "")
            self.this_tweet_num = self.tweet_df["id"].get_loc(self.this_tweet_id)
            self.populate_features()
        
        # Advance to next tweet by decreasing RT
        def btnPressFwd_Clicked(self):
            self.set_tweet_num(int(self.tweet_num_enter.toPlainText()) + 1)

        # Go back to previous tweet
        def btnPressBack_Clicked(self):
            self.set_tweet_num(int(self.tweet_num_enter.toPlainText()) - 1)   
        
        # Save current state
        def btnPressSave_Clicked(self):
            with open("more_features.json", 'w') as f:
                json.dump(self.dict_features, f)
            
        # Select tweet by tweet ID
        def txtTweetId_Change(self):
            if len(inspect.stack()) > 3:
                return
            
            if inspect.stack()[0][3] in ["txtTweetId_Change"]:
                self.set_tweet_id(self.enter_id.toPlainText())
                            
        # Select tweet by highest RT order
        def txtTweetNum_Change(self):
            if len(inspect.stack()) > 3:
                return
            
            if inspect.stack()[0][3] in ["txtTweetNum_Change"]:
                self.set_tweet_num(int(self.tweet_num_enter.toPlainText()))
        
        # Keep track of last feature
        def onCursorChange(self):
            if len(inspect.stack()) > 3:
                            return
            
            if self.focusWidget():
                object_name = self.focusWidget().objectName()
                if inspect.stack()[0][3] in ["onCursorChange"] and object_name:
                    exec("self.this_list = self.{obname}.toPlainText().split({char})".format(char="\n", obname=object_name))

                    if self.this_list:
                        this_feature = self.this_list[0]
                        if this_feature in self.feature_whitelist + ["none"]:
                            exec("self.{obname}.last_feature = this_feature".format(obname=object_name))
                            p("last feature = " + this_feature)
                                
        # Update self.dict_features once a change is made to the feature or reference URL
        # TODO: data_entry_gui_test.test_onFeatureChange(self)
        def onFeatureChange(self):
            p("onFeatureChange")
            if len(inspect.stack()) > 3:
                return
            p(inspect.stack())
            
            # Get calling widget name set during init
            object_name = self.focusWidget().objectName()
            
            # Check that the calling function is not some other internal gui function
            if inspect.stack()[0][3] in ["onFeatureChange"] and object_name:
                
                # Get list of single feature and references
                exec("self.this_list = self.{obname}.toPlainText().split({char})".format(
                    char="\n", 
                    maxsplit=1, 
                    obname=object_name)
                    )
                
                p(self.last_feature)
                # Check if anything is entered
                if self.this_list:
                    
                    p(self.this_list)
                    # First item is the feature
                    this_feature = self.this_list.pop(0)
                    
                    # Check if feature is valid
                    if this_feature in self.feature_whitelist or this_feature == "none":
                        
                        p("passed whitelist: " + this_feature)
                        # Check if feature is already in the dict for this tweet ID
                        # If not, create an empty list of references
                        if (this_feature not in list(self.dict_features[self.this_id].keys())):
                            self.dict_features[self.this_id][this_feature] = ""
                            
                        # The feature already exists dict for this tweet. Remove "none" if len > 1.
                        # This indicates that the tweet has been reviewed.
                        current_features = list(self.dict_features[self.this_id].keys())
                        if "none" in current_features and len(self.dict_features[self.this_id]) > 1:
                            exec("del self.dict_features[self.this_id]['none']".format(obname=object_name))
                            p("deleted none from dict_features")

                        # If references are entered, input them into dict_features
                        if self.this_list:
                            self.dict_features[self.this_id][this_feature] = self.this_list.pop(0)
                            p(self.dict_features[self.this_id][this_feature])
                            p(this_feature)
                            p("onFeatureChange: references updated in dict_features")
                            
                        if this_feature:
                            exec("self.{obname}.last_feature = this_feature".format(obname=object_name))

                # Delete the feature from the file if it is erased in the gui                
                else:
                    try:
                        p("deleting from dict features")
                        exec("del self.dict_features[self.this_id][self.{obname}.last_feature]".format(obname=object_name))
                        p(self.dict_features[self.this_id])
                        
                    except Exception as e:
                        p(e)
                        p("dict_features_not_updated")
            
           
                              
if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TweetDataEntryTool()
        win.show()
        sys.exit(app.exec_())