import re
from collections import Counter
import os
import datetime

# Regex complile list
re_date = re.compile(r'(\d{4}-\d+-\d+).*')
re_time = re.compile(r'\d{4}-\d+-\d+, (\d+:\d+)')
re_hour = re.compile(r'\d{4}-\d+-\d+, (\d+):\d+')
re_sender = re.compile(r'\d+-\d+-\d+, \d+:\d+ - (.*?):')
re_content = re.compile(r'\d{4}-\d+-\d+, \d+:\d+ - \D+: (.*)')
re_year = re.compile(r'^(\d{4})-')
re_month = re.compile(r'^\d{4}-(\d+)-')
re_day = re.compile(r'^\d{4}-\d+-(\d+)')


def readfile(filename):
    """returns textfile in strings"""
    with open(filename, encoding="utf8") as textfile:
        data = textfile.read()
        return data


def parse_avoid_file(filename):
    with open(filename, 'r') as avoidfile:
        filedata = avoidfile.read()
        avoid_words = re.split(r',|\s|\n|;', filedata)
        avoid_words = list(map(lambda x: x.strip(), avoid_words))
        avoid_words = [word for word in avoid_words if word != '']
        return avoid_words


class messageUnit():
    def __init__(self, message):
        self.date = None
        self.time = None
        self.sender = None
        self.content = None
        self.wordlist = []
        self.rawcontent = ""

        self.initmsg(message)

    def initmsg(self, message):
        try:
            self.setDate(message)
            self.setTime(message)
            self.setSender(message)
            self.setContent(message)
        except:
            pass

    def getContent(self, message):
        self.content = re_content.match(message)[1]
        tempcontent = self.content.lower()
        tempwordslist = tempcontent.split(" ")
        self.wordslist = [x.strip() for x in tempwordslist]

    def setDate(self, message):
        self.date = re_date.match(message)[1]

    def setTime(self, message):
        self.time = re_time.match(message)[1]

    def setSender(self, message):
        self.sender = re_sender.match(message)[1]

    def setContent(self, message):
        re_text = re.compile(r'([a-z\'<>]*)')
        content = re_content.match(message)[1]
        self.rawcontent = content
        tempwordlist = content.split(" ")
        tempwordlist = [x.lower() for x in tempwordlist]
        tempwordlist = [x.strip() for x in tempwordlist]
        tempwordlist = [re_text.match(x)[1] for x in tempwordlist]
        self.wordlist = [x for x in tempwordlist if x not in avoid_words]


class chatBank():
    def __init__(self, chatname):
        self.chatname = chatname


avoid_words = parse_avoid_file(r'avoid_list.txt')
data = readfile(r'messages.txt')
chat = data.split('\n')
# print(avoid_words)

for messages in chat:
    message = messageUnit(messages)
    # print(message.date)
    # print(message.time)
    print(message.wordlist)
