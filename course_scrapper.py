"""
    Scrapper for Courses
    This module scraps course Data from Academic Calendar and writes it into a csv file. It also converts a CSV file
    with course data into course objects to use it for the rest of the project. We can specify which courses to scrap
    by changing the Courses To Scrap string.

    This file is Copyright(c) 2023 Mark Henein, Ege Sayin, Kelly Wong, and Joshiah Joseph
"""
import csv
import os
import re
from scrapy.crawler import CrawlerProcess
import bs4.element
import scrapy
from bs4 import BeautifulSoup as Soupy

from core_classes import Course

CSV_SPLIT_CHAR = "|"
LIST_SPLIT_CHAR = ","
COURSES_TO_SCRAP = {'CSC', 'MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1', 'MAT221H1', 'MAT223H1', 'MAT240H1',
                    'MAT235Y1', 'MAT237Y1', 'MAT257Y1', 'STA237H1', 'STA247H1', 'STA257H1'}


def categorize_courses(course_data: bs4.ResultSet, wanted_courses: set[str]) -> list[Course]:
    """
        This function takes a course data object which is a resul set from the webpage, and also a list of wanted
        courses which is to specify which courses we want to scrap from the webpage. After that, this function
        applies some filters to scrapped data to create course objects and then returns a list containing desired
        courses.
    """
    courses = []
    course_code_pattern = re.compile(r"[(" + str.join("|", COURSES_TO_SCRAP) + ")]+[0-9]+[A-Z]\d")
    for tag in course_data:
        course_title = tag.find(class_="views-field views-field-title").text.replace("\n", "")
        course_code = course_title.split(" ")[0]
        if any([str.__contains__(course_code, x) for x in wanted_courses]):
            try:
                body = tag.find(class_="views-field views-field-body").find(class_="field-content").find(
                    'p').getText().rstrip().replace("\n", "")
            except AttributeError:
                body = ""
            try:
                prerequisite = tag.find(class_="views-field views-field-field-prerequisite").contents[
                    1].text.rstrip().replace("\n", "")
                prerequisite = course_code_pattern.findall(prerequisite)
            except AttributeError:
                prerequisite = []
            try:
                recommended = tag.find(class_="views-field views-field-field-recommended").contents[
                    1].text.rstrip().replace("\n", "")
                recommended = course_code_pattern.findall(recommended)
            except AttributeError:
                recommended = []
            try:
                corequisite = tag.find(class_="views-field views-field-field-corequisite").contents[
                    1].text.rstrip().replace("\n", "")
                corequisite = course_code_pattern.findall(corequisite)
            except AttributeError:
                corequisite = []
            try:
                exclusion = tag.find(class_="views-field views-field-field-exclusion").contents[
                    1].text.rstrip().replace("\n", "")
                exclusion = course_code_pattern.findall(exclusion)
            except AttributeError:
                exclusion = []
            try:
                breadth_requirements_text = \
                    tag.find(class_="views-field views-field-field-breadth-requirements").contents[
                        1].text.rstrip().replace("\n", "")
                if str.__contains__(breadth_requirements_text, "1"):
                    breadth_requirements = 1
                elif str.__contains__(breadth_requirements_text, "2"):
                    breadth_requirements = 2
                elif str.__contains__(breadth_requirements_text, "3"):
                    breadth_requirements = 3
                elif str.__contains__(breadth_requirements_text, "4"):
                    breadth_requirements = 4
                elif str.__contains__(breadth_requirements_text, "5"):
                    breadth_requirements = 5
                else:
                    breadth_requirements = 0
            except AttributeError:
                breadth_requirements = 0
            course_object = Course(course_title=course_title, course_code=course_code, course_description=body,
                                   prerequisites=prerequisite, exclusion=exclusion, recommended=recommended,
                                   corequisite=corequisite, breadth_requirements=breadth_requirements)
            courses.append(course_object)
    return courses


def write_to_csv(courses: list[Course]) -> None:
    """
        This function creates a CSV file using a list of courses. The data follows the sturcuture:
        ["Course Code", "Course Title", "Course Description", "Prerequisites", "Exclusion", "Recommended", "Corequisite"
        ,"Breadth Requirement"] for columns.
    """
    if os.path.exists("CourseData.csv"):
        os.remove("CourseData.csv")
    course_file = open('CourseData.csv', mode='w', encoding="utf-8", newline="")
    course_writer = csv.writer(course_file, delimiter=CSV_SPLIT_CHAR, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    course_writer.writerow(
        ["Course Code", "Course Title", "Course Description", "Prerequisites", "Exclusion", "Recommended",
         "Corequisite", "Breadth Requirement"])
    for course in courses:
        course_writer.writerow([course.course_code, course.course_title, course.course_description,
                                LIST_SPLIT_CHAR.join(course.prerequisites), LIST_SPLIT_CHAR.join(course.exclusion),
                                LIST_SPLIT_CHAR.join(course.recommended), LIST_SPLIT_CHAR.join(course.corequisite),
                                course.breadth_requirements])
    course_file.close()


def read_from_csv(file_name: str) -> list[Course]:
    """
        This function creates a list of courses from the dataset. That dataset must follow the structure from the
        write_to_csv.
    """
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=CSV_SPLIT_CHAR)
        reader.__next__()
        course_so_far = []
        for row in reader:
            course = Course(course_code=row[0], course_title=row[1], course_description=row[2],
                            prerequisites=row[3].split(LIST_SPLIT_CHAR), exclusion=row[4].split(LIST_SPLIT_CHAR),
                            recommended=row[5].split(LIST_SPLIT_CHAR), corequisite=row[6].split(LIST_SPLIT_CHAR),
                            breadth_requirements=int(row[7]))
            course_so_far.append(course)
    return course_so_far


class CalendarSpider(scrapy.Spider):
    """
        This is a spider to perform scrapping on Course Calendar. It inherits from scrapy.spider class.
    """
    name = "CoursesSpider"

    def start_requests(self) -> list[scrapy.Request]:
        """
         It starts the request to the web page (Academic Calendar) and returns the result of the request. After that, it
         parses the request using Parse function
        """
        urls = [
            'https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug',
        ]
        requests = list()
        for url in urls:
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse(self, response: scrapy.http.response) -> None:
        """
            Parses given response from the request into a raw data format and sends the result to categorize_courses to
            clean and categorize raw data into a courses list and then return that list to write_to_csv to write a csv
            file using the categorized data.
        """
        soup = Soupy(response.text, "html.parser")
        calendar_content = soup.findAll(class_="no-break views-row")
        self.log(calendar_content)
        write_to_csv(categorize_courses(calendar_content, COURSES_TO_SCRAP))
        return None


if __name__ == '__main__':
    """Uncomment to Start Crawler to Scrap Data and create a csv file with scrapped course data"""
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(CalendarSpider)
    process.start()
