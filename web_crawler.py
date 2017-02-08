"""
Author: Garrett Guevara
Written/Tested: Python 3.5.2
Purpose: Create a Web Crawler to Scrape Web Pages for Tech Academy Live Project

Required Modules: BeautifulSoup, os, webbrowser, and requests.
"""

from bs4 import BeautifulSoup
import os
import webbrowser
import requests


def open_browser(url):
    """
    Open a url with your primary browser.
    :param url: Web site url.
    :return:
    """
    webbrowser.open(url)



def download_website_data_as_html(url, path):
    """
    Use the requests library to download website data as an html file.
    :param url: Url with desired data.
    :param path: Where you would like to save the data.
    :return:
    """
    # run the http get request
    res = requests.get(url)
    # check the http status code and if it is a 404, break
    res.raise_for_status()

    # check if http status code is 200
    if res.status_code == requests.codes.ok:
        # if the destination path exists, delete it for fresh creation
        if os.path.exists(path) is True:
            os.remove(path)

        # write the file in byte chunks to preserve memory and efficiency
        with open(path, 'wb') as f:
            for chunk in res.iter_content(100000):
                f.write(chunk)
            print("Data was written successfully to {}.".format(path))


def unicode_to_txt_parser(path):
    """
    Converts and parses the unicode file that was created by download_website_data() to a basic txt file.
    :param path: File path
    :return:
    """
    # check if the file exists:
    if os.path.exists(path) is True:
        with open(path, 'r+') as f:
            try:
                # cast the unicode file to a string
                soup = str(f)

                # parse the soup file with bs4, lxml, and prettify it
                soup = BeautifulSoup(soup, "lxml").prettify()
                f.write(soup)
                print("Unicode file at {} was successfully interpreted and parsed.".format(path))
            except ValueError as e:
                print(e)


def filter_html_by_selector(source, destination, selector):
    """
    Parse an html file with the use of a CSS selector, then write that data to a destination file.
    :param source: Source file path.
    :param destination: Destination file path.
    :param selector: The CSS selector to filter by.
    :return:
    """
    # delete destination path for fresh creation
    if os.path.exists(destination) is True:
        os.remove(destination)

    if os.path.exists(source) is True:
        # open the source file in read bytes mode and destination file in write byte mode
        with open(source, "rb") as src, open(destination, 'wb') as dst:
            # parse the source file into a bs4 object
            soup = BeautifulSoup(src, "lxml")
            # get a list of bs4 objects by parsing soup
            elements = soup.select(selector)

            # iterate through the list of bs4 objects, encode them, and cast them a string to be written to dst
            for element in elements:
                data = str(element.getText() + "\n").encode()
                dst.write(data)

            """
            # if you want to get attributes, use this
            for i in range(0, len(elements)):
                data = str(elements[i].attrs).encode()
                dst.write(data)

            # if you want to get the information with tags included, use this
            for i in range(0, len(elements)):
                data = str(elements[i]).encode()
                dst.write(data)
            """


def scrape_pages_from_links(source, selector, rootpath, endpath):
    """
    Scrape the links from the source file, open each one, and save those files in new individual html files
    on your machine.
    :param source: Source URL or path
    :param selector: The CSS selector you would like to filter by. i.e. "a"
    :param rootpath: The root of the destination path to your new files. i.e. "User\Documents\"
    :param endpath: The name of the file, which a number will be appended to for separation. i.e. "MyWebPageLinkPage"
    :return:
    """
    if os.path.exists(source) is True:
        # open the source file in read bytes mode and destination file in write byte mode
        with open(source, "rb") as src:
            # parse the source file into a bs4 object
            soup = BeautifulSoup(src, "lxml")
            # get a list of bs4 objects by parsing soup
            elements = soup.select(selector)

            count = 0
            # iterate through the list of bs4 objects, encode them, and cast them a string to be written to dst
            for i in range(0, len(elements)):
                url = str(elements[i].getText())
                end = endpath + str(count) + ".html"
                fullpath = rootpath + end
                download_website_data_as_html(url, fullpath)
                count += 1

