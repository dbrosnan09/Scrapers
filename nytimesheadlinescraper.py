#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

from requests_html import HTMLSession

session = HTMLSession()

url = 'https://nytimes.com'
nytimes_content = session.get(url)
nytimes_soup = BeautifulSoup(nytimes_content.content,"html.parser")
nytimes_headlines = BeautifulSoup(nytimes_content.content,"html.parser").find_all("a"
)
#eliminate briefings from headlines
items=nytimes_soup.select('section[data-block-tracking-id="Briefings"] h2')

briefings = []
for i in items:
  a = str(i)
  b = a.find(">")
  c=a.find("</h2")
  nope = a[b:c]
  nope= nope[1:]
  briefings.append(nope)

#dummy briefings if briefings not present
if len(briefings) < 3:
  briefings = ["kldjflsjdfs", "khdskfjhaskdjf", "lhsdkfhasdkjfh"]


for i in nytimes_headlines:
    if '<h3' or '<h2' in str(i):
        print(i.get_text())
        print(i.get('href'))

#eliminate author and subtitle h2s
nyt_list = []
for i in nytimes_headlines:
    if '<h2' in str(i):
        if 'class="svelte-' not in str(i):
            interlist = []
            interlist.append(i.find('h2').get_text())
            interlist.append(i.get('href'))
            nyt_list.append(interlist)
    elif '<h3' in str(i):
        if "eog7260" in str(i):
            interlist = []
            interlist.append(i.findAll('h3')[1].get_text())
            interlist.append(i.get('href'))
            nyt_list.append(interlist)

        elif 'class="svelte-' not in str(i):
            interlist = []
            interlist.append(i.find('h3').get_text())
            interlist.append(i.get('href'))
            nyt_list.append(interlist)

for z in briefings:
    print(z)


final_nyt_list = []
for y in nyt_list:
    not_brief = True
    for z in briefings:
        if z in y[0]:
            not_brief = False
    if y[0] == 'Opinion':
        not_brief = False
    if y[0] == '':
        not_brief = False
    if not_brief:
        final_nyt_list.append(y)

for i in final_nyt_list:
    print(i)

for x in final_nyt_list:
    if 'https://www.nytimes.com' not in x[1]:
        x[1] = 'https://www.nytimes.com'+x[1]

for y in final_nyt_list:
    print(y)

nytimeslist = []
counter = 1
for y in final_nyt_list:
    interlist = [1]
    interlist.append(counter)
    counter += 1
    interlist.append(y[0])
    interlist.append(y[1])
    nytimeslist.append(interlist)

print(nytimeslist)
