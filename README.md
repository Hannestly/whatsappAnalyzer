# Chat Analyzer
Python Library to parse chat data and analyze

## Quick start
1. Have your whatsapp chat saved as .txt file without media 
2. Clone or download the repository
2. Import all (*) from 'whatsapp.py'
```python
from whatsapp import *
```
3. Instantiate a 'ChatBank' object using the chat text file
```python
ChatObject = ChatBank("Chatfile.txt")     # insert path to chat file
```

## Simple demo
```python
from whatsapp import *

chatObject = ChatBank(chat_file_path="myChat.txt", avoid_file="avoid_list.txt")

print(chatObject.users)   # prints Chat users in Counter
print(ChatObject.userwords["John Park"].most_common(10))  # prints top 10 most commonly used words by user "John Park"
```

## Current Features
- First day of chat, chat's age 
- Users involved in chat, and percentage of messages sent by user
- Top most commonly used words (editable in code)(default showing at 15) 
- Most popular messaging hours (time ranges)
- Top most commonly used words by a user


## Dependencies
The following project currently does not contain any modules outside of Python's default modules. 

Modules used..
- os
- datetime
- collections
- regex
