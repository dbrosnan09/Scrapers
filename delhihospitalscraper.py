#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import re
from datetime import datetime
import pytz
timezone = pytz.timezone("America/New_York")
from dateutil.parser import parse

"""
scraper for Delhi websites:
there are two sources for their data. these are js files that contain a single js variable with json data

(1)facility data:
https://coronabeds.jantasamvad.org/covid-facilities.js

(2) bed data:
https://coronabeds.jantasamvad.org/covid-info.js

goal is to scrape both, get into python dict form and combine

output should be list of dictionaries, one for each hospital. format is :

{'DISTRICT': 'ARARIA', 'NAME': 'Govt. Polytechnic Araria Boys Hostel (Block-A)', 'LOCATION': {'LATTITUDE': 26.14689, 'LONGITUDE': 87.41251}, 'HOSPITAL TYPE': 'Other', 'FACILITY TYPE': 'DCHC', 'LAST UPDATED': datetime.datetime(2021, 7, 23, 13, 43, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>), 'TOTAL BEDS': 50, 'VACANT BEDS': 50, 'TOTAL ICU BEDS': 0, 'VACANT ICU BEDS': 0, 'TELEPHONE': 9431411845, 'SCRAPE TIME': datetime.datetime(2021, 7, 26, 17, 2, 29, 205004, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>)}

"""


#scraper for (1) facility data:
session = HTMLSession()
url = 'https://coronabeds.jantasamvad.org/covid-facilities.js'
delhi_total_content = session.get(url)
facility_json = delhi_total_content.text

#facility_json is a js file where a variable is named with the data. must get the variable naming out of the js, so just have data. the json data must start with "{" so find the index of the first "{" to get only the json data

json_start_index = facility_json.find("{")
facility_json = facility_json[json_start_index:]



#facility is a string in dict form, must shave off final ";" from js formatting
facility_json = (facility_json[:len(facility_json)-1])

#js has "null" for some latitudes, this doesnt work well with python, so changed null to ''
facility_json = facility_json.replace('null', "''")

#change string into a python dict
facility_json = eval(facility_json)

"""
facility_json is now a dict of this format: 
  "Bansal Hospital & Research Centre, New Friends Colony": {
    "type": "Pvt",
    "facility_type": "Hospital",
    "address": "Friends Colony, New Friends Colony, New Delhi, Delhi 110025",
    "contact_numbers": [
      "9650846789",
      "01146583333",
      "9650795533"
    ],
    "latitude": "28.56397",
    "longitude": "77.27154",
    "location": "https://www.google.com/maps/dir//Bansal+Hospital,+Friends+Colony,+New+Friends+Colony,+New+Delhi,+Delhi+110025/@28.5638237,77.2693463,17z/data=!4m9!4m8!1m0!1m5!1m1!1s0x390cfd22ec2ea155:0xf4855bc92c9bff93!2m2!1d77.271535!2d28.563819!3e0"
  },"next hospital":

  """

time_of_scraping = datetime.now(timezone)

#initialize output of facility data
facility_list = []

#loop through all facility data to get it into final form for saving to db
for key, value in facility_json.items(): 
  hosp_dict = {}
  hosp_dict['DISTRICT'] = None
  hosp_dict['NAME'] = key
  hosp_dict['LOCATION'] = {}
  #because converted nulls to '' in prior lat long step, cant convert those to float, so just store '' instead
  try:
    hosp_dict['LOCATION']['LATITUDE'] = float(value['latitude'])
  except:
    hosp_dict['LOCATION']['LATITUDE'] = value['latitude']
  try:
    hosp_dict['LOCATION']['LONGITUDE'] = float(value['longitude'])
  except:
    hosp_dict['LOCATION']['LONGITUDE'] = value['longitude']

  hosp_dict['HOSPITAL TYPE'] = value['type']
  hosp_dict['FACILITY TYPE'] = value['facility_type']
  hosp_dict['TELEPHONE'] = value['contact_numbers'][0]
  hosp_dict['SCRAPE TIME'] = time_of_scraping

  facility_list.append(hosp_dict)


#now facility_list is a list of dicts with all facility data in python friendly form. must combine this with bed data list using NAME as key


#scraper for (2) bed data:
session = HTMLSession()
url = 'https://coronabeds.jantasamvad.org/covid-info.js'
delhi_total_content = session.get(url)
bed_json = delhi_total_content.text

#facility_json is a js file where a variable is named with the data. so get the variable naming out of the js, so just have data. the json data must start with "{" so find the index of the first "{" to get only the json data

json_start_index = bed_json.find("{")
bed_json = bed_json[json_start_index:]



#facility is a string in dict form, must shave off final ";" from js formatting
bed_json = (bed_json[:len(bed_json)-1])

#js has "null" for some lattitudes, this doesnt work well with python, so changed null to ''
bed_json = bed_json.replace('null', "''")

#change string into a python dict
bed_json = eval(bed_json)

#multiple keys in this json (beds, updated, o2 amounts) so restrict to beds
bed_json = bed_json['beds']

#combine facilities json with bed json using name as key
for key, value in bed_json.items():

  for hospital in facility_list:
    if key == hospital['NAME']:

      hospital['LAST UPDATED'] = parse(value['last_updated_at'])
      hospital['TOTAL BEDS'] = value['total']
      hospital['VACANT BEDS'] = value['vacant']
      hospital['HOSPITAL TYPE'] = value['type']
      #delhi does not provide icu bed data so:
      hospital['TOTAL ICU BEDS'] = None
      hospital['VACANT ICU BEDS'] = None

for hospital in facility_list:
  print(hospital)
  print("       ")

#output data is in list of dicts called facility_list