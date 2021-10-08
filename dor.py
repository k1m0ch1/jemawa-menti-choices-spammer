import re
import sys
import json

import requests
from bs4 import BeautifulSoup as bs
from progress.bar import Bar
from art import text2art, art
from progress.spinner import Spinner

print(text2art("JEMAWA", font='small'))
print(f"Mentimeter Multiple choice spammer {art('random')}")
print("---------------------------------------------")

if len(sys.argv) < 2:
    print(f"\n( `ε´ ) you need to provide the menti page, ex: https://www.menti.com/uyupv3tww7")
    sys.exit(1)

TARGET = sys.argv[1]
KEY = TARGET.split('/',)[3]
DATA_PAGE = f"https://www.menti.com/core/vote-keys/{KEY}/series"
SUPPORTED_TYPE = ['choices', 'ranking']
if sys.argv[2] != "":
    CUSTOM = sys.argv[2]


firstPage = requests.get(DATA_PAGE, headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
})

if firstPage.status_code != 200:
    print(f"{firstPage.status_code} WTF I can't access the page (＃`Д´)")
    print(f"{firstPage.text}")
    sys.exit(1)

INIT = firstPage.json()
PRESENTER_ID = INIT['pace']['active']
if sys.argv[2] == "questions":
    for question in INIT['questions']:
        print(f"[{question['id']}] type: {question['type']} question: {question['question']}")
    sys.exit(1)
    
if sys.argv[2] != "":
    PRESENTER_ID = CUSTOM

PRESENTER_QUESTION = INIT['questions'][0] # default
for question in INIT['questions']:
    if PRESENTER_ID == question['id']:
        if question['type'] not in SUPPORTED_TYPE:
            print(f"WTF this is {question['type']}, didn't I tell you this is only for {SUPPORTED_TYPE}? (＃`Д´)")
            print(f"just wait until the presenter show the {SUPPORTED_TYPE} to vote")
            sys.exit(1)
        PRESENTER_QUESTION = question
        break


pqi = { f"{item['id']}": item['label'] for item in PRESENTER_QUESTION['choices']}
CURRENT_ID = INIT['pace']['active']
QUESTIONS = {question['id']: question for question in INIT['questions']}

if sys.argv[2] != "":
    print(f"\nCurrent Presenter Page {QUESTIONS[CUSTOM]['type']} {CUSTOM} {PRESENTER_QUESTION['question']}\n")
elif sys.argv[2] == "questions":
    print(f"\nyou choose custom page Page {QUESTIONS[CUSTOM]['type']} {CUSTOM} {PRESENTER_QUESTION['question']}\n")
else:
    print(f"\nCurrent Presenter Page {QUESTIONS[PRESENTER_ID]['type']} {PRESENTER_ID} {PRESENTER_QUESTION['question']}\n")

for choice in PRESENTER_QUESTION['choices']:
    print(f"ID {choice['id']} LABEL {choice['label']}")
choice = input(f"\nWhich ID you want to vote: ")
loop = input("how much vote you want to sent: ")
print(f"\nyou pick '{pqi[choice]}' to vote '{loop}' times\n")
sure = input("you sure about this? (Y/N) ").lower()
if sure == 'n':
    print("bye")
    sys.exit(0)

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
    
    if sys.argv[2] != "":
        PRESENTER_ID = CUSTOM

    DATA = {
        'question_type': QUESTIONS[PRESENTER_ID]['type'],
        'vote': choice
    }    

    if QUESTIONS[PRESENTER_ID]['type'] == "ranking":
        DATA['vote'] = [int(choice)]

    vote = requests.post(f"https://www.menti.com/core/votes/{PRESENTER_ID}", headers=headers, json=DATA)

    if vote.status_code != 200:
        print(f"{vote.status_code} HAHAHAHAHA LOOKS LIKE ERROR, LOOKS WHAT YOU DID ┐('～`;)┌")
        print(vote.text)
        break
    
    bar.next()
bar.finish()

