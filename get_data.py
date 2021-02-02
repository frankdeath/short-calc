#!/usr/bin/env python3

# http://regsho.finra.org/CNMSshvol20210201.txt

import requests
import os
import time

from html.parser import HTMLParser

delay = 0.5

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

data_links = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        #print("attrs: ", attrs)
        if tag == 'a':
            attr = dict(attrs)
            if attr['href'] != None:
                #print(attr['href'])
                #http://www.finra.org/
                #http://regsho.finra.org/regsho-March.html
                #http://regsho.finra.org/regsho-April.html
                #http://regsho.finra.org/regsho-May.html
                #http://regsho.finra.org/regsho-June.html
                #http://regsho.finra.org/regsho-July.html
                #http://regsho.finra.org/regsho-August.html
                #http://regsho.finra.org/regsho-September.html
                #http://regsho.finra.org/regsho-October.html
                #http://regsho.finra.org/regsho-November.html
                #http://regsho.finra.org/regsho-December.html
                #http://regsho.finra.org/regsho-January.html
                #javascript:newWindow('http://regsho.finra.org/DailyShortSaleVolumeFileLayout.pdf');
                #http://regsho.finra.org/CNMSshvol20210201.txt
                #http://regsho.finra.org/FNQCshvol20210201.txt
                #http://regsho.finra.org/FNRAshvol20210201.txt
                #http://regsho.finra.org/FNSQshvol20210201.txt
                #http://regsho.finra.org/FNYXshvol20210201.txt
                #http://regsho.finra.org/FORFshvol20210201.txt
                #http://www.finra.org/privacy
                #http://www.finra.org/legal
                if 'CNMS' in attr['href']:
                    data_links.append(attr['href'])
    
    #def handle_endtag(self, tag):
    #    print("Encountered an end tag :", tag)

    #def handle_data(self, data):
    #    print("Encountered some data  :", data)

# 
index_url = 'http://regsho.finra.org/regsho-Index.html'
base_url = 'http://regsho.finra.org/regsho-'
url_suffix = '.html'

parser = MyHTMLParser()

if not os.path.isdir('data'):
    os.mkdir('data')

#if False:
for month in months:
    url = base_url + month + url_suffix
    print(url)
    
    page = requests.get(url)
    parser.feed(page.text)
    
    time.sleep(delay)

#page = requests.get(index_url)
# page.content is a binary string
# page.text is a string
# html_bytes = page.content
# html = html_bytes.decode("utf-8")
# print(page.text == html)
# print(page.text)
#parser.feed(page.text)

# print(data_links)

for data_link in data_links:
    filename = "data/{}".format(data_link.split('/')[3])
    if not os.path.isfile(filename):
        print("Downloading {}".format(filename))
        page = requests.get(data_link)
        with open(filename, 'wb') as f:
            f.write(page.content)
        time.sleep(delay)
    else:
        print("{} already exists".format(filename))
