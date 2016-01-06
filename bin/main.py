#!/usr/bin/env python3

r'''
Run `xkcd-dl --update-db` if running for the first time.

Usage:
  xkcd-dl --update-db
  xkcd-dl --download-latest
  xkcd-dl --download=XKCDNUMBER
  xkcd-dl --download-all
  xkcd-dl --version
  xkcd-dl (-h | --help)
Options:
  --update-db   Updates dictionary which stores all xkcd's till date
  -h --help     Show this screen
  -v --version  Show version 
'''

from docopt import docopt
from bs4 import BeautifulSoup as bs4
import urllib.request
import magic
import requests
import json
import os
from os.path import expanduser
from os import getcwd

__author__ = "Tasdik Rahman (https://github.com/prodicus)"
__version__ = '0.0.5'

HOME =expanduser("~")       ## is cross platform. 'HOME' stores the path to the home directory for the current user
BASE_URL = 'http://xkcd.com'
ARCHIVE_URL='http://xkcd.com/archive/'
XKCD_DICT = {}      
xkcd_dict_filename = '.xkcd_dict.json'
xkcd_dict_location = HOME + '/' + xkcd_dict_filename
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))       ## returns the directory of this script
WORKING_DIRECTORY = os.getcwd()         ##returns the directory the terminal is currently in

arguments = docopt(__doc__, version=__version__)

def sanitize_description(desc):
-    return ''.join([i for i in desc if i.isdigit() or i.isalpha()])

#####  --download-all STARTS

def download_all():
    '''
    Downloads all the XKCD's and stores them in apporopriate folders.
    If an XKCD has been already downloaded. It skips it!
    '''

    if not os.path.isfile(xkcd_dict_location):
        print("XKCD list not created!Run \nxkcd-dl --update-db")
    else: 
        ## load the json file
        print("Downloading all xkcd's Till date!!")
        with open(xkcd_dict_location, 'r') as f:
            file_content = f.readline()
            json_content = json.loads(file_content)
            """>>>print(type(json_content))
            <class 'dict'>
            """
            ## getting all the keys 
            all_keys = json_content.keys()
            for xkcd_number in all_keys:
              ## Nothing wrong with #1462. Ran it again and was successfully saved!
              #  if xkcd_number == '1462':      ## some issue downloading for #1462, will have to look into it
              #     continue        
                description = json_content[xkcd_number]['description']
                date_published=json_content[xkcd_number]['date-published']

                xkcd_url = "{base}/{xkcd_num}".format(base=BASE_URL, xkcd_num=xkcd_number)
                new_folder = '{current_directory}/xkcd_archive/{name}'.format(current_directory=WORKING_DIRECTORY, name=xkcd_number)
                new_description = sanitize_description(description)

                print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
                    img_url=xkcd_url, 
                    path=new_folder
                    )
                )
                ## check if the file exists
                if os.path.exists(new_folder):
                    print("xkcd  number '{num}' has already been downloaded!".format(num=xkcd_number))
                else:
                    os.makedirs(new_folder)
                    os.chdir(new_folder)
                    ## creating the description file inside this directory :
                    with open('description.txt', 'w') as f:
                        content = """title : {description}
date-publised: {date}
url = {url}
                        """.format(description=description, date=date_published, url=xkcd_url)
                        f.write(content)

                    ######################################
                    ##getting the image link from the page
                    image_page = requests.get(xkcd_url, stream=True)
                    if image_page.status_code == 200:
                        image_page_content = image_page.content
                        image_page_content_soup = bs4(image_page_content, 'html.parser')

                        for data in image_page_content_soup.find_all("div", {"id": "comic"}):
                            for img_tag in data.find_all('img'):
                                img_link = img_tag.get('src')
                        
                        complete_img_url = "http:{url}".format(url=img_link)

                        file_name = "{description}.jpg".format(description=new_description)
                        urllib.request.urlretrieve(complete_img_url, file_name)
                        magic_response = str(magic.from_file(file_name, mime=True))
                        if 'png' in magic_response:
                            os.rename(file_name, "{description}.png".format(description=new_description))
                        elif 'jpeg' in magic_response:
                            os.rename(file_name, "{description}.jpeg".format(description=new_description))
                        ## file storage successful

#####  --download-all ENDS

#####  --download-latest STARTS
def download_latest():
    '''
    gets the xkcd number of the last uploaded xkcd. Info got from 
    url = 'https://www.xkcd.com/info.0.json'
    ''' 
    url = 'https://www.xkcd.com/info.0.json'
    response = requests.get(url)
    if response.status_code == 200:
        response_content = response.json()

        xkcd_number = response_content['num']
        mon = response_content['month']
        year = response_content['year']
        date = response_content['day']
        publishing_date = "{date}-{month}-{year}".format(date=date, month=mon, year=year)

        title = response_content['title']
        stripped_title = title.replace(" ", "_").replace(":", "_").replace("/", "_").replace("*", "_").replace("$", "_").replace("@", "_")

        xkcd_url = "{base}/{xkcd_num}".format(base=BASE_URL, xkcd_num=xkcd_number)

        new_folder = '{current_directory}/xkcd_archive/{name}'.format(current_directory=WORKING_DIRECTORY, name=xkcd_number)

        if os.path.exists(new_folder):
            print("xkcd number : '{xkcd}'' has already been downloaded !".format(xkcd=xkcd_number))
        else:
            os.makedirs(new_folder)
            os.chdir(new_folder)
            ## creating the description file inside this directory :
            with open('description.txt', 'w') as f:
                content = """title : {description}
date-publised: {date}
url = {url}
                """.format(
                    description=title, 
                    date=publishing_date, 
                    url=xkcd_url
                )
                f.write(content)            

            ## Now to download the image file 
            img_raw_link = response_content['img']
            ## ^ has the string in the form of "http:\/\/imgs.xkcd.com\/comics\/flashlights.png"
            img_link = img_raw_link.replace("\/", "/")
            """>>>print(img_link)
            http://imgs.xkcd.com/comics/flashlights.png
            """
            print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
                                img_url=img_link, 
                                path=new_folder
                                )
            )
            file_name = img_link.split("/")[-1]
            urllib.request.urlretrieve(img_link, file_name)


#####  --download-latest ENDS

##### --update-db START
def make_keyvalue_list(xkcd_num, date, description):
    """
    Creates a list consisting of the date at which the xkcd was published (and) it's description with it
    eg : ['2007-1-24', 'The Problem with Wikipedia']

    After that it indexes this list with the corressponding xkcd number in the dictionary 'XKCD_DICT'
    reference : http://stackoverflow.com/a/28897347/3834059
    """
    xkcd_number = xkcd_num              ## JSON cannot store integer values. Convert it to string if you want to store it 
    if xkcd_number != '472':         ## Refer [1]
        keyvalue_list = {}
        keyvalue_list['date-published'] = date
        keyvalue_list['description'] = description
        ### indexing it
        XKCD_DICT[xkcd_number] = keyvalue_list

    '''
    [1] the description for XKCD number is "<span style="color: #0000ED">House</span>". Leaving it for this release
    '''

def update_dict():
    '''
    getting the info from the archive page. url="http://xkcd.com/archive/" 
    '''
    archive_page = requests.get(ARCHIVE_URL)
    if archive_page.status_code == 200:
        page_content = archive_page.content
        archive_soup = bs4(page_content, 'html.parser')

        ## now get all the <a> tags under the div '<div class="box" id="middleContainer">' from the soup object 
        for data in archive_soup.find_all("div", {"id": "middleContainer"}):
            ## this gets all the contents inside "<div class="box" id="middleContainer">"
            ## now to get the individual links
            for alinks in data.find_all('a'):          ## tries to get all the <a> tags from the 'data' object
                href = alinks.get('href').strip("/")   ## the href stored is in form of eg: "/3/". So make it of form "3"
                date = alinks.get('title')
                description = alinks.contents[0]       
                make_keyvalue_list(href, date, description) 
                
        with open(xkcd_dict_location, 'w') as f:
            json.dump(XKCD_DICT, f)
            print("XKCD link database updated\nStored it in '{file}'. You can start downloading your XKCD's!\nRun 'xkcd-dl --help' for more options".format(file=xkcd_dict_location))

    else:
        print('Something bad happened!')

#####  --update-db ends


#####  --download=XKCDNUMBER
def download_xkcd_number():
    '''Downloads the particular XKCD number and stores it in the current directory'''
    ## check if the main dict is empty. If yes, then prompt got updating 
    ## reference : http://stackoverflow.com/a/23177452/3834059

    xkcd_number = arguments['--download']

    if not os.path.isfile(xkcd_dict_location):
        print("XKCD list not created!Run \nxkcd-dl --update-db")
    else: 
        ## load the json file
        with open(xkcd_dict_location, 'r') as f:
            file_content = f.readline()
            json_content = json.loads(file_content)

            if xkcd_number in json_content:
                date=json_content[xkcd_number]['date-published']
                description=json_content[xkcd_number]['description']

                new_description = sanitize_description(description)

                new_folder = '{current_directory}/xkcd_archive/{name}'.format(current_directory=WORKING_DIRECTORY, name=xkcd_number)

                to_download_single = "{base}/{xkcd_num}/".format(base=BASE_URL, xkcd_num=xkcd_number)
                print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
                    img_url=to_download_single, 
                    path=new_folder
                    )
                )
                ## check if file already exists! i.e xkcd has been downloaded
                if os.path.exists(new_folder):
                    print("xkcd  number '{num}' has already been downloaded!".format(num=xkcd_number))
                else:
                    os.makedirs(new_folder)
                    os.chdir(new_folder)
                    ## creating the description file inside this directory :
                    with open('description.txt', 'w') as f:
                        content = """title : {description}
date-publised: {date}
url = {url}
                        """.format(description=description, date=date, url=to_download_single)
                        f.write(content)

                    ######################################
                    ##getting the image link from the page
                    image_page = requests.get(to_download_single, stream=True)
                    if image_page.status_code == 200:
                        image_page_content = image_page.content
                        image_page_content_soup = bs4(image_page_content, 'html.parser')

                        for data in image_page_content_soup.find_all("div", {"id": "comic"}):
                            for img_tag in data.find_all('img'):
                                img_link = img_tag.get('src')
                        
                        ## a sample 'img_link' is like '//imgs.xkcd.com/comics/familiar.jpg', so we need to add 
                        ### 'http:' to it
                        ## making a request for the image in question
                        complete_img_url = "http:{url}".format(url=img_link)

                        file_name = "{description}.jpg".format(description=new_description)
                        urllib.request.urlretrieve(complete_img_url, file_name)
                        ## now don't be fooled here by the .jpg extension here!
                        ## You would be surprised to find out that it may have a different file type. PNG for example per se.

                        ## using module 'python-magic' to detect the mime type of the file downloaded 
                        magic_response = str(magic.from_file(file_name, mime=True))
                        if 'png' in magic_response:
                            os.rename(file_name, "{description}.png".format(description=new_description))
                        elif 'jpeg' in magic_response:
                            os.rename(file_name, "{description}.jpeg".format(description=new_description))
                        ## file storage successful

            else: 
                print("{} does not exist! Please try with a different option".format(xkcd_number))
        
#####  --download=XKCDNUMBER ends


def main():
    '''
    xkcd-dl is a simple command line utility to download all the xkcd comics till date and store them
    in an orderly fashion
    '''
    if arguments['--update-db']:
        update_dict()
    elif arguments['--download-latest']:
        download_latest()
    elif arguments['--download']:
        download_xkcd_number()
    elif arguments['--download-all']:
        download_all()
    elif arguments['-h'] or arguments['--help']:
        print(__doc__)
    elif arguments['--version'] or arguments['-v']:
        print(__version__)
        print(__author__)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
