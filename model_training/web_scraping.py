#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""web scraping module for Dota classification app
"""


from icrawler.builtin import GoogleImageCrawler
import urllib
from bs4 import BeautifulSoup
import os
from shutil import copyfile
from PIL import Image


def scrapeheroes(url):
    # get url with heroes
    page =  urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page)
    table = soup.find('table', {'class': 'wikitable sortable'})
    rows = table.find_all('tr')
    heroes = []
    
    # parse heroes
    for row in rows:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        if len(cols) > 0:
            heroes.append(cols[0])
    return heroes

def scrape_hero_images(heroes):   
    for hero in heroes:
        google_crawler = GoogleImageCrawler(storage={'root_dir': ''.join(['hero_images\\', hero])})
        google_crawler.crawl(keyword=(hero , ' dota 2'), max_num=100)

def convert_images(image_width,data_path,data_dir_list,n_heroes):
    basewidth = image_width
    
    # convert all files for serving to jpg and resize them
    for dataset in data_dir_list[0:n_heroes]:
        img_list=os.listdir(data_path+'\\'+ dataset)
        im = Image.open(data_path+'\\'+ dataset+'\\'+ img_list[0])
        wpercent = (basewidth/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        im = im.resize((basewidth,hsize), Image.ANTIALIAS)
        rgb_im = im.convert('RGB')
        rgb_im.save(os.getcwd()+'\\heroes_for_serving\\'+dataset+".jpg")