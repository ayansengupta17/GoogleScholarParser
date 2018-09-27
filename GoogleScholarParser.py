#!/usr/local/bin/python3
import datetime
from bs4 import BeautifulSoup
import urllib
import os
from os import listdir
from os.path import isfile, join
import time


def parse_info(soup):
    paper_box = soup.find_all('a', attrs={'class': 'gsc_a_at'})
    link = [paper['data-href'] for paper in paper_box]
    paper = [paper.text.strip() for paper in paper_box]
    author_box = soup.find_all('div', attrs={'class': 'gs_gray'})
    author = [author.text.strip() for author in author_box]
    # publish_box = soup.find_all('div', attrs={'class': 'gs_gray'})
    # publish = [publish.text.strip() for publish in publish_box]
    year_box = soup.find_all('span', attrs={'class': 'gsc_a_h gsc_a_hc gs_ibl'})
    year = [year.text.strip() for year in year_box]

    return paper, link, author, year


def create_publication(num, paper, link, author, year, name):

    base_url = 'https://scholar.google.co.in'
    with open('./md/'+name+'.md','w',encoding='utf-8') as f:
        print("file created")
        f.write("|Publication | year\n")
        f.write("|:-------------:|------:|\n")
        for i in range(num):
            f.write('|' + author.pop(0) + ', [' + paper.pop(0) + '](' + base_url+ link.pop(0) + '), *' + author.pop(0) + '* |' + year.pop(0) + '|\n')


def check_year(time_period, year_list):
    year = []
    for item in year_list:

        if int(item) in time_period:
            year.append(item)

    return year


def check_dates():

    mypath = './md/'
    # mdfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    time_stamps = [os.path.getmtime(mypath + f) for f in listdir(mypath) if isfile(join(mypath, f))]

    if len(time_stamps) == 0:
        return True
    if (time.time() - min(time_stamps)) > 7*24*60*60:
        return True
    else:
        return False


if __name__ == "__main__":

    if check_dates():
        # Author Name : uniqe user id from google scholar link
        author_dict = {'Debraj Chakraborty': 'j_oVo0gAAAAJ',
                 'Madhu Belur': 'YjwIVGQAAAAJ',
                }

        time_period = []
        current_year = datetime.datetime.now().year
        time_period.append(current_year)
        time_period.append(current_year - 1)

        for prof in author_dict:
            quote_page = 'https://scholar.google.co.in/citations?hl=en&user=' + author_dict[prof] + '&view_op=list_works&sortby=pubdate'

            page = urllib.request.urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            paper, link, author, year_list = parse_info(soup)
            year = check_year(time_period, year_list)
            num = len(year)

            create_publication(num, paper, link, author, year, str(prof))

    else:
        print("Already Cached")
