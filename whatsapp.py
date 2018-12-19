import re
from collections import Counter
import os
import datetime


def readfile(filename):
    with open(filename, encoding="utf8") as textfile:
        data = textfile.read()
        return data


re_date = re.compile(r'(\d{4}-\d+-\d+).*')
re_time = re.compile(r'\d{4}-\d+-\d+, (\d+:\d+)')
re_hour = re.compile(r'\d{4}-\d+-\d+, (\d+):\d+')
re_sender = re.compile(r'\d+-\d+-\d+, \d+:\d+ - (.*?):')
re_content = re.compile(r'\d{4}-\d+-\d+, \d+:\d+ - \D+: (.*)')


class messageBank():
    def __init__(self, message):
        self.date = None
        self.time = None
        self.sender = None
        self.content = None
        self.wordslist = []

        processlist = {"getDate": self.getDate,
                       "getTime": self.getTime, "getSender": self.getSender,
                       "getContent": self.getContent}

        for process in processlist:
            try:
                processlist[process](message)
            except:
                pass

    def getDate(self, message):
        self.date = re_date.match(message)[1]

    def getTime(self, message):
        self.time = re_time.match(message)[1]

    def getSender(self, message):
        self.sender = re_sender.match(message)[1]

    def getContent(self, message):
        self.content = re_content.match(message)[1]
        tempcontent = self.content.lower()
        self.wordslist = tempcontent.split(" ")


class chatStat():
    def __init__(self, chatname):
        self.chatname = chatname
        self.counter_sender = {}
        self.wordbank = Counter()
        self.timezone = Counter()

    def setFirstday(self, msg):
        re_year = re.compile(r'^(\d{4})-')
        re_month = re.compile(r'^\d{4}-(\d+)-')
        re_day = re.compile(r'^\d{4}-\d+-(\d+)')

        year = int(re_year.match(msg.date)[1])
        month = int(re_month.match(msg.date)[1])
        day = int(re_day.match(msg.date)[1])
        self.firstDay = datetime.date(year, month, day)
        self.chatAge = datetime.datetime.now().date() - self.firstDay

    def count_sender(self, msg):
        if msg.sender not in self.counter_sender:
            self.counter_sender[msg.sender] = 1
        else:
            self.counter_sender[msg.sender] += 1

    def get_count_sender(self):
        tempsender = sorted(self.counter_sender.items(),
                            key=lambda x: x[1], reverse=True)
        return tempsender

    def add_word_bank(self, msg):
        avoid_words = [r'i', 'to', 'the', 'you',
                       'a', 'my', 'and', 'was', 'it', 'for', 'of', 'is',
                       'but', '<media', 'omitted>', 'this', 'me', 'that',
                       r'i\'m', 'u', 'at', 'so', 'in', 'on', 'are', 'have',
                       'with', 'not', 'do', 'how', 'if', 'be', 'are', r"it\'s",
                       '?', 'no', 'what', 'can', 'just', 'when', 'too', 'actually']
        tempwordlist = [x for x in msg.wordslist if x not in avoid_words]
        self.wordbank.update(tempwordlist)

    def get_word_bank(self, n):
        return self.wordbank.most_common(n)

    def count_hours(self, msg):
        try:
            hour = re.compile(r'(\d+):\d+').match(msg.time)[1]

            self.timezone.update({hour: 1})
        except:
            pass

    def get_time_zones(self, n):
        return self.timezone.most_common(n)


for file in os.listdir('./'):
    if file.endswith('txt'):
        confirm_file = input("\nAnalyze {}? (Y/N)".format(file))
        if confirm_file.lower() == "y" or confirm_file.lower() == "yes":
            currentChat = chatStat(file)
            data = readfile(file)
            messages = data.split('\n')
            count_entry = 0
            for message in messages:
                msg = messageBank(message)
                if count_entry == 0:
                    currentChat.setFirstday(msg)
                count_entry += 1
                currentChat.count_sender(msg)
                currentChat.add_word_bank(msg)
                currentChat.count_hours(msg)
            print("\n\n-------------------------------------------------------")
            print("\nAnalysis on '{}'".format(file))
            print("\nFirst day:        {}".format(currentChat.firstDay))
            print("Days online:      {}".format(currentChat.chatAge))

            print('\n\n==========Chat Breakdown==========')
            print('\nO User info')
            print('\n{:<10s} {:>10s}'.format("User", "Percentage"))
            print('--------------------------')
            for user, times in currentChat.get_count_sender():
                if user != None:

                    percentage = round(times/count_entry * 100, 2)
                    print('{:<10s} {:>10.2f}%'.format(user, percentage))

                if user == None:
                    percentage = round(times/count_entry * 100, 2)
                    print('{:<10s} {:>10.2f}%'.format("N/A", percentage))
            print("--------------------------")
            print("\n\nO Most common words (displaying 15)")
            print('\n{:<10s} {:>10s}'.format("User", "Frequency"))
            print('--------------------------')
            for word, times in currentChat.get_word_bank(15):
                print('{:<10s} {:>10}'.format(word, times))

            print("\n\nO Popular hour range (displaying 15)")
            print('\n{:<10s} {:>10s}'.format("Hour", "Percentage"))
            print('--------------------------')
            for hour, times in currentChat.get_time_zones(15):
                percentage = round(times/count_entry * 100, 2)
                print('{:<10s} {:>10.2f}%'.format(hour, percentage))
            # for word, times in currentChat.get_word_bank(15):

            # print(currentChat.get_word_bank(20))

            break
        else:
            pass
