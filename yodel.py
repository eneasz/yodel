#!/usr/bin/env python3
"""TODO: Handle situation where parcel is in state saying contact driver"""

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
    if len(tracker) < 18 or tracker[:1] != 'J':
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
    print('{0:55}:{1}\n'.format(with_courier_status[0], courier_date[0]))

# Checking if  parcel is out for delivery and  starting tracking if so
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
            rearrange = tree.xpath('/html/body/section[1]/div/ol/li[4]/div[2]/p/a/text()')[0]
            if rearrange == 'Rearrange':
                print('You missed your parcel, please rearrange delivery with Yodel {}'.format(rearrange))
                exit(0)
            elif rearrange == 'HAVE YOUR SAY':
                delivered_at = tree.xpath('/html/body/section[1]/div/ol/li[4]/div[2]/p/span/text()')[0]
                print('\tDelivered at' + ' ' * 39 + ':{0}'.format(delivered_at))
                exit(0)
        except IndexError:
            contact = tree.xpath('//*[@id="courier_details"]/a/test()')
            print('There was a problem with your parcel details, try later {}'.format(contact))


    time.sleep(120)
