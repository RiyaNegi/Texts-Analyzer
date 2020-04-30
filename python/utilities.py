import re

mediaPattern = r"(\<Media omitted\>)" 
regexMedia = re.compile(mediaPattern, flags=re.M)

dateAndTimepattern = r"(\d+\/\d+\/\d+)(,)(\s)(\d+:\d+)(\s)(\w+)(\s)(-)(\s\w+)*(:)"
regexDate = re.compile(dateAndTimepattern, flags=re.M)

def cleanText(a_file):    
    chat = open(a_file)
    chatText = chat.read()
    chat.close()

    chatText = regexMedia.sub("", chatText)
    chatText = regexDate.sub("", chatText)

    lines = []

    for line in chatText.splitlines():
        if line.strip() is not "": 
            lines.append(line.strip())

    return lines