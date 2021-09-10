#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import re
from datetime import datetime
import pytz
timezone = pytz.timezone("America/New_York")

#scraper for Bihar website: https://covid19health.bihar.gov.in/DailyDashboard/BedsOccupied

"""

output should be list of dictionaries, one for each hospital. format is :

{'DISTRICT': 'ARARIA', 'NAME': 'Govt. Polytechnic Araria Boys Hostel (Block-A)', 'LOCATION': {'LATTITUDE': 26.14689, 'LONGITUDE': 87.41251}, 'HOSPITAL TYPE': 'Other', 'FACILITY TYPE': 'DCHC', 'LAST UPDATED': datetime.datetime(2021, 7, 23, 13, 43, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>), 'TOTAL BEDS': 50, 'VACANT BEDS': 50, 'TOTAL ICU BEDS': 0, 'VACANT ICU BEDS': 0, 'TELEPHONE': 9431411845, 'SCRAPE TIME': datetime.datetime(2021, 7, 26, 17, 2, 29, 205004, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>)}

"""


#get html
session = HTMLSession()
url = 'https://covid19health.bihar.gov.in/DailyDashboard/BedsOccupied'
bihar_content = session.get(url)

#parse html
bihar_soup = BeautifulSoup(bihar_content.content,"html.parser")

#"bed-enough" "bed-more" "bed-less" are the css classes for rows in the list of hospital data....the below gets the html for each row of hospital data
hospitals = bihar_soup.find_all(True, {'class':['bed-enough', 'bed-more', 'bed-less']})

time_of_scraping = datetime.now(timezone)


#setting up list for the final output
hospital_data = []

#loop through each row and save data to dict 
for hospital in hospitals:
  #initialize dict for this hospital
  hosp_dict = {}
  
  #td tags hold each data point for each hospital
  #all_tds is all raw data points for a single hospital
  all_tds = hospital.find_all('td')
  
  #now must get raw data into dict that is ready for saving to a db
  """
  tds are ordered as below on website:

  added "complex" to data points that are not simple td tag text extraction:

  0 = district
  1 = location (lat and long); and hospital name (complex)
  2 = hospital type
  3 = facility type
  4 = last updated (in format Jun 10 2021 12:23PM) (complex)
  5 = total beds
  6 = vacant beds
  7 = total icu beds
  8 = vacant icu beds
  9 = telephone (complex)

  """

  #get tds into a dictionary that can be easily saved to database
  hosp_dict['DISTRICT'] = all_tds[0].text
  hosp_dict['NAME'] = all_tds[1].text.strip()

  #regex to get lattitude and longitude, which is contained in a href of td[1]
  loc_link = all_tds[1].find("a", href=True)
  loc_link = loc_link['href']
  latregex =r"lat=([0-9.]*)"
  longregex = r"lon=([0-9.]*)"
  lat = re.search(latregex, loc_link)
  long = re.search(longregex, loc_link)
  lat = lat.group(1)
  long = long.group(1)


  hosp_dict['LOCATION'] = {}
  
  #some hospitals do not have long and lat information...for them empty dict, otherwise: 
  if lat != "0":
    hosp_dict['LOCATION']['LATTITUDE'] = float(lat)
  if long != "0":
    hosp_dict['LOCATION']['LONGITUDE'] = float(long)
  
  
  hosp_dict['HOSPITAL TYPE'] = all_tds[2].text  
  hosp_dict['FACILITY TYPE'] = all_tds[3].text
  
  #get 'last updated' into standardized datetime format
  last_updated = datetime.strptime(str(all_tds[4].text), '%b %d %Y %I:%M%p')
  #add timezone information to datetime 
  last_updated = timezone.localize(last_updated)
  hosp_dict['LAST UPDATED'] = last_updated
  
  hosp_dict['TOTAL BEDS'] = int(all_tds[5].text)
  hosp_dict['VACANT BEDS'] = int(all_tds[6].text)
  hosp_dict['TOTAL ICU BEDS'] = int(all_tds[7].text)
  hosp_dict['VACANT ICU BEDS'] = int(all_tds[8].text)
  hosp_dict['TELEPHONE'] = int(all_tds[9].text)
  
  #add the time when scraped to the hopsital dict
  hosp_dict['SCRAPE TIME'] = time_of_scraping
  
  #add this hospital's data to the master hospital list before looping 
  hospital_data.append(hosp_dict)

#final data is stored in a list of dictionaries called hospital_data
print(hospital_data)
print(len(hospital_data))