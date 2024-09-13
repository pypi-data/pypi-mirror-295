from time import sleep

from invoke import task
import random
import webbrowser

@task()
def yell(c):
    print("AAAAAAAaaaafdffAHHH")

@task()
def open(c, link):
    list = {
        'talk': 'https://educationwarehouse.org/nextcloud/apps/spreed/',
        'pp': 'https://www.perplexity.ai/',
        'git': 'https://github.com/educationwarehouse',
        'taiga': 'https://taiga.edwh.nl/project/ewstudents',
    }

    if link == 'all':
        for x in list:
            webbrowser.open(list[x])
    elif link == '--help':
        print(list)
    else:
        try:
            webbrowser.open(list[link])
            return
        except:
            webbrowser.open('https://www.' + link + '.com/')
            return