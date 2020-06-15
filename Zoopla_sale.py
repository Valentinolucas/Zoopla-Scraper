#!/usr/bin/python

import requests
import json
from datetime import date
import time
import os
import gzip

#API KEYS
zoopla_key = 'z7cyp8jsb3enyxxfvvs8s8fn'

uk_cities = [
'Bath',
'Birmingham',
'Bradford-on-Avon',
'Brighton & Hove',
'Bristol',
'Cambridge',
'Canterbury',
'Carlisle',
'Chelmsford',
'Chester Cheshire',
'Chichester',
'Coventry',
'Derby',
'Durham',
'Ely',
'Exeter',
'Gloucester',
'Hereford',
'Kingston upon Thames (Royal Borough)',
'Lancaster',
'Leeds',
'Leicester',
'Lichfield',
'Lincoln',
'Liverpool',
'City of London',
'Manchester',
'Newcastle upon Tyne, Tyne & Wear',
'Norwich',
'Nottingham',
'Oxford',
'Peterborough',
'Plymouth',
'Portsmouth',
'Preston',
'Ripon',
'Salford',
'Salisbury',
'Sheffield',
'Southampton',
'St Albans',
'Stoke on Trent',
'Sunderland',
'Truro',
'Wakefield',
'Wells, Somerset',
'Wells-next-the-Sea, Norfolk',
'City of Westminster',
'Winchester',
'Wolverhampton',
'Worcester',
'York'
]

last_city = 0
date = date.today()


class Zoopla_listings:
    '''
    This class defines a JSON object with all the listings of a given city
    '''

    def __init__(self,city_name,page_number=1):
        self.city_name = city_name
        self.date = date.today()
        self.count = 0
        self.page_number = page_number
        self.listing_qty = 1
        self.over_run = 0

    def property_download(self):
        url_base = 'http://api.zoopla.co.uk/api/v1/property_listings.js?' + '&page_number=' + str(self.page_number) + '&area=' + self.city_name + '&page_size=100&listing_status=sale&&api_key=z7cyp8jsb3enyxxfvvs8s8fn'
        rentals = requests.get(url_base)

        if rentals.status_code == 403:
            self.over_run = 1

        if rentals.status_code == 200:
            try:
                content_rental = rentals.content
                content_rental = json.loads(content_rental)
                #with open('/home/luqui/Sale_downloader/'+ str(date.year) + str(date.month) + str(date.day)+'/'+str(self.city_name) + ' ' + 'page' + ' ' + str(self.page_number) +' '+ str(self.date.month) + '-' + str(self.date.day) + '-' + str(self.date.year) + ' ' + str(self.date.hour) + str(self.date.minute) , 'w') as f:
                with gzip.GzipFile('/home/luqui/Sale_downloader/'+ str(date) +'/'+str(self.city_name) + ' ' + 'page' + ' ' + str(self.page_number) +' '+ str(self.date.month) + '-' + str(self.date.day) + '-' + str(self.date.year) + ' ' + str(self.date.hour) + str(self.date.minute) + ".gz" , 'w') as f:
                    json_str = json.dumps(content_rental) + "\n"
                    json_bytes = json_str.encode('utf-8')
                    f.write(json_bytes)
                    print(city +' page '+str(self.page_number)+ ' download is complete')
                self.listing_qty = len(content_rental['listing'])
                self.count += 1
                return self.listing_qty
                return self.count
            except TypeError:
                pass

    def listing_empty(self):
        if self.listing_qty == 0:
            return True

    def counter(self):
        if self.count == 99:
            return True

    def resume_download(self, city):
        pass

    def developer_over_run(self):
        if self.over_run == 1:
            return True


def last_created(string):
    global last_city
    list_of_files = os.listdir('/home/luqui/Sale_downloader/' + str(date))
    # list_of_files = os.listdir('/home/luqui/Rent_downloader')
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
        filename = os.path.split(latest_file)
        filename = filename[1]
        if string in filename:
            last_city = uk_cities.index(string)
            print(last_city)
            return last_city
    except:
        pass



if __name__ == '__main__':

    if os.path.exists('/home/luqui/Sale_downloader/'+ str(date)):
        os.chdir('/home/luqui/Sale_downloader/'+ str(date))
    else:
        os.mkdir('/home/luqui/Sale_downloader/' + str(date))
        os.chdir('/home/luqui/Sale_downloader/' + str(date))


    for city in uk_cities:
        last_created(city)

    else:
        for city in uk_cities[last_city:]:
            for page in range(80):
                properties = Zoopla_listings(city,page+1)
                properties.property_download()
                time.sleep(1)
                if properties.listing_empty():
                    break
                if properties.developer_over_run():
                    print('Developer Over Rate, sleeping for an hour...')
                    time.sleep(3600)






