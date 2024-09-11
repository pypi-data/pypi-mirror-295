from time import sleep

from invoke import task
import random
import webbrowser

@task()
def yell(c):
    print("AAAAAAAaaaafdffAHHH")

@task()
def open(c, link):
    list = [
        ['talk', 'https://educationwarehouse.org/nextcloud/apps/spreed/'],
        ['pp', 'https://www.perplexity.ai/'],
        ['git', 'https://github.com/educationwarehouse'],
        ['taiga', 'https://taiga.edwh.nl/project/ewstudents'],
    ]

    if link == 'all':
        for x in list:
            webbrowser.open(x[1])
    else:
        for x in list:
            if link == x[0]:
                webbrowser.open(x[1])
                return
        webbrowser.open('https://www.' + link + '.com/')

    # match link:
    #     case 'base':
    #         webbrowser.open('https://educationwarehouse.org/nextcloud/apps/spreed/')
    #         webbrowser.open('https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment')
    #         webbrowser.open('https://www.perplexity.ai/')
    #         webbrowser.open('https://github.com/educationwarehouse')
    #         webbrowser.open('https://taiga.edwh.nl/project/ewstudents/backlog')
    #         return
    #     case 'talk':
    #         webbrowser.open('https://educationwarehouse.org/nextcloud/apps/spreed/')
    #     case 'pp':
    #         webbrowser.open('https://www.perplexity.ai/')
    #     case 'git':
    #         webbrowser.open('https://github.com/educationwarehouse')
    #     case 'taiga':
    #         webbrowser.open('https://taiga.edwh.nl/project/ewstudents')
    #     case _:
    #         webbrowser.open('https://www.' + link + '.com/')