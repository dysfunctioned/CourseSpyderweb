# CSC111 Project Report: CourseSpyderweb

## Mark Henein, Ege Sayin, Kelly Wong, Joshiah Joseph

## Introduction

Our research question asks, ”How can we visualize relations between courses from the UofT Faculty of
Arts and Science Academic Calendar using directed graphs?”. When accessing the academic calendar, we
noticed the inconvenience of navigating back and forth between each page through the provided links to learn about
the required courses for each program. As a result, it is difficult for students to keep track of all the required
courses they need in one place, so the development of a virtual interface to display the relationships between these
courses (exclusion, prerequisites, etc.) would help students to visualize the ”paths” they can take. More specifically,
we will be creating an interactive directed graph displaying all CSC, MAT, and STA courses from the Computer Science
program in which data such as course requirements, minimum grades, and a credit count will be represented in the
nodes. In addition, users will be able select focuses within the Computer Science program to display the requirements
for completing the selected focus.

We decided on this particular research question after experiencing difficulties with determining which courses we
should take to complete certain programs or focuses. The UofT academic calendar often presents data in an indigestible 
form that many students find puzzling. By sorting this data into a directed graph, students could effectively
plan their future courses without the confusion of sorting through blocks of text. We hope that this project will have
some impact on the computer science community at UofT by providing a more comprehensible and user friendly
alternative to the academic calendar.

The dataset used to construct the graph is obtained by scraping the Computer Science academic calendar, a subsection 
of the Uoft Faculty of Arts and Science academic calendar, and filtered accordingly to generate a dataset of all
the necessary data for this project. The following columns in the provided csv file are used by our program (in order):
Course Code, Course Title, Course Description, Prerequisites, Exclusion, Recommended, Corequisite, Breadth.

## Computational Overview

Our project uses directed graphs to model a central part of the data. Each vertex in this graph represents a specific
CSC, MAT or STA course, while the edges represent the relationships between courses, indicating whether the connected 
course is a prerequisite, exclusion, corequisite or recommended. These asymmetrical relationships prompt the
need for a directed graph type, as connections between courses must be directional, and trees would be unsuitable
since courses must be able to connect with other courses at different depths.

core_classes.py contains three main classes that hold all the associated information for each course from the generated 
dataset. The Course class contains an instance attribute of either str, list[str] or int type to represent each
column from the dataset, while the Record class is responsible for documenting a student’s academic record for a
course resembling the style of UofT’s academic transcripts. Lastly, the Student class allows users to create a profile
unique to themselves, which contains their student identification and academic history. This enables users to record
the status of their current completed courses, and check for course/focus eligibility as well as plan out their future
course load.

The Program class creates links between the course code and the Course object by using a dictionary, in which
the course code is the key and the Course object is the corresponding value. Additionally, the Program class contains 
an instance attribute of the Student object type to record the students enrolled in the program. The main
methods in the Program class are responsible for constructing the directed graph with the provided information
by initializing the vertices representing the courses, and the edges representing the links between courses and their
prerequisites if applicable. Then, specific information pertaining to each student is updated and maintained through
the add_course_info and create_student_mapping functions. We have also implemented multiple algorithms using
extensive filtering to check whether a student is eligible to take a certain program or focus offered by the department
of Computer Science.

This project makes use of various different Python libraries and modules to collect and visualize data. First, our
program uses Scrapy, a web scraping framework, to extract course data (course codes, prerequisites, exclusions,
corequisites, minimum grade requirements) from the Arts and Sciences’ academic calendar, and sort out the information 
we have collected to create course objects. To obtain the dataset, the Spider class from Scrapy library is used in 
course_scrapper.py to compose the CalendarSpider class, which extracts data from the academic calendar by navigating 
specific links on its webpages. Then, this information is filtered by course code to contain only CSC, MAT and STA 
courses, and written to a new csv file for processing.

The Python library NetworkX is incorporated into this program to generate a visual model of the directed graph, and
illustrate the connections between the course objects as represented by edges and vertices respectively. NetworkX
is an appropriate library for visualizing this graph because it provides a large amount of customization, namely,
the ability to create directed graphs. visualize_graph from main.py employs the DiGraph class from the
NetworkX library to initialize a directed graph, and make related changes to the graph using the methods involving 
nodes, edges, and attributes included in the class. An important characteristic of the graph’s visualization is
the colour of the edges connecting the courses, which is a customizable feature enabled by NetworkX. Green edges
indicate that all prerequisites for the corresponding course have been fulfilled, while red edges represent unfulfilled
prerequisites. Additionally, this function computes the particular position of a vertex depending on its course level,
i.e. 300 and 400-level courses have two layers, and 100 and 200-level courses have one layer in the visualization.
On a further note, we have also used the matplotlib plotting library to display all the figures generated in the
Visualizegraph function.

## Program Instructions

1. (Optional) In the course_scrapper module, uncomment the lines in main body to start scrapping process. It
    would scrap the data from the webpage and create a dataset named ”CourseData.csv”. However, we already
    included that dataset in the project.
2. The main block of main.py includes the function call run_example(), which builds a directed graph using
    NetworkX and displays the graph on a Matplotlib window. In the given example, a graph is built using a
    student object with courses ’CSC110Y1’ and ’CSC111H1’ completed. The green arrows represent fulfilled
    prerequisites and the red arrows represent unfulfilled prerequisites.
    Note: please fullscreen the Matplotlib windows to accurately view each node.
3. For further testing, create your own student object and add courses to academichistory using the following functions:
    - check_eligibility_course: checks if the student is eligible to enroll in an input course based on their academic
   history.
    - add_course_info: adds a Record object to the student’s academic record. Raises a ValueError if the input course code
   is not in the dataset.

    Then, call run_example() using this student object.

4. In addition, we have provided a few helper functions which you may find useful:
    - check_eligibility_program and check_eligibility_focus: checks if the student is eligible to complete a
       computer science major/specialist/focus program based on their academic history.
    - get_requirements: return the student’s missing requirements needed to complete a program/focus.
    - get_FCE_count: calculates the total number of FCEs obtained by the student.


## References

“Computer Science Academic Calendar.” UofT Faculty of Arts and Science Academic Calendar, https://artsci.calendar.utoronto.ca/section/Computer-Science.

“Digraph-Directed Graphs with Self Loops.” NetworkX 3.0 Documentation, https://networkx.org/documentation/stable/reference/classes/digraph.html.

“Scrapy 2.8 Documentation.” Scrapy, 2 Feb. 2023, https://docs.scrapy.org/en/latest/.
