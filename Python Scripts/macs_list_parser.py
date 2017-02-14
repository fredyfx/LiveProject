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
import web_crawler


def parse_for_json_ms(source,
                      destination,
                      job_id,
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
    :param job_id:
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
            elements = soup.select(job_id)
            new_id = ""
            try:
                new_id = str(elements[0].getText())
                new_id = new_id.strip()
            except IndexError as e:
                print("Index out of range for job ID.")
            finally:
                first = "Job ID"
                new_dict.update({first: new_id})

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
                new_location = str(elements[1].getText())
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
                new_hours = str(elements[4].getText())
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
                new_date = str(elements[2].getText())
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

            # create a json dump of the new dictionary, format it, print it to the console, and write it to destination
            new_object = json.dumps(new_dict, sort_keys=True, indent=4, separators=(',', ': '))
            print(new_object)
            dst.write(new_object + "\n")


def run_parser_for_macs_list(path):
    """
    Runs the parser for macs list with its specific logic. This function will have to be specifically adapted
    to your machine, so make sure you correct the paths as appropriate within the function.
    :param path:
    :return:
    """
    if os.path.exists(path) is True:
        # open the source file in read bytes mode and destination file in write byte mode
        with open(path, "rb") as src:
            # parse the source file into a bs4 object
            soup = BeautifulSoup(src, "lxml")
            elements = soup.select("item")

            for i in range(0, len(elements)):
                parse_for_json_ms("C:\\Users\Your\Path{}.html".format(i),
                                  "C:\\Users\Your\Path",
                                  "#none",
                                  ".titleContainer h1",
                                  ".titleContainer h2",
                                  ".whitebox-content h5",
                                  "#none",
                                  ".whitebox-content h5",
                                  "#none",
                                  ".whitebox-content h5",
                                  "#none",
                                  ".whitebox-content p a")


