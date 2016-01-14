#!/usr/bin/env python3
# Chatbot-test.py

# This short program tests out some of the Chatbot, making sure it won't crash. Needs Chatbot v0.2.0 or later.

import Chatbot  # PyCharm seems to think this is an error, but it seems fine.
import random
import os
import sys

__author__ = 'Peter Maar'
__version__ = '1.0.0'

Chatbot.debugTestMode = True
humanSayList = ["Hello!", "How are you?", "What is your name?", "What time is it?", "How's the weather?", "DFTBA", "Good Morning!", "Bye!", "I gtg", "Just FYI idk who u are."]
outstuff = ''
for i in range(100):
    humanSays = humanSayList[random.randint(0, len(humanSayList)-1)]
    print("Human says:", humanSays)
    stuff = outstuff + "\n\n\n:::\n\n\n" + humanSays
    outstuff = Chatbot.processInput(stuff)
    print("Bot says:", outstuff)
    humanSayList.append(outstuff)

print("\n\n\n\n\n\n\n\n\n\n")
print(Chatbot.thingsToSayOld)
print("\n\n\n\n\n")
print(Chatbot.smartSayDict)

os.remove(sys.path[0] + "/DEBUG-smartSayDict.pickle")
os.remove(sys.path[0] + "/DEBUG-thingsToSayOld.pickle")
