```
    _  ___  __  __    _   __      __   _
 _ | || __||  \/  |  /_\  \ \    / /  /_\
| || || _| | |\/| | / _ \  \ \/\/ /  / _ \
 \__/ |___||_|  |_|/_/ \_\  \_/\_/  /_/ \_\

Mentimeter Manipulator
```

I know this is stupid but its fun, my company using this to vote "something" for a fun event, so I think it will be fun to makes a good laugh for a day in front everyone, so thats it, I create this tools only for fun.

This tools is created experimented for the mentimeter platform.

> DISCLAIMER or USE AT YOUR OWN RISK, These tools should be considered for educational and research purposes only, this tools is made not to violate the law or abuse the system. Any action you take by using this tools is strictly at your own risk. The creator is not responsible for any action

TL;DR version :

Click the video to see how it work.

[![Jemawa](https://img.youtube.com/vi/sVb0bos-vkQ/0.jpg)](https://www.youtube.com/watch?v=sVb0bos-vkQ "JEMAWA the mentimeter multiple choice vote spammer")

## How to use ?

we publish on pypi, you could run jemawa by install with this command

```
pip install jemawa
```

after that you can run `jemawa` command

```
jemawa <mentimeter vote page link or menti code> <optional command>
```

example

```
jemawa https://www.menti.com/alg3v6yduhsr
```

or

```
jemawa 26876868
```

Optional Command list:
`ls` to list all the question alongside with ID
`slide_id` to direct vote to the slide

Currently Slide Type we can spam is:
1. Multiple Choice
2. Ranking Type <FIXING>
3. Wordcloud <FIXING>
4. Open Ended
5. Scales 
6. Q&A
7. 2x2 grid vote

## Custom page vote

Now you can vote on any page not by only presented page, to do this you can run this

```
jemawa <link> questions
```

to list the questions, after that get the question ID and run this

```
jemawa <link> <questionID>
```

so it will continue like normal

## How this is work?

alright so you want to know, actually you can spam vote by creating a new session or a new identifier to every vote, you know its like whenver you want to vote, just simply open a new private browser, and vote.

so this is how program work.

1. We need to get which page is presented by presenter
2. get the content of the vote, ID and label
3. choose the ID to vite
4. tell the tools much vote you want
5. bot will get a new identifier for voting
6. and just vote.

## What is jemawa ?

indonesian word for 'arrogant'

## Development

to run the development, use the `python dev.py ..`

## Contributors

![GitHub Contributors Image](https://contrib.rocks/image?repo=k1m0ch1/jemawa-menti-choices-spammer)
