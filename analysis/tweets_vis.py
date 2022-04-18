# this projects takes amount of tweets based on your query
# then, data is stored to the TXT file 
# then, the file is opened and parsed
# finally, a nice diagram is plotted

# it's a quite stupid code but made for Windows with a lot of newbie's pain :'(
# some data engineering moments are not optimal, they were taken as a challenge ;P
# for further work it's better to split this code into several files or functions to call

import tweepy
import json

#import numpy
import pandas as pd
import ast
#import seaborn as sb
import matplotlib as mpl
import matplotlib.pyplot as plt

credfile = open('experiments\credentials.json')
 
# returns JSON object as
# a dictionary
cred = json.load(credfile)

####input your credentials here
#consumer_key = cred["API_key"]
#consumer_secret = cred["API_key_secret"]
#access_token = cred["access_token"]
#access_token_secret = cred["access_token_secret"]
bearer_token = cred["bearer_token"]

client = tweepy.Client(bearer_token=bearer_token)

query = 'covid -is:retweet place_country:It'
start_time = '2022-02-01T00:00:00Z'
end_time = '2022-04-01T00:00:00Z'

#csvFile = open(r'experiments\counts.txt', 'a', newline='')

#variant with dict in rows
counts = client.get_all_tweets_count(query=query, granularity='day')
with open(r'experiments\counts.txt', 'w') as f:
    for count in counts.data:
        f.write(str(count))
        f.write('\n')
    f.close()

# now we have to process all the data
with open(r'experiments\counts.txt', 'r') as f:
    raw_data = f.readlines()

# loop through rows, each row - object of DICT type that originally comes as a string
i = 0
for row in raw_data:
    s = ast.literal_eval(row) # sets dict type to a string
    df_row = pd.DataFrame.from_dict(s, orient = 'index', columns = [s.keys]).T # transposed
    if i > 0:
        df = pd.concat([df,df_row],ignore_index=True) # ignore index as by default all rows come with repeating indices
    else:
        df = df_row
    i += 1

# finally we have a dataframe but still need to change data types for further viz
df.astype({"tweet_count": int})
df['start'] = pd.to_datetime(df['start'], format='%Y-%m-%d').dt.date

# 1. Basic vizzes
#df.plot(x ='start', y='tweet_count', kind = 'bar')

#sb.barplot(x = df['start'], y = df['tweet_count'])
#plt.show()

# 2. Advanced viz 
"""df['colors'] = ['coral' if i < df['tweet_count'].mean() else 'lightgreen' for i in df['tweet_count']]
plt.figure(figsize=(12, 8), dpi=80)
plt.bar(x = df.start, height = df.tweet_count, color = df.colors)
plt.title('Tweets count by day')
plt.gca().set(ylabel = 'tweets', xlabel = 'date')
plt.grid(linestyle = '--', alpha = 0.5)
plt.show()"""

# 3. Stylish viz B-)
#cmap = mpl.cm.cool
#norm = mpl.colors.Normalize(vmin=df['tweet_count'].min(), vmax=df['tweet_count'].max())
with plt.style.context('Solarize_Light2'):
    #plt.plot(df['start'], df['tweet_count'])
    plt.figure(figsize=(14, 10), dpi=80)
    plt.bar(x = df['start'], height = df['tweet_count'])
    #plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), orientation='vertical')
    plt.title('Tweet count by day')
    plt.grid(linestyle = '--', alpha = 0.75)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Tweets', fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

plt.show()