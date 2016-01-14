#!/usr/bin/env python3
# Chatbot.py

import time
import pickle
import random
import os
import sys

__author__ = 'Peter Maar'
__version__ = '0.1.0'

thingsToSayOld = []
smartSayDict = {}


def stripText(st):
    st += ' ' # Trailing space helps parse abbr.s
    
    # Strip out punctuation and grammer that might prevent the bot from recognising a phrase
    st = st.lower()
    st = st.replace('.', '')  # Period, question, or exclamation point, they are often mistakenly interchanged or left off
    st = st.replace(',', '')  # Commas are important, but also can be misused and confuse the chatbot more than it's worth
    st = st.replace('!', '')  # Period, question, or exclamation point, they are often mistakenly interchanged or left off
    st = st.replace('?', '')  # Period, question, or exclamation point, they are often mistakenly interchanged or left of
    st = st.replace(':', '')
    st = st.replace(';', '')
    st = st.replace('@', '')
    st = st.replace('#', '')
    st = st.replace('$', '')
    st = st.replace('%', '')
    st = st.replace('^', '')
    st = st.replace('&', '')
    st = st.replace('*', '')
    st = st.replace('(', '')
    st = st.replace(')', '')
    st = st.replace('-', '')
    st = st.replace('_', '')
    st = st.replace('=', '')
    st = st.replace('+', '')
    st = st.replace('/', '')
    st = st.replace('\\', '')
    st = st.replace('`', '')
    st = st.replace('~', '')
    st = st.replace('<', '')
    st = st.replace('>', '')
    while st.find('  ') != -1: # Remove double spaces
        st = st.replace('  ', ' ')
    
    # Translate out abbr.s
    st = st.replace(' lol ', ' laugh out loud ')
    st = st.replace(' l8r ', ' later ')
    st = st.replace(' h8r ', ' hater ')
    st = st.replace(' gmta ', ' great minds think alike ')
    st = st.replace(' irl ', ' in real life ')
    st = st.replace(' u ', ' you ')
    st = st.replace(' c ', ' see ')
    st = st.replace(' f8 ', ' fate ')
    st = st.replace(' tmi ', ' too much information ')
    st = st.replace(' gg ', ' good going ')
    st = st.replace(' rip ', ' rest in peace ')
    st = st.replace(' k ', ' okay ')
    st = st.replace(' jk ', ' just kidding ')
    
    # Simplify contractions to more consistent, spelled out words
    st = st.replace("an't", 'an not')  # Words like "can't"
    st = st.replace("n't", ' not')
    st = st.replace("'re", ' are')
    st = st.replace("'s ", ' is ') # 'is' is actually removed later anyways, but it is more clear to have it in two steps
    st = st.replace("'m ", ' am ')


    # Strip out some words/phrases/abbreviations to get closer to the actual meaning or point of the phrase so that sentences like "how is the weather" and "how is weather" are the same
    # To prevent partial stripping of words, the words must have spaces on both sides to be stripped
    st = st.replace(' a ', ' ')
    st = st.replace(' the ', ' ')
    st = st.replace(' is ', ' ')
    st = st.replace(' are ', ' ')
    st = st.replace(' fyi ', ' ')
    st = st.replace(' tbh ', ' ')

    while (len(st) > 1) and (st[-1] == ' ' or st[-1] == '\t'):
        st = st[:-1] # Remove trailing spaces

    while (len(st) > 1) and (st[0] == ' ' or st[0] == '\t'):
        st = st[1:] # Remove leading spaces

    return st
    

def processInput(inputToProcess):
    """Takes a string in. The string contains: BotLastSaid\n\n\n:::\n\n\nUsersNewReply"""
    botSaid = inputToProcess[:inputToProcess.find("\n\n\n:::\n\n\n")]
    userSaid = inputToProcess[inputToProcess.find("\n\n\n:::\n\n\n")+9:]
    global thingsToSayOld
    global smartSayDict

    print("Bot:", botSaid, " | ", "User said:", userSaid)
    print("Stripped Bot:", stripText(botSaid), " | ", "Stripped User said:", stripText(userSaid))
    


    
    ##### Load/Create File ########################################################################################################################################################################################################################################################
    try:
        loadmem()
    except FileNotFoundError:
        continueRun = ""
        while continueRun.lower() != "y":
            continueRun = 'y'#input("Looks like this program hasn't been run before. This program will generate a few files where it is located, so it is reccomended it is in a folder by itself, and executed from that directory.\nIs the program set up correctly? (y/n): ")
            if continueRun.lower() == "n":
                input("The program will now exit. Please move the file to a folder on its own, and execute in that directory.\nPress any key to exit...")
                exit()
        print("Great! Creating files and starting program.")
        setDefaultMem()
        savemem()
        time.sleep(1)
        print("\n\n\n\n\n\n\n\n\n\n") # Put some space betwen this message and the formal start
    ###############################################################################################################################################################################################################################################################################


    #### Store interaction ##########################################################################################################################################################################################################################################################
    if safeToStore(userSaid) and  botSaid.lower() != "what is your name?" and botSaid.lower() != "who are you?" and botSaid.lower() != "what time is it?": # Protect built-in dict. entries
        thingsToSayOld.append(userSaid)  # Store the phrase the user said
        try:
            smartSayDict[stripText(botSaid)].append(userSaid)  # Store the last interaction - use the stripped version of what the bot said
        except KeyError: # If the key doesn't exist yet, append won't work, so create it with the value
            smartSayDict[stripText(botSaid)] = [userSaid]
        savemem()
    ###############################################################################################################################################################################################################################################################################


    #### Reply ####################################################################################################################################################################################################################################################################
    # Use special Response if possible
    sr = specialResponse(userSaid.lower())  
    if sr != 0:
        return sr

    # Use a Smart Response if possible, otherwise just use the old random list of phrases
    if stripText(userSaid) in smartSayDict:  # If the stripped version of what the user said is a key in smartSayDict, return the value at that key
        return smartSayDict[stripText(userSaid)][random.randint(0, len(smartSayDict[stripText(userSaid)])-1)] # Return a random entry from the possible ones for this key
    else:
        return thingsToSayOld[random.randint(0, len(thingsToSayOld)-1)]
    ###############################################################################################################################################################################################################################################################################
    




def specialResponse(srIn):
    """Returns a special response to srIn. srIn should be a lowercase string. If there is no special response, returns 0"""
    if srIn == "what do you know?":
        print(str(thingsToSayOld) + "\n" + str(smartSayDict))  # Print to the console, but don't return/reply it
        return 0
    elif srIn.find("what time is it?") != -1:
        return currentTime()
    else:
        return 0






def currentTime():
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    if hour > 12:
        hour -= 12
        return str(hour) + ":" + minute + " PM"  # Minute is a string, to let us add a 0 to the beginning of it if needed
    else:
        return str(hour) + ":" + minute + " AM"  # Minute is a string, to let us add a 0 to the beginning of it if needed


def savemem():
    global thingsToSayOld
    global smartSayDict
    f1 = open(sys.path[0] + '/thingsToSayOld.pickle', 'wb')
    pickle.dump(thingsToSayOld, f1, pickle.HIGHEST_PROTOCOL) #Higher protocols may reduce compatibility, but are faster and create smaller files
    f1.close()
    f2 = open(sys.path[0] + '/smartSayDict.pickle', 'wb')
    pickle.dump(smartSayDict, f2, pickle.HIGHEST_PROTOCOL) #Higher protocols may reduce compatibility, but are faster and create smaller files
    f2.close()

def loadmem():
    global thingsToSayOld
    global smartSayDict
    f1 = open(sys.path[0] + '/thingsToSayOld.pickle', 'rb')
    thingsToSayOld = pickle.load(f1)
    f1.close()
    f2 = open(sys.path[0] + '/smartSayDict.pickle', 'rb')
    smartSayDict = pickle.load(f2)
    f2.close()

def setDefaultMem():
    global thingsToSayOld
    global smartSayDict
    thingsToSayOld = ["Yes", "No", "Oh", "Oh, okay", "What?", "I'm confused", "so...?", "What do you mean?", "Please clarify", "I don't get it", "meaning...", "Don't Forget to Be Awesome", "I love memes", "I love the internet", "Python is pretty cool, don't you agree? It may be a little limited in some aspects, but it's so easy to use!", "What's the weather like?", "How's the weather?", "How are you doing?", "How are you?"]
    #  "Who?", "What?", "When?", "Where?", "Why?", "How?", #asked way too much
    smartSayDict = {"hello!" : ["Hi!"], "hello" : ["Hi"], "hi!" : ["Hello!"], "hi" : ["Hello"], "how are you doing?" : ["Very well, how are you?"], "what is your name?": ["My name is Sapiens, who are you?"], "who are you?" : ["I'm Sapiens, what's your name?"], "bye" : ["Bye"], "bye!" : ["Bye!"], "i gtg" : ["k"], "gtg" : ["k"], "ttyl" : ["ttyl"]}  # A dictionary of the interactons in the format of "question : [replies]". Interactions will be added as "botMsg : usrReply" This will be referenced in reverse when the user types something

def isProfane(checkText):
    checkText = checkText.lower()
    # This list was created using various sites with statistics. Some are more profane than others, or can be mistakenly found inside other words, but it doesn't affect the reply, it just silently prevents storing it
    if checkText.find('fuck') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('ass') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('damn') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('bitch') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('shit') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('penis') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('vagina') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('bastard') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('boob') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('ballsack') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('crap') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('piss') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('dick') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('cock') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('pussy') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('asshole') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('fag') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('bastard') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('slut') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('douche') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('cunt') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('arse') != -1:  # If the word is found
        return True  # Return that there is profanity
    elif checkText.find('bollocks') != -1:  # If the word is found
        return True  # Return that there is profanity
    else:
        return False

def safeToStore(inputString):
    if not isProfane(inputString): # If no profanity
        return inputString.lower() != '' and inputString.lower().find("sapiens") == -1 and inputString.lower().find("name") == -1 and inputString.lower().find("i'm") == -1 and inputString.lower().find("i am") == -1 and inputString.lower().find("to leave") == -1 and inputString.lower().find("bye") == -1 and inputString.lower().find("ttyl") == -1 and inputString.lower().find("gtg") == -1 and inputString.lower().find("what do you know?") == -1 #Don't store if they said something about sapiens or names or leaving or 'what do you know
    else: # If there is profanity
        return False
    

if __name__ == "__main__":
    # execute only if run as a script
    outstuff = ''
    for i in range(10):
        stuff = outstuff + "\n\n\n:::\n\n\n" + input("Human says: ")
        outstuff = processInput(stuff)
        print("Bot says:", outstuff)
