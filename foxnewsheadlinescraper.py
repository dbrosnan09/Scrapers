#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests


#soup it up
url = 'https://foxnews.com'
fn_content = requests.get(url)
fn_soup = BeautifulSoup(fn_content.content,"html.parser")
fn_main = fn_soup.find_all("main")
main = str(fn_main)
main_soup = BeautifulSoup(main, "html.parser")
main_h2 = main_soup.find_all("h2")




#create numbered list of headlines
counter = 0
dailyrank = 1
fnlist = []
for v in main_h2:


  interlist = [3]
  interlist.append(dailyrank)
  dailyrank += 1
  interlist.append(v.text.lstrip().rstrip())
  fnlist.append(interlist)


#extract urls part 1 -> cut off leading
h2_html = []
counter1 = 0
for v in main_h2:

  if "http" in str(v):
    a = str(v).index(">")
    h2_html.append(str(v)[a + 10:])
  else:
    h2_html.append(str(v)[a+12:])
  counter1 += 1

#extract urls part 2: find index of where to cut off trailing
link_end = []

for i in h2_html:
  link_end.append(str(i).index('>'))


#actually cut off trailing
link_rip = []
link_end_index = 0

for i in h2_html:
  a = link_end[link_end_index]
  link_rip.append(i[:a-1])
  link_end_index +=1

#combine headline list with urls
link_rip_index = 0
for i in fnlist:
  b = link_rip[link_rip_index]
  i.append(b)
  link_rip_index += 1
#final in fnlist