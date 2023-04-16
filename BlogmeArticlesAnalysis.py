# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:29:09 2023

@author: pijan_000
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Open excel or xlsx file
data=pd.read_excel('C:\\Users\\pijan_000\\Downloads\\articles.xlsx')

#summary of the data
data.describe()

#summary the columns
data.info

#Counting the number of articles grouping per source
data.groupby(['source_id'])['article_id'].count()

#Number of reactions by publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#Dropping useless column
data = data.drop('engagement_comment_plugin_count' , axis=1)

# Creating keyword flag
keyword = 'crash'

#Creating function for finding keyword in an articles titles whitch in return creating a flag column
# Try is added to avoid an error when the entity is nan
def keywordflag(keyword):
    length=len(data)
    keyword_flag=[]
    for x in range(0,length):
        heading=data['title'][x]
        try:
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except: 
            flag=0
        keyword_flag.append(flag)
    return keyword_flag

keywordflag = keywordflag('murder')
data['keyword_flag']= pd.Series(keywordflag)

##SentimentIntensityAnalyzer using Vader
sent_int=SentimentIntensityAnalyzer()
text = data['title'][15]
sent = sent_int.polarity_scores(text)

#Extracting sentiment values

neg = sent['neg']
pos = sent['pos']
neu = sent['neu']

#Creating variables for sentiment values

title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

#populing sentiment data into set

length=len(data)

for x in range(0, length):
    try:
        text = data['title'][x]
        sent_int=SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)
    
#Changing type to a Series
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)

#Adding sentiment values to df data
data['title_neg_sentiment']=title_neg_sentiment
data['title_pos_sentiment']=title_pos_sentiment
data['title_neu_sentiment']=title_neu_sentiment

#saving table in excel file
data.to_excel('blogme_clean.xlsx', sheet_name = 'blogmedata', index=False)
       