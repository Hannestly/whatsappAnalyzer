import re
from collections import Counter
import os
import datetime

# Regex complile list
re_date = re.compile(r'(\d{4}-\d+-\d+).*')
re_time = re.compile(r'\d{4}-\d+-\d+, (\d+:\d+)')
re_hour = re.compile(r'^\d+-\d+-\d+, (\d+):')
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
        self.date = None        # date sent
        self.time = None        # time sent
        self.sender = None      # sender
        self.content = None     # message raw content
        self.wordlist = []      # cleaned list of words from raw content
        self.hour = None

        self.initmsg(message)

    def initmsg(self, message):
        try:
            self.setDate(message)
            self.setTime(message)
            self.setSender(message)
            self.setContent(message)
            self.setHour(message)
        except:
            pass

    def setDate(self, message):
        self.date = re_date.match(message)[1]

    def setTime(self, message):
        self.time = re_time.match(message)[1]

    def setSender(self, message):
        self.sender = re_sender.match(message)[1]

    def setHour(self, message):
        self.hour = re_hour.match(message)[1]

    def setContent(self, message):
        re_text = re.compile(r'([a-z\'<>]*)')
        self.content = re_content.match(message)[1]
        tempwordlist = self.content.split(" ")
        tempwordlist = [x.lower() for x in tempwordlist]
        tempwordlist = [x.strip() for x in tempwordlist]
        tempwordlist = [re_text.match(x)[1] for x in tempwordlist]
        tempwordlist = [x for x in tempwordlist if x not in avoid_words]
        self.wordlist = [x for x in tempwordlist if x is not '']


class ChatBank():
    def __init__(self, chatname):
        self.chatname = chatname    # name of the chat
        self.usedwords = Counter()  # used words with counter
        self.users = Counter()      # Chat users with counter
        self.firstday = ""          # first day of the chat
        self.chathours = Counter()  # chatting hours with counter
        self.userwords = {}

    def add_tobank(self, message):
        if message.wordlist is not "":
            self.usedwords.update(message.wordlist)
        self.users.update({message.sender: 1})
        self.add_chathours(message)
        self.add_userwords(message)

    def add_userwords(self, message):
        if message.sender not in self.userwords:
            self.userwords[message.sender] = Counter()
        if message.wordlist is not '':
            self.userwords[message.sender].update(message.wordlist)

    def add_chathours(self, message):
        if message.hour is not None:
            hoursent = int(message.hour)
            if hoursent <= 4:
                self.chathours.update({'Night': 1})
            elif hoursent > 4 and hoursent <= 7:
                self.chathours.update({'Dawn': 1})
            elif hoursent > 7 and hoursent <= 12:
                self.chathours.update({'Morning': 1})
            elif hoursent > 12 and hoursent <= 15:
                self.chathours.update({'Early Afternoon': 1})
            elif hoursent > 15 and hoursent <= 17:
                self.chathours.update({'Late Afternoon': 1})
            elif hoursent > 17 and hoursent <= 20:
                self.chathours.update({'Early Evening': 1})
            elif hoursent > 20 and hoursent <= 22:
                self.chathours.update({'Late Evening': 1})
            elif hoursent > 22 and hoursent <= 24:
                self.chathours.update({'Night': 1})

    def set_firstdate(self, message):
        self.firstday = message.date


avoid_words = parse_avoid_file(r'avoid_list.txt')
data = readfile(r'messages.txt')
chat = data.split('\n')

ChatBank = ChatBank("placeholder")     # Edit the name of the chat
msgindex = 0
for messages in chat:
    message = messageUnit(messages)
    if msgindex == 0:                   # first entry recorded as first day
        ChatBank.set_firstdate(message)
    ChatBank.add_tobank(message)
    msgindex += 1
