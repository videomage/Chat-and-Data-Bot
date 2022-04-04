import pickle
from googlesearch import search
import webbrowser
from random import randrange
import time
import pymsgbox
import nltk.data

with open("User_Info_List", "rb") as fp:
    b = pickle.load(fp)

passkeyTry = False
passkey = True
action = False
loopActive = False
userList = b
qResponseListNo = ["I did not know that!", "that's very interesting", "I'll be sure to remember that"] #three entries
qResponseListYes = [" I think I remember that!", "I think that rings a bell!", " That's very interesting"] #three entries
chatGreetingList = ["hi!", "hello!", "greetings!", "sup!", "what's up?", "hey!"] #six entries
chatMoodAskList = ["how are you?", "how is your day going?", "how have you been?", "how's it going?",
                   "how are you doing?"] #five entries
chatMoodResponseList = ["I'm doing pretty good today!", "Pretty good!", "Great!", "Good!"] #four entries
chatNegResponseList = ["I'm sorry to hear about that", "Oh, that sucks", "Oh, well I hope you feel better!"
                       , "well I hope things shape up!"] #four entries
chatPosResponseList = ["I'm glad to hear that!", "That's good!", "That's great!", "I'm glad!"] #four entries
chatBadList = ["bad", "not the best", "not to good",] #three entries
chatGoodList = ["good", "great", "pretty good", "awesome", "ok"] #five entries
chatKnowList = ["know", "recognize","remember"] #three entries


while passkey != passkeyTry: #second phase security
    with open("User_Password.txt", "r") as usp:
        passkey = usp.read()
        passkeyTry = pymsgbox.password(text = 'Enter user password (default: ChatBotUser)', title = 'Password Entry', mask = '#' )

if passkey == "ChatBotUser":
    newPass = input("Please enter a new password >>")
    with open("User_Password.txt", "w") as usp:
        usp.truncate(0)
        usp.write(newPass)

musicChoice = input("Do you want to turn on some LoFi? (yes/no) >>")
if musicChoice == "yes":
    webbrowser.open_new('https://www.youtube.com/watch?v=5qap5aO4i9A')

loopActive = True

while loopActive == True:
    ad = input(
       "Hey there! What do you want to do? (learn, forget, search, chat, study) >> ")  # UPDATE IF NAME CHANGES AND WHEN MORE FUNCTIONS ARE ADDED!!!
    action = ad

    while action == "learn":
        question = input("What do you want to tell me? (type back to return to action selection) >>")
        if question == "back":
            action = False
            break
        choice = randrange(0, 2)


        def dyn(question):
            if any(question in s for s in userList):
                print(str(qResponseListYes[choice]))
            else:
                userList.append(str(question))
                print(str(qResponseListNo[choice]))


        dyn(question)
        with open("User_Info_List", "wb") as fp:
            pickle.dump(userList, fp)
        print(userList)

    while action == "forget":
        print(userList)
        question = input("Enter the entry to be forgotten (or type back to return to action selection) >>")
        if question == "back":
            action = False
            break
        def frgt(question):
            if any(question in s for s in userList):
                userList.remove(question)
                print("Forgotten!")
            else:
                print("I never learned that anyway!")
        frgt(question)
        with open("User_Info_List", "wb") as fp:
            pickle.dump(userList, fp)

    while action == "search":
        searchAsk = input("What do you want me to search for? (type back to return to action selection) >>")
        if searchAsk == "back":
            action = False
            break
        searchList = list(search(searchAsk))
        print(searchList)
        linkWant = int(input("Enter the number of the desired link (first link is 0) >>"))
        webbrowser.open_new(searchList[linkWant])

    while action == "study":
        studyFile = input("Enter study file (type back to return to action selection) >>")
        with open(studyFile,"rb") as fs:
            studyText = pickle.load(fs)
        print(studyText)
        if studyFile == "back":
            action = False
            break

    while action == "chat":
        chatAsk = input("(type back to return to action selection)>>")
        chatToken = nltk.word_tokenize(chatAsk)
        if chatAsk == "back":
            action = False
            break
        if any(str.lower(chatAsk) in s for s in chatGreetingList):
            maxList = len(chatGreetingList)
            responseChoice = randrange(0,maxList)
            print(chatGreetingList[responseChoice])
        if any(str.lower(chatAsk) in s for s in chatMoodAskList):
            maxList = len(chatMoodResponseList)
            responseChoice = randrange(0,maxList)
            print(chatMoodResponseList[responseChoice])
            time.sleep(2)
            maxList = len(chatMoodAskList)
            responseChoice = randrange(0,maxList)
            print(chatMoodAskList[responseChoice])
            chatAsk = input(">>")
        if any(s in chatAsk for s in chatGoodList):
            maxList = len(chatPosResponseList)
            responseChoice = randrange(0,maxList)
            print(chatPosResponseList[responseChoice])
        if any(s in chatAsk for s in chatBadList):
            maxList = len(chatNegResponseList)
            responseChoice = randrange(0,maxList)
            print(chatNegResponseList[responseChoice])
        if set(chatToken) & set(chatKnowList):
            maxUserList = len(userList)
            recall = randrange(0, maxUserList)
            randomListEntry = userList[recall]
            if "I" in randomListEntry:
                randomListEntry = randomListEntry.replace("I", "you")
            elif "i" in randomListEntry:
                randomListEntry = randomListEntry.replace("i", "you")
            if "am" in randomListEntry:
                randomListEntry = randomListEntry.replace("am", "are")
            print("I remember " + randomListEntry + "!")
