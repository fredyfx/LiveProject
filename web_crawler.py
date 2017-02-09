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
import json


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
        with open(source, "rb") as src, open(destination, "wb") as dst:
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


def parse_for_json(source,
                   destination,
                   job_ID,
                   job_title,
                   company,
                   location,
                   salary,
                   hours,
                   experience,
                   date_posted,
                   languages_used,
                   application_link):
    """
    Create usable JSON from parsed data by searching for specific criteria. JSON will be defaulted to an empty string
    if there are no selectors available. Pass in "#none" for unknown selectors.
    :param source:
    :param destination:
    :param job_ID:
    :param job_title:
    :param company:
    :param location:
    :param salary:
    :param hours:
    :param experience:
    :param date_posted:
    :param languages_used:
    :param application_link:
    :return:
    """

    new_dict = {}

    if os.path.exists(source) is True:
        # open the source file in read bytes mode and destination file in write byte mode
        # open source in read byte mode and destination in append mode
        with open(source, "rb") as src, open(destination, "a") as dst:
            # parse the source file into a bs4 object
            soup = BeautifulSoup(src, "lxml")

            # parse for job_ID
            elements = soup.select(job_ID)
            new_ID = ""
            try:
                new_ID = str(elements[0].getText())
                new_ID = new_ID.strip()
            except IndexError as e:
                print("Index out of range for job ID.")
            finally:
                first = "Job ID"
                new_dict.update({first: new_ID})

            # parse for job_title
            elements = soup.select(job_title)
            new_title = ""
            try:
                new_title = str(elements[0].getText())
                new_title = new_title.strip()
            except IndexError as e:
                print("Index out of range for job title.")
            finally:
                first = "Job Title"
                new_dict.update({first: new_title})

            # parse for company
            elements = soup.select(company)
            new_company = ""
            try:
                new_company = str(elements[0].getText())
                new_company = new_company.strip()
            except IndexError as e:
                print("Index out of range for company.")
            finally:
                first = "Company"
                new_dict.update({first: new_company})

            # parse for location
            elements = soup.select(location)
            new_location = ""
            try:
                new_location = str(elements[0].getText())
                new_location = new_location.strip()
            except IndexError as e:
                print("Index out of range for location.")
            finally:
                first = "Location"
                new_dict.update({first: new_location})

            # parse for salary
            elements = soup.select(salary)
            new_salary = ""
            try:
                new_salary = str(elements[0].getText())
                new_salary = new_salary.strip()
            except IndexError as e:
                print("Index out of range for salary.")
            finally:
                first = "Salary"
                new_dict.update({first: new_salary})

            # parse for hours
            elements = soup.select(hours)
            new_hours = ""
            try:
                new_hours = str(elements[0].getText())
                new_hours = new_hours.strip()
            except IndexError as e:
                print("Index out of range for hours.")
            finally:
                first = "Hours"
                new_dict.update({first: new_hours})

            # parse for experience
            elements = soup.select(experience)
            new_experience = ""
            try:
                new_experience = str(elements[0].getText())
                new_experience = new_experience.strip()
            except IndexError as e:
                print("Index out of range for experience.")
            finally:
                first = "Experience"
                new_dict.update({first: new_experience})

            # parse for date posted
            elements = soup.select(date_posted)
            new_date = ""
            try:
                new_date = str(elements[0].getText())
                new_date = new_date.strip()
            except IndexError as e:
                print("Index out of range for date posted.")
            finally:
                first = "Date Posted"
                new_dict.update({first: new_date})

            # parse for languages used
            elements = soup.select(languages_used)
            new_langs = ""
            try:
                new_langs = str(elements[0].getText())
                new_langs = new_langs.strip()
            except IndexError as e:
                print("Index out of range for languages used.")
            finally:
                first = "Languages Used"
                new_dict.update({first: new_langs})

            # parse for application link
            elements = soup.select(application_link)
            new_app_link = ""
            try:
                new_app_link = str(elements[0].getText())
                new_app_link = new_app_link.strip()
            except IndexError as e:
                print("Index out of range for application link.")
            finally:
                first = "Application Link"
                new_dict.update({first: new_app_link})

            # crate a json dump of the new dictionary, format it, print it to the console, and write it to destination
            new_object = json.dumps(new_dict, sort_keys=True, indent=4, separators=(',', ': '))
            print(new_object)
            dst.write(new_object + "\n")

