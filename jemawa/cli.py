import re
import sys
import json
import threading
import math

import requests
from bs4 import BeautifulSoup as bs
from progress.bar import Bar
from art import text2art, art
from progress.spinner import Spinner

def main():
    print(text2art("JEMAWA", font='small'))
    print(f"Mentimeter Multiple choice spammer {art('random')}")
    print("---------------------------------------------")

    if len(sys.argv) < 2:
        print(f"\n( `ε´ ) you need to provide the menti page, ex: https://www.menti.com/uyupv3tww7 or type `help` to get the instruction")
        sys.exit(1)

    IS_CUSTOM_VOTE = len(sys.argv) == 3
    TARGET = sys.argv[1]

    if TARGET == "help":
        help()
        return

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }

    if TARGET.isnumeric():
        getKey = requests.get(f"https://www.menti.com/core/vote-ids/{TARGET}/series", headers=HEADERS)
        if getKey.status_code == 200:
            dataReturn = getKey.json()
            KEY = dataReturn['vote_key']
    else:
        KEY = TARGET.split('/',)[3]
        
    DATA_PAGE = f"https://www.menti.com/core/vote-keys/{KEY}/series"
    SUPPORTED_TYPE = ['choices', 'ranking', 'wordcloud', 'open', 'scales', 'qfa', 'prioritisation', 'rating', 'slide']
   
    CUSTOM= ""
    if IS_CUSTOM_VOTE:
        CUSTOM = sys.argv[2]

    # get the active page of slide
    firstPage = requests.get(DATA_PAGE, headers=HEADERS)

    if firstPage.status_code != 200:
        print(f"{firstPage.status_code} WTF I can't access the page (＃`Д´)")
        print(f"{firstPage.text}")
        sys.exit(1)

    INIT = firstPage.json()

    print(f"\n=== {INIT['name']} available at https://menti.com/{INIT['id']} ===\n")

    PRESENTER_ID = INIT['pace']['active']
    if IS_CUSTOM_VOTE:
        PRESENTER_ID = CUSTOM
        if PRESENTER_ID.isdigit():
            PRESENTER_ID = INIT['questions'][int(PRESENTER_ID)-1]['id']
        if sys.argv[2] == "ls":
            print("= List of accessible page =")
            for i, question in enumerate(INIT['questions']):
                print(f"{i+1}. [{question['id']}] type: {question['type']}, question: \"{question['question']}\"")
            print("to pick on of the page you can run `jemawa <menti page> <number>")
            sys.exit(1)

    PRESENTER_QUESTION = INIT['questions'][0] # default
    if not PRESENTER_ID:
        PRESENTER_ID = PRESENTER_QUESTION['id']
    for question in INIT['questions']:
        if PRESENTER_ID == question['id']:
            if question['type'] not in SUPPORTED_TYPE:
                print(f"WTF this is {question['type']}, didn't I tell you this is only for {SUPPORTED_TYPE}? (＃`Д´)")
                print(f"just wait until the presenter show the {SUPPORTED_TYPE} to vote")
                sys.exit(1)
            PRESENTER_QUESTION = question
            break

    pqi = { f"{item['id']}": item['label'] for item in PRESENTER_QUESTION['choices']}
    QUESTIONS = {question['id']: question for question in INIT['questions']}

    if IS_CUSTOM_VOTE:
        if sys.argv[2] == "questions":
            print(f"\nCurrent Presenter Page {QUESTIONS[CUSTOM]['type']} {CUSTOM} {PRESENTER_QUESTION['question']}\n")
    else:
        print(f"\nCurrent Presenter Page {QUESTIONS[PRESENTER_ID]['type']} {PRESENTER_ID} {PRESENTER_QUESTION['question']}\n")

    if QUESTIONS[PRESENTER_ID]['type'] == "qfa":
        page = 0
        parseQA = []
        while True:
            page += 1
            getQA = requests.get(f"https://www.menti.com/core/vote-keys/{KEY}/qfa?page={page}", headers=HEADERS)
            dataQA = getQA.json()
            parseQA += [item for item in dataQA['data']]
            if len(dataQA['data']) == 0:
                break
        for q in parseQA:
            print(f"ID {q['id']} {q['question']}")
    
    if QUESTIONS[PRESENTER_ID]['type'] in ["choices", "ranking"]:
        for choice in PRESENTER_QUESTION['choices']:
            print(f"ID {choice['id']} LABEL {choice['label']}")

    if QUESTIONS[PRESENTER_ID]['type'] == "slide":
        print("LETS SPAM HEART <3")
        
    value = ""
    if QUESTIONS[PRESENTER_ID]['type'] in ['wordcloud', 'open']:
        choice = input(f"\nWhat text you want to sent: ")
    elif QUESTIONS[PRESENTER_ID]['type'] == "scales":
        choice = input(f"\nWhich ID you want to vote: ")
        while True:
            value = input(f"\nInsert the value from 1-5: ")
            value = int(value)
            if value<0 or value >5:
                print("WTF? re-input mf")
            else:
                reValue = [value,1]
                value = {
                    f"{choice}": value
                }
                break
    elif QUESTIONS[PRESENTER_ID]['type'] == "rating":
        choice = input(f"\nWhich ID you want to vote: ")
        while True:
            valueHorizontal = input(f"\nInsert horizontal axis value from 1-10: ")
            valueHorizontal = int(valueHorizontal)
            if valueHorizontal<0 or valueHorizontal >10:
                print("WTF? re-input mf")
            else:
                valueVertical = input(f"Insert vertical axis value from 1-10: ")
                valueVertical = int(valueVertical)
                if valueVertical<0 or valueVertical >10:
                    print("WTF? re-input mf")
                else:
                    value = [valueHorizontal, valueVertical]
                    break

    elif QUESTIONS[PRESENTER_ID]['type'] == "prioritisation":
        selected_choice = input("\nWhich id do you want to prioritize:")
        value = { choice['id']: 0 for choice in PRESENTER_QUESTION['choices'] }
        value[selected_choice] = 100

    elif QUESTIONS[PRESENTER_ID]['type'] == "slide":
        choice = 'heart1'
            
    else:
        choice = input(f"\nWhich ID you want to vote: ")

    loop = input("how much vote you want to sent: ")
    if QUESTIONS[PRESENTER_ID]['type'] in ['wordcloud', 'open']:
        print(f"\nyou pick '{choice}' to vote '{loop}' times\n")
    elif QUESTIONS[PRESENTER_ID]['type'] == "qfa":
        print(f"\nyou pick '{choice}' to vote '{loop}' times\n")
    elif QUESTIONS[PRESENTER_ID]['type'] == "prioritisation":
        print(f"\nyou pick '{selected_choice}' to vote '{loop}' times\n")
    elif QUESTIONS[PRESENTER_ID]['type'] == "slide":
        print(f"\nyou pick '{loop}' times\n")
    else:
        print(f"\nyou pick '{pqi[choice]}' to vote '{loop}' times\n")
    sure = input("you sure about this? (Y/N) ").lower()
    if sure == 'n':
        print("bye")
        sys.exit(0)

    threads = []

    loopround = 4 if int(loop)%2 == 0 else 5
    loop = int(math.ceil(int(loop)/loopround))

    for i in range(0, loopround):
        t = threading.Thread(target=execute, args=(TARGET, IS_CUSTOM_VOTE, QUESTIONS, CUSTOM, choice, PRESENTER_QUESTION,value , loop, PRESENTER_ID))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

def execute(TARGET, IS_CUSTOM_VOTE, QUESTIONS, CUSTOM, choice, PRESENTER_QUESTION, value , loop, PRESENTER_ID):
    
    bar = Bar('w00t w00t', max=int(loop))
    for until in range(0, int(loop)):

        headers = {
            "origin": "https://menti.com",
            "referer": TARGET,
            "accept": "application/json",
            "content-type": "application/json; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        getIdentifier = requests.post("https://www.menti.com/core/identifiers", json={}, headers=headers)

        if getIdentifier.status_code != 200:
            print(f"{getIdentifier.status_code} yo I can't get the Identifier (⊙_⊙)")
            print(getIdentifier.text)
            break

        headers['x-identifier'] = getIdentifier.json()['identifier']
        
        if IS_CUSTOM_VOTE:
            PRESENTER_ID = CUSTOM

        DATA = {
            'question_type': QUESTIONS[PRESENTER_ID]['type'],
            'vote': choice
        } 

        if QUESTIONS[PRESENTER_ID]['type'] == "ranking":
            DATA['vote'] = [int(choice)]

        if QUESTIONS[PRESENTER_ID]['type'] in ["scales", "prioritisation"] :
            DATA['vote'] = value

        if QUESTIONS[PRESENTER_ID]['type'] == "slide":
            DATA['vote'] = choice

        if QUESTIONS[PRESENTER_ID]['type'] == "rating":
            values={c['id']: [0,0] for c in PRESENTER_QUESTION['choices']}
            values[int(choice)] = value
            DATA['vote'] = values

        if QUESTIONS[PRESENTER_ID]['type'] == "qfa":
            vote = requests.post(f"https://www.menti.com/core/qfa/{choice}/upvote", headers=headers, json={})
        else:
            vote = requests.post(f"https://www.menti.com/core/votes/{PRESENTER_ID}", headers=headers, json=DATA)

        if vote.status_code not in [201, 200]:
            print(f"{vote.status_code} HAHAHAHAHA LOOKS LIKE ERROR, LOOKS WHAT YOU DID ┐('～`;)┌")
            print(vote.text)
            break
        
        bar.next()
    bar.finish()

def help():
    print("Jemawa is the tools to spam the mentimeter page")
    print("\n you can run by running the command `jemawa <menti page/code> <optional command>`")
    print("for example `jemawa 12345611` to get the current active page and vote the page")
    print("\nAvailable Command:")
    print("- <menti page/code>    : you can use active page like https://www.menti.com/alwqyhbebzzr or 12345611")
    print("\n- <optinal command>    : is always after the menti page/code, with available command `ls` and `question ID`")
    print("                       : for example running `jemawa 12345611 ls` will reveal existing question")
    print("                       : and by running `jemawa 12345611 df3rgr7drk1v` will vote the page direct without follow the active page")
