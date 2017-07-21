#!/usr/bin/env python3

import requests
from lxml import html
from playsound import playsound
from datetime import datetime
import time

deliveries_to_go = 5
sound_incoming = 'alarm.mp3'
url = 'https://www.yodel.co.uk/tracking'

# Basic tracking number validation
while True:
    tracker = input('Please enter a tracking number : ')
#    tracker = 'JD0002218204292880'
    if len(tracker) != 18 or tracker[:2] != 'JD':
        print('Please provide correct tracking number, JDXXXXXXXXXXXXXXXX')
    else:
        break

# Getting data from yodel and checking if:
#  - Yodel has parcel
#  - Parcel is out for delivery

page = requests.get('{0}/{1}'.format(url, tracker))
tree = html.fromstring(page.content)

with_yodel = tree.xpath('/html/body/section[1]/div/ol/li[2]/div[2]/p/text()')
if not with_yodel:
    print('\nYour parcel is not with Yodel yet.')
    exit(0)
else:
    transit_date = tree.xpath('/html/body/section[1]/div/ol/li[2]/div[2]/p/span/text()')
    print('\n{0:55}:{1}'.format(with_yodel[0],transit_date[0]))

with_courier_status = tree.xpath('//*[@id="courier-box"]/p/text()')
if not with_courier_status:
    print('Predicted delivery within 24h')
    exit(0)
else:
    courier_date = tree.xpath('//*[@id="courier-box"]/p/span/text()')
    print('{0:55}:{1}'.format(with_courier_status[0], courier_date[0]))

# Checking if  parcel is out for delivery and  starting tracking if so
number = tree.xpath('//*[@id="courier-box"]/div/div/h4/text()')
while True:
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
            exit(0)
        print('Delivered at' + ' '*43 + ':{0}'.format(delivered_at))
        playsound(sound_incoming)
        exit(0)

    time.sleep(120)
