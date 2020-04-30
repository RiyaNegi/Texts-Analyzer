import re
import sys
import time
import plotly.graph_objects as go


def split_text(a_file):
    """
    Split file contents by newline.
    """
    chat = open(a_file, 'r', encoding='utf-8')
    chatText = chat.read()
    return chatText.splitlines()


def get_total(linesText, timeRegex):
    total= []
    for index,line in enumerate(linesText):
        matches = re.findall(timeRegex, line)
        if(len(matches) > 0):
            match = matches[0] 
            total.append(match[0])
    return len(total)

def analyze(name):
    linesText = split_text(name)
    timeRegex = re.compile(r"(\d+(:)\d+)(\s)(\w+)")
    message_count = get_total(linesText, timeRegex)
    return message_count
    print(name,message_count)
    

import os
PATH = "./chats"

chat_files = os.listdir(PATH)
chat_counts = []

for a_file in chat_files:
    current_count = analyze(PATH+'/'+a_file)
    chat_counts.append(current_count)

chat_count_list = list(zip(chat_files, chat_counts))

TOP_COUNT = 5

def sorter_function(x):
    return -x[1]

chat_count_list.sort(key=sorter_function)

top_chats = chat_count_list[:TOP_COUNT]

counts = []
names = []

for x in top_chats:
    counts.append(x[1])
    names.append(x[0])

data = [go.Bar(
    x=names,
    y=counts,
    name='TOP 5 CHATS'
) ]
layout=go.Layout(title='TOP 5 CHATS')
fig=go.Figure(data=data, layout=layout)
fig.show()