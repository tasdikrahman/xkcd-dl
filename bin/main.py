#!/usr/bin/env python

r'''
Usage:
  xkcd-cli --update-db
  xkcd-cli --download-latest
  xkcd-cli --download=XKCDNUMBER
  xkcd-cli --download-all
  xkcd-cli --version
  xkcd-cli (-h | --help)
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


__version__ = '0.0.1'


BASE_URL = 'http://xkcd.com'
ARCHIVE_URL='http://xkcd.com/archive/'
XKCD_DICT = {}      
xkcd_dict_filename = 'xkcd_dict.json'
DIRECTORY = os.path.dirname(os.path.abspath(__file__))      ## returns the directory of this script


arguments = docopt(__doc__, version=__version__)

#####  --download-all STARTS

def download_all():
    '''
    Downloads all the XKCD's and stores them in apporopriate folders.
    If an XKCD has been already downloaded. It skips it!
    '''
    pass

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
        ## Approach 1 : 
        # response_content = str(response.json()) 
        # json_data = json.dumps(response_content)
        """
        >>>print(type(json_data))
        <class 'str'>
        >>>print(json_data['num'])
        TypeError: string indices must be integers
        """
        ## Approach 2:
        ## Note : response.json() returns a dict object
        response_content = response.json()
        """
        >>>print(type(response_content))
        <class 'dict'>
        """
        xkcd_number = response_content['num']
        """
        >>>print(xkcd_number)
        1603
        """
        mon = response_content['month']
        year = response_content['year']
        date = response_content['day']
        publishing_date = "{date}-{month}-{year}".format(date=date, month=mon, year=year)

        title = response_content['title']
        stripped_title = title.replace(" ", "_").replace(":", "_")

        xkcd_url = "{base}/{xkcd_num}".format(base=BASE_URL, xkcd_num=xkcd_number)

        new_folder = 'data/{name}'.format(name=xkcd_number)

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

                ## cleaning description
                # description_1 = description.translate(None, "!@#$&*()+=~<>")
                make_keyvalue_list(href, date, description) 
                
                """>>>pprint(XKCD_DICT)
                {1: ['2006-1-1', 'Barrel - Part 1'],
                 2: ['2006-1-1', 'Petit Trees (sketch)'],
                 ......
                 ......
                 1603: ['2015-11-13', 'Flashlights']}
                """

        ## making a file in the current directory to store the dictionary in for later reference
        ## Will always update the dictionary file, even if the file exists. Will over-write for the 
        ## newest content
        with open(xkcd_dict_filename, 'w') as f:
            # f.write(str(XKCD_DICT))       ## will give error, as JSON wants double quotes instead of the single quotes which this
            ## method provides

            ## Making the JSON object and wrtintg it to "xkcd_dict.json"
            ## Reference : http://stackoverflow.com/a/23110401/3834059

            # json_data = json.dumps(XKCD_DICT)
            json.dump(XKCD_DICT, f)
            print("XKCD link database updated\nStored it in '{file}'. You can start downloading your XKCD's!\nRun 'xkcd-cli --help' for more options".format(file=xkcd_dict_filename))

    else:
        print('Something bad happened!')

#####  --update-db ends


#####  --download=XKCDNUMBER
def download_xkcd_number():
    '''Downloads the particular XKCD number and stores it in the current directory'''
    ## check if the main dict is empty. If yes, then prompt got updating 
    ## reference : http://stackoverflow.com/a/23177452/3834059

    xkcd_number = arguments['--download']

    if not os.path.isfile(xkcd_dict_filename):
        print("XKCD list not created!Run \nxkcd-cli --update-db")
    else: 
        ## load the json file
        with open(xkcd_dict_filename, 'r') as f:
            file_content = f.readline()
            json_content = json.loads(file_content)
            ## converting this to a dictionary  
            
            # print(json.dumps(json_content))       #FOR TESTING PURPOSE
            ## above print displays the whole of the JSON file

            ## checking if the requested xkcd exists in the keys 
            if xkcd_number in json_content:
                date=json_content[xkcd_number]['date-published']
                description=json_content[xkcd_number]['description']

                new_description = description.replace(" ","_").replace(":", "_")

                new_folder = 'data/{name}'.format(name=xkcd_number)

                to_download_single = "{base}/{xkcd_num}/".format(base=BASE_URL, xkcd_num=xkcd_number)
                print("Downloading xkcd from '{img_url}' and storing it under '{path}'".format(
                    img_url=to_download_single, 
                    path=new_folder
                    )
                )
                # print("XKCD number : {key} \ndate published : {date} \ndescription : {description} ".format(
                #         key=xkcd_number,
                #         date=json_content[xkcd_number]['date-published'],
                #         description=json_content[xkcd_number]['description']
                #      )
                # )

                '''
                TO-DO : Make an api for this print
                >>>xkcd-cli --download=3
                XKCD number : 3 
                date published : 2006-1-1 
                description : Island (sketch) 
                >>>

                '''
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

                    ## Approach1 : Was not being saved properly. Showed image size as 0 bytes
                    ## Ref : http://stackoverflow.com/a/13137873/3834059
                    # img_link_request = requests.get(complete_img_url)
                    # if img_link_request.status_code == 200:
                        # with open('{desc}.jpg'.format(desc= new_description),'wb') as f:
                        #     img_link_request.raw.decode_content=True       ## for images which are zipped 
                        #     shutil.copyfileobj(img_link_request.raw, f)


                    ## Approach2 : Using urllib
                    ##################################
                    ## now before saving this image, I have to check the image type. Whether it is a 
                    ## png, jpg, jpeg. Or else it will give me an encoding error when opening the file with
                    ## the wrong extension type.

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
    xkcd-cli is a simple command line utility to download all the xkcd comics till date and store them
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
    else:
        print(__doc__)

if __name__ == '__main__':
    main()