#!/usr/bin/env python3

import requests
from lxml import html
from playsound import playsound
from datetime import datetime
import time

deliveries_to_go = 5
sound_incoming = 'alarm.mp3'
url = 'https://www.yodel.co.uk/tracking'


while True:
    tracker = input('Please enter a tracking number : ')
    if len(tracker) != 18 or tracker[:2] != 'JD':
        print('Please provide correct tracking number, JDXXXXXXXXXXXXXXXX')
    else:
        break


while True:
    page = requests.get('{0}/{1}'.format(url, tracker))
    tree = html.fromstring(page.content)
    number = tree.xpath('//*[@id="courier-box"]/div/div/h4/text()')

    if number:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('{0} - There are {1} deliveries before {2}'.format(now, number[0], tracker))
        if int(number[0]) < deliveries_to_go:
            playsound(sound_incoming)

    else:
        try:
            delivered_at = tree.xpath('/html/body/section[1]/div/ol/li[4]/div[2]/p/span/text()')[0]
        except IndexError:
            print('Unable to obtain delivery time details')
            exit(5)
        print('Delivered at : {0}'.format(delivered_at))
        playsound(sound_incoming)
        exit(0)

    time.sleep(120)
