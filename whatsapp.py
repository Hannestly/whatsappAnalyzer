import re
from collections import Counter
import os
import datetime


class messageUnit():
    def __init__(self, message, avoid_list):
        self.date = None        # date sent
        self.time = None        # time sent
        self.sender = None      # sender
        self.content = None     # message raw content
        self.wordlist = []      # cleaned list of words from raw content
        self.hour = None
        self.avoid_list = avoid_list

        # Unused Regex compilers
        # re_year = re.compile(r'^(\d{4})-')
        # re_month = re.compile(r'^\d{4}-(\d+)-')
        # re_day = re.compile(r'^\d{4}-\d+-(\d+)')
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
        re_date = re.compile(r'(\d{4}-\d+-\d+).*')
        self.date = re_date.match(message)[1]

    def setTime(self, message):
        re_time = re.compile(r'\d{4}-\d+-\d+, (\d+:\d+)')
        self.time = re_time.match(message)[1]

    def setSender(self, message):
        re_sender = re.compile(r'\d+-\d+-\d+, \d+:\d+ - (.*?):')
        self.sender = re_sender.match(message)[1]

    def setHour(self, message):
        re_hour = re.compile(r'^\d+-\d+-\d+, (\d+):')
        self.hour = re_hour.match(message)[1]

    def setContent(self, message):
        re_content = re.compile(r'\d{4}-\d+-\d+, \d+:\d+ - \D+: (.*)')
        re_text = re.compile(r'([a-z\'<>]*)')
        self.content = re_content.match(message)[1]
        tempwordlist = self.content.split(" ")
        tempwordlist = [x.lower() for x in tempwordlist]
        tempwordlist = [x.strip() for x in tempwordlist]
        tempwordlist = [re_text.match(x)[1] for x in tempwordlist]
        tempwordlist = [x for x in tempwordlist if x not in self.avoid_list]
        self.wordlist = [x for x in tempwordlist if x is not '']


class ChatBank():
    def __init__(self, chatname, avoid_file=None):
        self.chatname = chatname    # name of the chat

        self.message_index = 0
        self.chatdata = self.read_chatfile(chatname)    # chat data in string
        self.avoid_list = []        # list of words to be avoided
        if avoid_file is not None:
            self.avoid_list = self.parse_avoid_file(avoid_file)
        self.usedwords = Counter()  # used words with counter
        self.users = Counter()      # Chat users with counter
        self.firstday = ""          # first day of the chat
        self.chathours = Counter()  # chatting hours with counter
        self.userwords = {}
        self.iterate_messages(self.chatdata)

    def read_chatfile(self, chatname):
        with open(chatname, encoding="utf8") as textfile:
            data = textfile.read()
            return data

    def parse_avoid_file(self, avoid_file):
        with open(avoid_file, 'r') as avoidfile:
            filedata = avoidfile.read()
            avoid_words = re.split(r',|\s|\n|;', filedata)
            avoid_words = list(map(lambda x: x.strip(), avoid_words))
            avoid_words = [word for word in avoid_words if word != '']
            return avoid_words

    def iterate_messages(self, chatdata):
        chatmessages = chatdata.split('\n')
        for message in chatmessages:
            msg = messageUnit(message, self.avoid_list)
            if self.message_index == 0:
                self.set_firstdate(msg)
            self.add_tobank(msg)
            self.message_index += 1

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
