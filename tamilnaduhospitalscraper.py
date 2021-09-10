#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import pytz
timezone = pytz.timezone("America/New_York")


#scraper for tamil nadu

#PLEASE NOTE!!! Not all hospitals had data for Total Beds. So instead saved BedsAllotedForCovidTreatment to Total Beds


"""
Output should be in format: 
{'LOCATION': {'LATITUDE': 12.4461866, 'LONGITUDE': 79.9346603}, 'DISTRICT': 'Chengalpattu', 'NAME': 'Zamin Endathur', 'FACILITY TYPE': 'ICCC', 'LAST UPDATED': datetime.datetime(2021, 7, 28, 12, 28, 59), 'TOTAL BEDS': 33, 'VACANT BEDS': 33, 'TOTAL ICU BEDS': 0, 'VACANT ICU BEDS': 0, 'TELEPHONE': '9952966370', 'SCRAPE TIME': datetime.datetime(2021, 7, 28, 10, 15, 35, 143954, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>)}

"""



"""
site populates via api, so api is used to scrape. one complication: must manually add in all districts to the json in the api request

District IDs for api requests (found by monitoring XHR requests in chrome inspector when select district on web page)


District	District ID	Hospital Count
Ariuyalur	5ea0abd3d43ec2250a483a4f	23
Chengalpattu	5ea0abd4d43ec2250a483a61	65
Chennai	5ea0abd2d43ec2250a483a40	262
Coimbatore	5ea0abd3d43ec2250a483a4a	143
Cuddalore	5ea0abd3d43ec2250a483a50	55
Dharmapuri	5ea0abd2d43ec2250a483a43	16
Dindigul	5ea0abd3d43ec2250a483a4b	57
Erode	5ea0abd2d43ec2250a483a48	55
Kallakurichi	5ea0abd4d43ec2250a483a5f	26
Kancheepuram	5ea0abd2d43ec2250a483a41	39
Kanniyakumari	5ea0abd3d43ec2250a483a5c	55
Karur	5ea0abd3d43ec2250a483a4c	44
Krishnagiri	5ea0abd3d43ec2250a483a5d	44
Madurai	5ea0abd3d43ec2250a483a56	127
Mayiladuthari	60901c5f2481a4362891d572	14
Nagapattinam	5ea0abd3d43ec2250a483a51	10
Namakkal	5ea0abd2d43ec2250a483a47	57
Nilgiris	5ea0abd3d43ec2250a483a49	23
Perambalur	5ea0abd3d43ec2250a483a4e	25
Pudukkotai	5ea0abd3d43ec2250a483a54	39
Ramanathapuram	5ea0abd3d43ec2250a483a59	34
Ranipet	5ea0abd4d43ec2250a483a63	25
Salem	5ea0abd2d43ec2250a483a46	115
Sivagangai	5ea0abd3d43ec2250a483a55	40
Tenkasi	5ea0abd4d43ec2250a483a60	24
Thanjavur	5ea0abd3d43ec2250a483a53	70
Theni	5ea0abd3d43ec2250a483a57	29
Thiruchirappalli	5ea0abd3d43ec2250a483a4d	114
Thirupathur	5ea0abd4d43ec2250a483a62	12
Thiruvarur	5ea0abd3d43ec2250a483a52	25
Thoothukudi	5ea0abd3d43ec2250a483a5a	51
Tirunelveli	5ea0abd3d43ec2250a483a5b	58
Tiruppur	5ea0abd4d43ec2250a483a5e	68
Tiruvallur	5ea0abd1d43ec2250a483a3f	44
Tiruvannamalai	5ea0abd2d43ec2250a483a44	30
Vellore	5ea0abd2d43ec2250a483a42	25
Villupuram	5ea0abd2d43ec2250a483a45	21
Virudhunagar	5ea0abd3d43ec2250a483a58	50


Total Hospitals = 2014 as of 7/28/21

"""


#api call
url = 'https://tncovidbeds.tnega.org/api/hospitals'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
hospital_json = requests.post(url, data=r'''{"searchString":"","sortCondition":{"Name":1},"pageNumber":1,"pageLimit":100000,"SortValue":"Availability","ShowIfVacantOnly":"","Districts":["5ea0abd3d43ec2250a483a4f","5ea0abd4d43ec2250a483a61","5ea0abd2d43ec2250a483a40", "5ea0abd3d43ec2250a483a4a","5ea0abd3d43ec2250a483a50", "5ea0abd2d43ec2250a483a43", "5ea0abd3d43ec2250a483a4b", "5ea0abd2d43ec2250a483a48", "5ea0abd4d43ec2250a483a5f", "5ea0abd2d43ec2250a483a41", "5ea0abd3d43ec2250a483a5c","5ea0abd3d43ec2250a483a4c", "5ea0abd3d43ec2250a483a5d", "5ea0abd3d43ec2250a483a56", "60901c5f2481a4362891d572", "5ea0abd3d43ec2250a483a51","5ea0abd2d43ec2250a483a47", "5ea0abd3d43ec2250a483a49", "5ea0abd3d43ec2250a483a4e", "5ea0abd3d43ec2250a483a54","5ea0abd3d43ec2250a483a59","5ea0abd4d43ec2250a483a63","5ea0abd2d43ec2250a483a46","5ea0abd3d43ec2250a483a55","5ea0abd4d43ec2250a483a60","5ea0abd3d43ec2250a483a53","5ea0abd3d43ec2250a483a57","5ea0abd3d43ec2250a483a4d","5ea0abd4d43ec2250a483a62", "5ea0abd3d43ec2250a483a52","5ea0abd3d43ec2250a483a5a", "5ea0abd3d43ec2250a483a5b", "5ea0abd4d43ec2250a483a5e", "5ea0abd1d43ec2250a483a3f","5ea0abd2d43ec2250a483a44","5ea0abd2d43ec2250a483a42","5ea0abd2d43ec2250a483a45","5ea0abd3d43ec2250a483a58"],"BrowserId":"85ae6fd573c1b94f1a6590acbcb9f3a7","IsGovernmentHospital":true,"IsPrivateHospital":true,"FacilityTypes":["CHO","CHC","CCC","ICCC"]}''', headers=headers)

#format api response for manipulation in python
hospital_json.encoding = 'utf-8-sig'
hospital_json = hospital_json.json()


#initialize final data output list
hospital_data = []

#get scrape time before looping
time_of_scraping = datetime.now(timezone)

#get response into list of dicts ready for saving to db or other 
for hospital in hospital_json['result']:
    
    #initialize dict for this hospital's data
    hosp_dict ={"LOCATION":{}}

    #get json response into easy to save to db format
    hosp_dict['DISTRICT'] = hospital['District']['Name']
    hosp_dict['NAME'] = hospital['Name']
    hosp_dict['LOCATION']['LATITUDE'] = hospital['Latitude']
    hosp_dict['LOCATION']['LONGITUDE'] = hospital['Longitude']
    hosp_dict['FACILITY TYPE'] = hospital['FacilityType']
    hosp_dict['LAST UPDATED'] = datetime.utcfromtimestamp(hospital['UpdatedDateTime'])
    hosp_dict['TOTAL BEDS'] = hospital['CovidBedDetails']['BedsAllotedForCovidTreatment']
    hosp_dict['VACANT BEDS'] = hospital['CovidBedDetails']['TotalVaccantBeds']
    hosp_dict['TOTAL ICU BEDS'] = hospital['CovidBedDetails']['AllotedICUBeds']
    hosp_dict['VACANT ICU BEDS'] = hospital['CovidBedDetails']['VaccantICUBeds']
    
    #some hospitals apparently do not have landline so:
    if hospital['Landline'] != '':
      hosp_dict['TELEPHONE'] = hospital['Landline']
    else:
      hosp_dict['TELEPHONE'] = hospital['MobileNumber']
    hosp_dict['SCRAPE TIME'] = time_of_scraping
    
    hospital_data.append(hosp_dict)


for i in hospital_data:
  print(i)
  print("   ")

print(len(hospital_data))

#output data in hospital_data
#as of 7/28/21 len should be 2014 (2014 total hospitals scraped)