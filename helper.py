# Helper functions used when gui and notebook should be synchronized. 

import pandas as pd
import numpy as np

NUM_TWEETS = 10000

# Load tweets and discard all before he ran for president first time. Out of those, sort by RT and take the top NUM_TWEETS.
def load_and_clean_tweets(tweet_filename):
    
    # Load tweets
    with open(tweet_filename, encoding='utf-8') as f:
        tweet_df = pd.read_json(f)

    # Drop before Trump ran for President
    is_president_or_running_for_president = tweet_df['date'] < '2015-06-16'    
    tweet_df = tweet_df.loc[np.invert(is_president_or_running_for_president)]

    # Sort by RT descending 
    tweet_df.sort_values(by=['retweets'], ascending=False, inplace=True, ignore_index=True)
    
    # Take the top NUM_TWEETS tweets
    tweet_df = tweet_df.iloc[range(0, NUM_TWEETS)]
                
    return tweet_df