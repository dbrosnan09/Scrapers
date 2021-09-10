#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests


url = 'https://www.bbc.com/news'
bbc_content = requests.get(url)
bbc_soup = BeautifulSoup(bbc_content.content,"html.parser")
bbc_headlines = bbc_soup.findAll("h3")
counter = 0
dailyrank = 1
bbclist = []
vdoublecheck = []
for v in bbc_headlines:
  #eliminate recommended reading headlines
  if "gs-u-vh" not in str(v):
    if "BBC World News TV" or "BBC World Service" not in str(v):
      if v not in vdoublecheck:
        interlist = [2]
        interlist.append(dailyrank)
        dailyrank += 1
        interlist.append(v.text.lstrip().rstrip())
        bbclist.append(interlist)
        if v not in vdoublecheck:
          vdoublecheck.append(v)



bbc_hrefs_soup = bbc_soup.findAll("a")

hrefs = []

vadoublecheck = []
for v in bbc_hrefs_soup:
  #hrefs are relative so add in https
  if v not in vadoublecheck:
    if "<h3" in str(v):

      if "http" in v["href"]:

        hrefs.append(v['href'])
      else:
        hrefs.append("https://bbc.com" + v['href'])
  vadoublecheck.append(v)

dailyrank2 = 1
hrefsfinal = []
dailyrank2 = 1
for i in hrefs:
  interlist3 = []
  interlist3.append(dailyrank2)
  dailyrank2 += 1
  interlist3.append(i)
  hrefsfinal.append(interlist3)

counter4 = 0
for i in hrefsfinal:
    for y in bbclist:
      if i[0] == y[1]:
        bbclist[counter4].append(i[1])
        counter4 += 1

#GET RID OF BBC World News and Radio ads
for v in bbclist:
  if v[2] == "BBC World News TV":
    vindex = bbclist.index(v)
    bbclist.remove(v)
    for i in bbclist:
      if bbclist.index(i) >= vindex:
        i[1] -= 1

for v in bbclist:
  if v[2] == "BBC World Service Radio":
    vindex = bbclist.index(v)
    bbclist.remove(v)
    for i in bbclist:
      if bbclist.index(i) >= vindex:
        i[1] -= 1

#final in bbclist
print(bbclist)