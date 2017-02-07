"""
Author: Garrett Guevara
Written/Tested: Python 3.5.2
Purpose: Scrape Web Content for Tech Academy Live Project

Required Modules: BeautifulSoup4, urllib, lxml, os
"""

from bs4 import BeautifulSoup
import urllib.request
import os
import unicodedata
import xml.etree.ElementTree as ET


def write_web_data_to_file(path, url):
    """
    Write a website's html to a file in your machine.
    :param path: File path you would like to use.
    :param url: URL you would like to get data from
    """

    # if the file exists, delete it
    if os.path.exists(path) is True:
        os.remove(path)

    # open the file in write mode
    f = open(path, 'w')
    # get website data
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "lxml")
    # format it and write it to a file
    try:
        f.write(soup.prettify())
        print("The file was created successfully.")
    except UnicodeEncodeError as e:
        print(e)
    finally:
        if(os.path.getsize(path) is 0):
            # convert the beautifulsoup object to unicode and ignore its errors
            soup = unicodedata.normalize('NFKC', soup.decode()).encode('ascii', 'ignore')
            # cast the unicode as a string
            soup_string = str(soup)
            f.write(soup_string)
            print("\n\nThe txt was file written without being formatted.")
        f.close()

def get_raw_data(url):
    """
    Create an html parsed string from a url.
    :param url: URL you would like to get data from.
    :return: soup object
    """
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "lxml")
    return soup

def title_filter(source, destination):
    """
    Parse an xml file into JSON.
    :param source: Source file path.
    :param destination: Destination file path.
    :return:
    """
    # open source and destination files
    source = open(source, 'r')
    destination = open(destination, 'w')

    # filter for title
    soup = BeautifulSoup(source, "lxml").prettify()
    root = ET.fromstring(soup)

    # print for testing
    for value in root.findall("./body/rss/channel/item"):
        title = value.find('title').text
        link = value.find('guid').text
        print("\"title\" :", "\"" + title.strip() + "\"",
              "\n\"link\" :", "\"" + link.strip() + "\""
              )

    # close both source and destination
    source.close()
    destination.close()


