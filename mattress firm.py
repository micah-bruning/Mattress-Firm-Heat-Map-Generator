# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 13:45:23 2018

@author: micah
"""
from bs4 import BeautifulSoup
import gmplot
import pandas as pd
import requests
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mattress") 

#Get Page of Texas on Mattress Firm and make it into bs4 object
texas_list = requests.get('https://www.mattressfirm.com/stores/tx/')
soup = BeautifulSoup(texas_list.text, 'html.parser')

#Narrow down page to just the list of cities
city_body = soup.find(class_='map-list-wrap map-list-tall')

#Create an empty list and store all of the links in there
city_webs = []
for link in city_body.find_all('a', href=True):
    city_webs.append(link['href'])

#Make a bs4 object out of each page. Then, grab all adresses out of each page
#and add it to the master list


master_address_list = []
for page in city_webs:
    site = requests.get(page)
    soup2 = BeautifulSoup(site.text, 'html.parser')
    address_body = soup2.find(class_='map-list-wrap map-list-tall')

    for address in address_body.find_all('span', attrs={"class":"block address-1 bold fc-gray"}):
        master_address_list.append(address.string)

lats = []
longs = []
for a in master_address_list:
    try:
        location = geolocator.geocode(a)
        lats.append(location.latitude)
        longs.append(location.longitude)
    except:
        pass

#df = pd.DataFrame({'Latitude':lats, 'Longitude':longs})


gmap = gmplot.GoogleMapPlotter(29, -98, 10)

gmap.heatmap(lats, longs)

gmap.draw("heat.html")

    
    
