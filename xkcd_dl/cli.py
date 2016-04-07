#!/usr/bin/env python3

'''
Run `xkcd-dl --update-db` if running for the first time.
Usage:
  xkcd-dl --update-db
  xkcd-dl --download-latest [--path=PATH]
  xkcd-dl --download=XKCDNUMBER [--path=PATH]
  xkcd-dl --download-all [--path=PATH]
  xkcd-dl --download-range <START> <END> [--path=PATH]
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
from os.path import expanduser, join
from os import getcwd

__author__ = "Tasdik Rahman (https://github.com/prodicus)"
__version__ = '0.0.6'

HOME = expanduser("~")       ## is cross platform. 'HOME' stores the path to the home directory for the current user
BASE_URL = 'http://xkcd.com'
ARCHIVE_URL='http://xkcd.com/archive/'
xkcd_dict_filename = '.xkcd_dict.json'
xkcd_dict_location = os.path.join(HOME, xkcd_dict_filename)
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))       ## returns the directory of this script
WORKING_DIRECTORY = os.getcwd()         ##returns the directory the terminal is currently in

arguments = docopt(__doc__, version=__version__)

#####  --download-all STARTS
def download_all():
    '''
    The command to download all the XKCD's and stores them in appropriate folders.
    '''
    json_content = read_dict()
    if json_content:
        print("Downloading all xkcd's Till date!!")
        all_keys = json_content.keys()
        for xkcd_number in all_keys:
            download_one(json_content, xkcd_number) 

#####  --download-all ENDS


#####  --download=XKCDNUMBER
def download_xkcd_number():
    '''
    The command for downloading one comic
    '''
    json_content = read_dict()
    if json_content:
        download_one(json_content, arguments['--download'])

#####  --download=XKCDNUMBER ends


#####  --download-range <START> <END>
def download_xkcd_range():
    '''
    The command for downloading a comic range
    '''
    start = int(arguments["<START>"])
    end = int(arguments["<END>"])

    json_content = read_dict()
    if json_content:
        if start > end:
            print("Start must be smaller than End.")
            return

        if is_valid_comic(start) and is_valid_comic(end):
            range_numbers = [x for x in range(start, end+1)]
            # 404 does not exist, so remove it from the range
            if start <= 404 <= end:
                range_numbers.remove(404) 
            for number in range_numbers:
               download_one(json_content, number) 
 
#####  --download-range <START> <END> ends


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
        alt = response_content['alt']

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
alt = {altText} \n""".format(
                    description=title, 
                    date=publishing_date, 
                    url=xkcd_url,
                    altText=alt
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
def make_keyvalue_list(xkcd_dict, xkcd_num, date, description):
    """
    Creates a list consisting of the date at which the xkcd was published (and) it's description with it
    eg : ['2007-1-24', 'The Problem with Wikipedia']
    After that it indexes this list with the corressponding xkcd number in the
    dictionary 'xkcd_dict'
    reference : http://stackoverflow.com/a/28897347/3834059
    """
    xkcd_number = xkcd_num              ## JSON cannot store integer values. Convert it to string if you want to store it 
    if xkcd_number != '472':         ## Refer [1]
        keyvalue_list = {}
        keyvalue_list['date-published'] = date
        keyvalue_list['description'] = description
        ### indexing it
        xkcd_dict[xkcd_number] = keyvalue_list

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
        
        ## dict where all the infomation will be stored
        xkcd_dict = dict()

        ## now get all the <a> tags under the div '<div class="box" id="middleContainer">' from the soup object 
        for data in archive_soup.find_all("div", {"id": "middleContainer"}):
            ## this gets all the contents inside "<div class="box" id="middleContainer">"
            ## now to get the individual links
            for alinks in data.find_all('a'):          ## tries to get all the <a> tags from the 'data' object
                href = alinks.get('href').strip("/")   ## the href stored is in form of eg: "/3/". So make it of form "3"
                date = alinks.get('title')
                description = alinks.contents[0]       
                make_keyvalue_list(xkcd_dict, href, date, description) 
                
        with open(xkcd_dict_location, 'w') as f:
            json.dump(xkcd_dict, f)
            print("XKCD link database updated\nStored it in '{file}'. You can start downloading your XKCD's!\nRun 'xkcd-dl --help' for more options".format(file=xkcd_dict_location))

    else:
        print('Something bad happened!')

#####  --update-db ends


##### Utility functions
def sanitize_description(desc):
    return ''.join([i for i in desc if i.isdigit() or i.isalpha()])

def is_valid_comic(num):
    '''
    True if the comic number is valid, i.e. 0 < num <= latest comic
    '''
    # This uses the internet, but it may be desireable 
    # to store the release numbers in the JSON as integers.
    # If that were so, it could just be max(json_content.keys())
    # and there would be no internet connection failure chance.
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
    '''
    True if the main dict has already been created.
    '''
    ## reference : http://stackoverflow.com/a/23177452/3834059
    if not os.path.isfile(xkcd_dict_location):
        print("XKCD list not created!Run \nxkcd-dl --update-db")
        return False
    return True


def read_dict():
    '''
    Return the dict() object representing the xkcd json information, or None
    if the xkcd json has not been retrieved yet.
    '''
    if dict_exists():
        with open(xkcd_dict_location, 'r') as f:
            file_content = f.readline()
            return json.loads(file_content)
    else:
        return None


def download_one(xkcd_dict, xkcd_num):
    '''
    Downloads the particular XKCD number and stores it in the current directory.
    If the comic has already been downloaded, it is not redownloaded.
    '''
    # ensure a string key
    xkcd_number = str(xkcd_num)
    if xkcd_number in xkcd_dict:
        date=xkcd_dict[xkcd_number]['date-published']
        description=xkcd_dict[xkcd_number]['description']

        new_description = sanitize_description(description)

        new_folder = '{current_directory}/xkcd_archive/{name}'.format(current_directory=WORKING_DIRECTORY, name=xkcd_number)

        to_download_single = "{base}/{xkcd_num}/".format(base=BASE_URL, xkcd_num=xkcd_number)
        print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
            img_url=to_download_single, 
            path=new_folder
            )
        )
        alt=requests.get(to_download_single+'info.0.json').json()['alt']
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
alt = {altText} \n""".format(description=description, date=date, url=to_download_single, altText=alt)
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

def set_custom_path():
    '''Changes the working directory path to a user-specified directory'''
    path_was_set = False
    if arguments["--path"] and os.path.isdir(arguments["--path"]):
        # If we didn't change the directory,
        # the user would only be able to use absolute paths
        # That is, --path=./anything would fail
        os.chdir(arguments["--path"])

        global WORKING_DIRECTORY #Only ever changed here. Works fine as global.
        WORKING_DIRECTORY = os.getcwd()
        path_was_set = True
    return path_was_set


##### Utility functions end
        

def main():
    '''
    xkcd-dl is a simple command line utility to download all the xkcd comics till date and store them
    in an orderly fashion
    '''
    if arguments['--update-db']:
        update_dict()

    if arguments['--path']:
        path_was_set = set_custom_path()
        if not path_was_set:
            print("The path could not be set. (The directory must exist. Was a directory name too long or null?)")
            return
    if arguments['--download-latest']:
        download_latest()
    elif arguments['--download']:
        download_xkcd_number()
    elif arguments['--download-range']:
        download_xkcd_range()
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
