import re
import sys
import plotly.graph_objects as go

def split_text(a_file):
    """
    Split file contents by newline.
    """
    chat = open(a_file, 'r', encoding='utf-8')
    chatText = chat.read()
    return chatText.splitlines()

def groupByHour(AM, PM):
    time_groups = {}

    for i in range(24):
        time_groups[str(i)] = 0 

    for time in AM:
        current_hour = int(time.split(":")[0])

        if current_hour == 12:
            current_hour = 0 

        current_hour = str(current_hour)
        time_groups[current_hour] += 1

    for time in PM:
        # print(time)
        current_hour = int(time.split(":")[0])

        if current_hour > 12:
            continue 

        current_hour += 12

        if current_hour == 24:
            current_hour = 12

        current_hour = str(current_hour)
        time_groups[current_hour] += 1

    return time_groups

def distributeByAmPm(linesText, timeRegex):
    AM, PM = [], []
    matches = []
    for index, line in enumerate(linesText):
        matches = re.findall(timeRegex,line)
        if(len(matches) > 0):
            match = matches[0] 

            if "AM" in match:
                AM.append(match[0])
            else:
                PM.append(match[0])
    # print(len(AM+PM))
    return AM, PM

def plot_graph(time_groups, name):
    listk = [] 
    for key in time_groups.keys(): 
        listk.append(key) 
    listv = [] 
    for key in time_groups.values(): 
        listv.append(key) 
    data = [go.Scatter(
    x=listk,
    y=listv,
    mode='lines+markers',
    name=f'{name}',
    ) ]
    layout=go.Layout(title=f'{name}',xaxis=dict(
        title='HOURS',
        tickmode='linear'),yaxis=dict(title='NUMBER OF CHATS'))
    fig=go.Figure(data=data, layout=layout)
    fig.show()
def analyze(name):
    linesText = split_text(name)
    timeRegex = re.compile(r"(\d+(:)\d+)(\s)(\w+)")

    # Distribute into AM and PM
    AM, PM = distributeByAmPm(linesText, timeRegex)

    # Now group time into 1-hour intervals
    time_groups = groupByHour(AM, PM)
    print(name, time_groups)
    # plot_graph(time_groups, name)


import os
PATH = "./chats"
chat_files = os.listdir(PATH)

print("Here are your chats:")
for i,a_file in enumerate(chat_files):
    choice = i
    analyze(PATH+'/'+chat_files[choice])
    print(f"{i+1}. {a_file}")

# choice = int(input("Select one: ")) - 1

# analyze(PATH+'/'+chat_files[choice])