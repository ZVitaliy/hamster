from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import requests
import datetime
import json
import random
import time
import os
import csv
import logging
from os import getcwd


# Errors logging
LOG_PATH = '{}/my_app.log'.format(getcwd())
LOG_FORMAT = '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s: %(message)s'

logger = logging.getLogger('MODULE_NAME')
formatter = logging.Formatter(LOG_FORMAT)
logfile = logging.FileHandler(LOG_PATH)
logfile.setFormatter(formatter)
logfile.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(logfile)

delay = 12
logger.warning(f'Flood wait: {delay} seconds.')

# User data
delay = random.randint(0, 60)/10 # Random time from 0.1 ms to 6 seconds

USER_AGENT = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:70.0) Gecko/20100101 Firefox/70.0'
URL = 'https://xhamster.com/x-api'
usr_login = 'seros14986@fft-mail.com'
usr_pass = 'Q!w2e3r4'
cookies = 'd4636acc974e7c12b775d8939ec043da11586108448' # Cookies must be set manually from logged in profile


# Autorization request
r = requests.get(URL)
s = requests.Session()
data = {
        'login': usr_login,
        'password': usr_pass,
        'user-agent': USER_AGENT,
}
s.post(URL, data=data)


#Open URLs from CSV file by rows and check on friendship
def urls_checker():
    with open('urls.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            page = '\n'.join(row)
            r = requests.get(page, timeout=delay).text
            soup = BeautifulSoup(r, 'html.parser')
            # Checking the tooltip does the profile invited or not
            for i in soup.find_all('div', class_='invite-to-friends'):
                invite = i.find('button', class_='add-to-friends xh-button black')
                btn_info = i.find(attrs={'data-tooltip': 'Invite to friends'})
                print(page)
                print(btn_info['data-tooltip'])
                try:
                    if btn_info['data-tooltip'] == 'Invite to friends':
                        # Write not a friend URLs into CSV file
                        with open('result.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(page.split())
                            print('The URL was added to CSV file')
                    else:
                        continue
                except:
                    print('Something went wrong!')


urls_checker()
