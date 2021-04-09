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

firstPage = requests.get(TARGET, headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
})

if firstPage.status_code != 200:
    print(f"{firstPage.status_code} WTF I can't access the page (＃`Д´)")
    print(f"{firstPage.text}")
    sys.exit(1)

soup = bs(firstPage.text, 'html.parser')
script = soup.find_all('script')[5]
p = re.compile('window.__CONFIG__ = (.*);').search(script.string)
CONFIG = json.loads(p.group(1))

p = re.compile('window.__INITIAL_STATE__ = (.*);').search(script.string)
INIT = json.loads(p.group(1))

PRESENTER_ID = INIT['pace']['presenter']['presenterId']
PRESENTER_QUESTION = INIT['questions'][0] # default
for question in INIT['questions']:
    if PRESENTER_ID == question['id']:
        if question['type'] != 'choices':
            print(f"WTF this is {question['type']}, didn't I tell you this is only for MULTIPLE CHOICE? (＃`Д´)")
            print("just wait until the presenter show the multiple choices to vote")
            sys.exit(1)
        PRESENTER_QUESTION = question
        break
pqi = { f"{item['id']}": item['label'] for item in PRESENTER_QUESTION['choices']}
CURRENT_ID = INIT['pace']['presenter']['presenterId']

print(f"Current Presenter Page {PRESENTER_ID} {PRESENTER_QUESTION['question']}\n")
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

    getIdentifier = requests.post("https://www.menti.com/core/identifiers", json={}, headers={
        "origin": "https://menti.com",
        "referer": TARGET,
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    })

    if getIdentifier.status_code != 200:
        print(f"{getIdentifier.status_code} yo I can't get the Identifier (⊙_⊙)")
        print(getIdentifier.text)
        break

    IDENTIFIER = getIdentifier.json()['identifier']

    vote = requests.post(f"https://www.menti.com/core/votes/{PRESENTER_ID}", headers={
        "origin": "https://menti.com",
        "referer": TARGET,
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "x-identifier": IDENTIFIER
    }, json={
        'question_type': 'choices',
        'vote': choice
    })

    if vote.status_code != 200:
        print(f"{vote.status_code} HAHAHAHAHA LOOKS LIKE ERROR, LOOKS WHAT YOU DID ┐('～`;)┌")
        print(vote.text)
        break
    bar.next()
bar.finish()

