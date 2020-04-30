import sys
import re
import plotly.graph_objects as go
import nltk
from utilities import cleanText 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze(name):
    linesList = cleanText(name)
    neutral, negative, positive = 0, 0, 0

    for index,sentence in enumerate(linesList):
        if re.match(r'^[\w]', sentence) is None:
            continue
        scores = sentiment_analyzer.polarity_scores(sentence)
        scores.pop('compound', None)

        maxAttribute = max(scores, key=lambda k: scores[k])

        if maxAttribute == "neu":
            neutral += 1
        elif maxAttribute == "neg":
            negative += 1
        else:
            positive += 1

    total = neutral + negative + positive
    print("Negative: {0}% | Neutral: {1}% | Positive: {2}%".format(
        negative*100/total, neutral*100/total, positive*100/total))

    # labels = 'Neutral', 'Negative', 'Positive'
    # sizes = [neutral, negative, positive]
    # fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3, marker={'colors':['rgb(11, 133, 200)','rgb(215, 11, 11)','rgb(0, 204, 0)']})])
    # fig.update(layout_title_text=f'{name}')
    # fig.show()

import os
PATH = "./chats"
chat_files = os.listdir(PATH)

print("Here are your chats:")
for i,a_file in enumerate(chat_files):
    print(f"{i+1}. {a_file}")
    choice = i
    analyze(PATH+'/'+chat_files[choice])





