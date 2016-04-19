# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Author: Tasdik Rahman
# @Date:   2016-04-19 12:29:20
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-04-19 13:55:46
# @MIT License
# @http://tasdikrahman.me
# @https://github.com/prodicus

import argparse
from subprocess import call
import glob
import shutil
import json
import os
from os.path import expanduser, join
from os import getcwd

import magic
import requests
from bs4 import BeautifulSoup as bs4

from xkcd_dl.version import VERSION

__author__ = "Tasdik Rahman"
__email__ = "prodicus@outlook.com"
__version__ = VERSION


HOME = expanduser("~")
BASE_URL = 'http://xkcd.com'
ARCHIVE_URL='http://xkcd.com/archive/'
xkcd_dict_filename = '.xkcd_dict.json'
xkcd_dict_location = os.path.join(HOME, xkcd_dict_filename)
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) 
WORKING_DIRECTORY = os.getcwd()
excludeList = ['1350','1416','1525','1608','1416','1506','1446','1663' ]

def download_all():
    json_content = read_dict()
    if json_content:
        print("Downloading all xkcd's Till date!!")
        all_keys = json_content.keys()
        for xkcd_number in all_keys:
            download_one(json_content, xkcd_number) 

def download_xkcd_range(*something):
    if len(something) != 2:
        print("Exactly two values are required for this.")
    else:
        start, end = something

        json_content = read_dict()
        if json_content:
            if start > end:
                print("Start must be smaller than End.")
                return

            if is_valid_comic(start) and is_valid_comic(end):
                range_numbers = [x for x in range(start, end+1)]
                if start <= 404 <= end:
                    range_numbers.remove(404) 
                for number in range_numbers:
                   download_one(json_content, number) 
 
def download_latest():
    update_dict()
    url = 'https://www.xkcd.com/info.0.json'
    response = requests.get(url)
    response_content = response.json()
    xkcd_number = response_content['num']
    download_one(read_dict(), xkcd_number)

def make_keyvalue_list(xkcd_dict, xkcd_num, date, description):
    xkcd_number = xkcd_num
    keyvalue_list = {}
    keyvalue_list['date-published'] = date
    xkcd_dict[xkcd_number] = keyvalue_list
    if xkcd_number == '472':         ## Refer [1]
        keyvalue_list['description'] = "House of Pancakes"
    else:
        keyvalue_list['description'] = description

    '''
    [1] the description for XKCD number is 
    "<span style="color: #0000ED">House</span>". It's hard coded currently
    But it works.
    '''

def update_dict():
    archive_page = requests.get(ARCHIVE_URL)
    if archive_page.status_code == 200:
        page_content = archive_page.content
        archive_soup = bs4(page_content, 'html.parser') 
        xkcd_dict = dict()

        for data in archive_soup.find_all("div", {"id": "middleContainer"}):
            for alinks in data.find_all('a'):
                href = alinks.get('href').strip("/")
                date = alinks.get('title')
                description = alinks.contents[0]       
                make_keyvalue_list(xkcd_dict, href, date, description) 

        with open(xkcd_dict_location, 'w') as f:
            json.dump(xkcd_dict, f)
            print("XKCD link database updated\nStored it in '{file}'. You can start downloading your XKCD's!\nRun 'xkcd-dl --help' for more options".format(file=xkcd_dict_location)) 
    else:
        print('Something bad happened!')

def sanitize_description(desc):
    return ''.join([i for i in desc if i.isdigit() or i.isalpha()])

def is_valid_comic(num):
    url = 'https://www.xkcd.com/info.0.json'
    response = requests.get(url)
    if response.status_code == 200:
        response_content = response.json()
        latest_number = response_content["num"]

        if not 0 < num <= latest_number:
            print("XKCD is numbered from 0 to {}".format(latest_number))
            return False
        return True
    else:
        print("There was an internet connection error.")
        return False

def dict_exists():
    if not os.path.isfile(xkcd_dict_location):
        print("XKCD list not created!Run \nxkcd-dl --update-db")
        return False
    return True

def read_dict():
    if dict_exists():
        with open(xkcd_dict_location, 'r') as f:
            file_content = f.readline()
            return json.loads(file_content)
    else:
        return None

def download_one(xkcd_dict, xkcd_num):
    xkcd_number = str(xkcd_num)
    if xkcd_number in excludeList:
        downloadImage = False
        print("{num} is special. It does not have an image.".format(
            num=xkcd_number
            )
        )
        '''
        [2] Some comics are special and either don't have an image or have a dynamic one.
            The full list is the array excludeList and needs to be manually update upon release
            of such comic.
        '''
    else:
        downloadImage = True
    if xkcd_number in xkcd_dict:
        date=xkcd_dict[xkcd_number]['date-published']
        description=xkcd_dict[xkcd_number]['description']

        new_description = sanitize_description(description)

        new_folder = '{current_directory}/xkcd_archive/{name}'.format(
            current_directory=WORKING_DIRECTORY, 
            name=xkcd_number
        )

        to_download_single = "{base}/{xkcd_num}/".format(base=BASE_URL, xkcd_num=xkcd_number)
        print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
            img_url=to_download_single, 
            path=new_folder
            )
        )
        alt=requests.get(to_download_single+'info.0.json').json()['alt']
        if os.path.exists(new_folder): print("xkcd  number '{num}' has already been downloaded!".format(
            num=xkcd_number)
        )
        else:
            os.makedirs(new_folder)
            os.chdir(new_folder)
            with open('description.txt', 'w') as f:
                content = """title : {description}
date-publised: {date}
url: {url}
alt: {altText} \n""".format(description=description,
                            date=date, url=to_download_single, altText=alt
                            )
                f.write(content)

            image_page = requests.get(to_download_single, stream=True)
            if downloadImage:
                if image_page.status_code == 200:
                    image_page_content = image_page.content
                    image_page_content_soup = bs4(image_page_content, 'html.parser')

                    for data in image_page_content_soup.find_all("div", {"id": "comic"}):
                        for img_tag in data.find_all('img'):
                            img_link = img_tag.get('src')

                    complete_img_url = "http:{url}".format(url=img_link)

                    file_name = "{description}.jpg".format(description=new_description)
                    r = requests.get(complete_img_url, stream = True)
                    if r.status_code == 200:
                        with open(file_name, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    else:
                        printf("Error with connectivity. HTTP error {}".format(r.status_code))
                    magic_response = str(magic.from_file(file_name, mime=True))
                    if 'png' in magic_response:
                        os.rename(file_name, "{description}.png".format(
                            description=new_description)
                        )
                    elif 'jpeg' in magic_response:
                        os.rename(file_name, "{description}.jpeg".format(
                            description=new_description)
                        )

    else: 
        print("{} does not exist! Please try with a different option".format(xkcd_number))

def set_custom_path(custom_path):
    path_was_set = False
    if custom_path and os.path.isdir(custom_path):
        os.chdir(custom_path)

        global WORKING_DIRECTORY
        WORKING_DIRECTORY = os.getcwd()
        path_was_set = True
        print("Path is set to {}".format(WORKING_DIRECTORY))
    else:
        print("The path does not exist.")
    return path_was_set

def show_xkcd(num):
    download_one(read_dict(), num)
    path = '{current_directory}/xkcd_archive/{name}/'.format(
        current_directory=WORKING_DIRECTORY, 
        name=num
    )
    call(["cat", path + "description.txt"])
    #call(["feh", path])
    ## ''' Comment out the following block if you like to use feh
    # Or set default image viewer to feh.
    try:
        img_path = glob.glob(path + "*.jpeg")[0]
        call(["xdg-open", img_path])
    except IndexError:
        try: 
            img_path = glob.glob(path + "*.png")[0]
            call(["xdg-open", img_path])
        except IndexError:
            print("Dynamic comic. Please visit in browser.")
    ## '''

def main():
    args = parser.parse_args()
    if args.update_db:
        update_dict()
    elif args.download_latest:
        download_latest()
    elif args.download:
        download_one(read_dict(), args.download)
    elif args.download_all:
        download_all()
    elif args.download_range:
        download_xkcd_range(*args.download_range)
    elif args.show:
        show_xkcd(args.show)
    elif args.path:
        set_custom_path(args.path)
    else:
        parser.print_usage()

parser = argparse.ArgumentParser(prog='xkcd-dl', description='Run `xkcd-dl --update-db` if running for the first time.')
parser.add_argument('-u', '--update-db', action='store_true', help='Update the database')
parser.add_argument('-l', '--download-latest', action='store_true', help='Download most recent comic') 
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--download', help='Download specified comic by number', type=int, metavar='XKCD_NUM')
group.add_argument('-a', '--download-all', action='store_true', help='Download all comics')
parser.add_argument('-r', '--download-range', nargs='*', help='Download specified range', type=int) 
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
parser.add_argument('-P', '--path', help='set path')
parser.add_argument('-s', '--show', help='Show specified comic by number', type=int, metavar='XKCD_NUM')

if __name__ == '__main__':
    main()
