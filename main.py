"""
    CSC111 Project: Main functions

    This python module contains the main program class and the main functions
    that make up the bulk of the testing and visualizing part of the project.
    Refer to each function's docstring for more detailed information on each
    of the functions and its purpose.


    This file is Copyright(c) 2023 Mark Henein, Ege Sayin, Kelly Wong, and Joshiah Joseph
"""
from dataclasses import dataclass
import core_classes as cc
import course_scrapper
import networkx as nx
import matplotlib.pyplot as plt


@dataclass
class Program:
    """
        The main graph representing courses in the CS program.

        Instance Atrributes:
        - courses: A dictionary mapping course code to Course object
        - student: A Student object

        Representation Invariants:
        - courses != {}
    """
    courses: dict[str, cc.Course]
    student: cc.Student

    def create_graph(self, g: nx.DiGraph) -> None:
        """
            Builds a directed graph from student data and course data. The nodes of the graph represent courses
            while the edges represent prerequisites.

            Edges are coloured red if the prerequisites are not met, and coloured green if they are met.
        """
        for course in self.courses:
            if course[:3] == 'CSC':
                g.add_node(course)
        to_remove = ['CSC110Y1', 'CSC111H1', 'CSC108H1', 'CSC148H1', 'CSC165H1', 'CSC399Y1', 'CSC399H1', 'CSC398Y0',
                     'CSC398H0', 'CSC396Y0', 'CSC495H1', 'CSC494Y1', 'CSC494H1', 'CSC491H1', 'CSC490H1', 'CSC199H1',
                     'CSC197H1', 'CSC196H1']
        g.remove_nodes_from(to_remove)
        g.add_node('(CSC110Y1, CSC111H1)/\n(CSC108H1, CSC148H1, CSC165H1)')

        prereq_courses = ['(MAT135H1, MAT136H1)/\nMAT137Y1/MAT157Y1', 'MAT221H1/MAT223H1/\nMAT240H1',
                          'MAT235Y1/MAT237Y1/\nMAT257Y1', 'STA237H1/STA247H1/\nSTA255H1/STA257H1']
        for course in prereq_courses:
            if course == '(MAT135H1, MAT136H1)/\nMAT137Y1/MAT157Y1':
                g.add_node(course)
            else:
                g.add_node(course)

        courses_taken = create_student_mapping(self.student)
        edges = get_edges(self.courses, courses_taken, g)
        for edge in edges:
            if nx.node_connectivity(g, edge[1], edge[0]) == 0:
                g.add_edge(edge[1], edge[0], color=edges[edge])


def get_edges(courses: dict[str, cc.Course], student_data: dict[str, cc.Record], g: nx.DiGraph) \
        -> dict[tuple[str, str], str]:
    """
        Returns a dictionary mapping edges with their corresponding relationship.

        Each tuple key has a str value indicating whether the colour of the edge should be red or green.
        Red edges represent unfulfilled prerequisites, while green edges represent fulfilled prerequisites.

        Preconditions:
        - courses != {}
        - student_data != {}
    """
    edges = {}
    for course in g.nodes():

        if course in ['(CSC110Y1, CSC111H1)/\n(CSC108H1, CSC148H1, CSC165H1)',
                      '(MAT135H1, MAT136H1)/\nMAT137Y1/MAT157Y1', 'MAT221H1/MAT223H1/\nMAT240H1']:
            prerequisites = []
        elif course in ['MAT235Y1/MAT237Y1/\nMAT257Y1']:
            prerequisites = ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']
        elif course in ['STA237H1/STA247H1/\nSTA255H1/STA257H1']:
            prerequisites = ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']
        else:
            prerequisites = courses[course].prerequisites

        for prerequisite in prerequisites:
            if prerequisite in g.nodes or prerequisite in ['CSC110Y1', 'CSC111H1', 'CSC108H1', 'CSC148H1', 'CSC165H1',
                                                           'MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1',
                                                           'MAT221H1', 'MAT223H1', 'MAT240H1',
                                                           'STA237H1', 'STA247H1', 'STA255H1', 'STA257H1']:

                if prerequisite in ['CSC110Y1', 'CSC111H1', 'CSC108H1', 'CSC148H1', 'CSC165H1']:
                    to_add = '(CSC110Y1, CSC111H1)/\n(CSC108H1, CSC148H1, CSC165H1)'
                elif prerequisite in ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']:
                    to_add = '(MAT135H1, MAT136H1)/\nMAT137Y1/MAT157Y1'
                elif prerequisite in ['MAT221H1', 'MAT223H1', 'MAT240H1']:
                    to_add = 'MAT221H1/MAT223H1/\nMAT240H1'
                elif prerequisite in ['MAT235Y1', 'MAT237Y1', 'MAT257Y1']:
                    to_add = 'MAT235Y1/MAT237Y1/\nMAT257Y1'
                elif prerequisite in ['STA237H1', 'STA247H1', 'STA255H1', 'STA257H1']:
                    to_add = 'STA237H1/STA247H1/\nSTA255H1/STA257H1'
                else:
                    to_add = prerequisite

                if (prerequisite in student_data) and (student_data[prerequisite].grade >= 50.0):
                    edges[(course, to_add)] = 'g'
                elif (prerequisite in ['CSC110Y1', 'CSC111H1', 'CSC108H1', 'CSC148H1', 'CSC165H1']) \
                        and (('CSC110Y1' in student_data and 'CSC111H1' in student_data)
                             or 'CSC108H1' and 'CSC148H1' and 'CSC165H1' in student_data):
                    edges[(course, to_add)] = 'g'
                elif (prerequisite in ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']) \
                        and (('MAT135H1' in student_data and 'MAT136H1' in student_data)
                             or ('MAT137Y1' in student_data) or ('MAT157Y1' in student_data)):
                    edges[(course, to_add)] = 'g'
                elif (prerequisite in ['MAT221H1', 'MAT223H1', 'MAT240H1']) \
                        and (('MAT221H1' in student_data) or ('MAT223H1' in student_data)
                             or ('MAT240H1' in student_data)):
                    edges[(course, to_add)] = 'g'
                elif (prerequisite in ['MAT235Y1', 'MAT237Y1', 'MAT257Y1']) \
                        and (('MAT235Y1' in student_data) or ('MAT237Y1' in student_data)
                             or ('MAT257Y1' in student_data)):
                    edges[(course, to_add)] = 'g'
                elif (prerequisite in ['STA237H1', 'STA247H1', 'STA255H1', 'STA257H1']) \
                        and (('STA237H1' in student_data) or ('STA247H1' in student_data)
                             or ('STA255H1' in student_data) or ('STA257H1' in student_data)):
                    edges[(course, to_add)] = 'g'
                else:
                    edges[(course, to_add)] = 'r'

    return edges


def create_course_mapping(lst: list) -> dict[str, cc.Course]:
    """
        Creates a dictionary mapping course codes to Course objects.

        Preconditions:
        - lst != []
    """
    courses = {}
    for course in lst:
        courses[course.course_code] = course
    return courses


def add_course_info(student: cc.Student, course: str, grade: int, weight: float) -> None:
    """
        Adds a Record object to the student's academic record. Raises a ValueError if the input course code is not in
        the dataset.

        Preconditions:
        - course != ''
        - 0 <= grade <= 100
    """
    if course not in course_data:
        raise ValueError
    record = cc.Record(course_data[course], grade, weight)
    student.academic_history.append(record)


def create_student_mapping(student: cc.Student) -> dict[str, cc.Record]:
    """
        Creates a dictionary mapping the student's completed course code to their record for that course.
    """
    course_mapping = {}
    for record in student.academic_history:
        course_mapping[record.course_taken.course_code] = record
    return course_mapping


def visualize_graph(g: nx.DiGraph) -> None:
    """
        Visualizes the directed graph. Nodes represent courses and edges represent prerequsites.
        Green edges represent fulfilled prerequisites and red edges represent unfulfilled prerequisites.
        Calculates the positions of course nodes based on the course's level.
        300 and 400 level courses each have 2 layers, while 100 and 200 level courses each have 1 layer.

        Note: please fullscreen the Matplotlib window.
    """
    pos = {}
    count2, count3, count3_2, count4, count4_2 = 0, 0, 0, 0, 0
    for node in g.nodes():
        if node[3] == '2':
            count2 += 1
        elif node[3:5] == '30' or node[3:5] == '31':
            count3 += 1
        elif node[3] == '3':
            count3_2 += 1
        elif node[3:5] == '40' or node[3:5] == '41' or node[3:5] == '42' or node[3:5] == '43' or node[3:5] == '44':
            count4 += 1
        elif node[3:5] == '45' or node[3:5] == '46' or node[3:5] == '47' or node[3:5] == '48' or node[3:5] == '49':
            count4_2 += 1

    counter2, counter3, counter3_2, counter4, counter4_2 = 0, 0, 0, 0, 0
    pos['(CSC110Y1, CSC111H1)/\n(CSC108H1, CSC148H1, CSC165H1)'] = (0.25, 1)
    pos['(MAT135H1, MAT136H1)/\nMAT137Y1/MAT157Y1'] = (0.75, 1)
    pos['CSC104H1'] = (1, 1)
    pos['CSC120H1'] = (0.9, 1)

    for node in g.nodes():
        if node[3] == '2':
            pos[node] = ((1 / count2) * (counter2 + 0.5), 0.8)
            counter2 += 1
        elif node[3:5] == '30' or node[3:5] == '31':
            pos[node] = ((1 / count3) * (counter3 + 0.5), 0.6)
            counter3 += 1
        elif node[3] == '3':
            pos[node] = ((1 / count3_2) * (counter3_2 + 0.5), 0.4)
            counter3_2 += 1
        elif node[3:5] == '40' or node[3:5] == '41' or node[3:5] == '42' or node[3:5] == '43' or node[3:5] == '44':
            pos[node] = ((1 / count4) * (counter4 + 0.5), 0.2)
            counter4 += 1
        elif node[3:5] == '45' or node[3:5] == '46' or node[3:5] == '47' or node[3:5] == '48' or node[3:5] == '49':
            pos[node] = ((1 / count4_2) * (counter4_2 + 0.5), 0)
            counter4_2 += 1

    colors = [g[u][v]['color'] for u, v in g.edges()]

    nx.draw_networkx_nodes(g, pos, node_size=600)
    nx.draw_networkx_labels(g, pos, font_size=5.4)
    nx.draw_networkx_edges(g, pos, arrows=True, edge_color=colors)

    plt.show()


def check_eligibility_course(course: str, student: cc.Student) -> bool:
    """
        Checks if a given student is eligible to take an input course.

        Note: grouped courses (e.g ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']) can satisfy prerequisites if
        the student completed one prerequisite in the group.
    """
    if course not in course_data:
        raise ValueError
    else:
        courses = create_student_mapping(student)
        courses_trimmed = [x[:6] for x in courses]
        prerequisites = course_data[course].prerequisites

        for prerequisite in prerequisites:
            if (prerequisite == '') or (prerequisite[:6] in courses_trimmed):
                ...
            elif prerequisite in ['CSC110Y1', 'CSC111H1', 'CSC108H1', 'CSC148H1', 'CSC165H1']:
                if not ('CSC110Y1' in courses and 'CSC111H1' in courses) and \
                        not ('CSC108H1' in courses and 'CSC148H1' in courses and 'CSC165H1' in courses):
                    return False
            elif prerequisite in ['MAT135H1', 'MAT136H1', 'MAT137Y1', 'MAT157Y1']:
                if not (('MAT135H1' in courses) and ('MAT136H1' in courses)) and \
                        not (('MAT137Y1' in courses) or ('MAT157Y1' in courses)):
                    return False
            elif prerequisite in ['MAT221H1', 'MAT223H1', 'MAT240H1']:
                if not (any(x in courses for x in ['MAT221H1', 'MAT223H1', 'MAT240H1'])):
                    return False
            elif prerequisite in ['MAT235Y1', 'MAT237Y1', 'MAT257Y1']:
                if not (any(x in courses for x in ['MAT235Y1', 'MAT237Y1', 'MAT257Y1'])):
                    return False
            elif prerequisite in ['STA237H1', 'STA247H1', 'STA255H1', 'STA257H1']:
                if not (any(x in courses for x in ['STA237H1', 'STA247H1', 'STA255H1', 'STA257H1'])):
                    return False
            elif prerequisite in ['CSC236H1', 'CSC240H1']:
                if not (any(x in courses for x in ['CSC236H1', 'CSC240H1'])):
                    return False
            elif prerequisite in ['CSC263H1', 'CSC265H1']:
                if not (any(x in courses for x in ['CSC263H1', 'CSC265H1'])):
                    return False
        return True


def get_FCE_count(student: cc.Student) -> float:
    """
        Returns the total number of full course equivalents(FCE's) obtained by a student using their
        academic history
    """
    fce_so_far = 0
    for course in student.academic_history:
        if course.course_taken.course_code[6] == 'H':
            fce_so_far += 0.5
        else:
            fce_so_far += 1
    return fce_so_far


def check_eligibility_program(degree: str, student: cc.Student) -> bool:
    """
        Checks whether a student has completed all the requirements for the computer science major or specialist program
        depending on which is specified, returning true if they are eligible and false if they are missing requirements.
        (The checks are done thorugh if statements representing each year)
        Preconditions:
        - degree == 'major' or degree == 'specialist'
    """
    s_c = []  # s_c is student courses
    for course in student.academic_history:
        s_c.append(course.course_taken.course_code)
    if degree == 'major':
        if not ((('CSC108H1' in s_c and 'CSC148H1' in s_c and ('CSC165H1' in s_c or 'CSC240H1' in s_c)) or (
                'CSC110Y1' in s_c and 'CSC111H1' in s_c)) and (
                        'Mat137Y1' in s_c or 'MAT157Y1' in s_c or ('Mat135H1 in s_c' and 'MAT136H1' in s_c))):
            return False
        elif not ('CSC207H1' in s_c and ('CSC236H1' in s_c or 'CSC240H1' in s_c) and 'CSC258H1' in s_c and (
                'CSC263H1' in s_c or 'CSC265H1' in s_c) and (
                          'STA247H1' in s_c or 'STA237H1' in s_c or 'STA255H1' in s_c or 'STA257H1' in s_c)):
            return False
        later_year_credits = 0
        for course in s_c:
            if course[:4] == 'CSC2' or course[:4] == 'CSC3' or course[:4] == 'CSC4' or course == 'MAT223H1' \
                    or course == 'MAT240H1' or course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' or \
                    course == 'STA414H1' or ((course[:4] == 'MAT3' or course[:4] == 'MAT4') and course not in
                                             {'MAT329Y1', 'MAT390H1', 'MAT391H1'}):
                if course[6] == 'H':
                    later_year_credits += 0.5
                else:
                    later_year_credits += 1.0
        if not (later_year_credits >= 3.0 and any(course[:4] == 'CSC4' for course in s_c) and any(
                course[3] == '4' for course in s_c) and any(
            course == 'MAT223H1' or course == 'MAT240H1' for course in s_c) and
                any(course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in s_c)):
            return False
        return True
    else:
        if not ((('CSC108H1' in s_c and 'CSC148H1' in s_c and ('CSC165H1' in s_c or 'CSC240H1' in s_c)) or (
                'CSC110Y1' in s_c and 'CSC111H1 in s_c')) and (
                        'Mat137Y1' in s_c or 'MAT157Y1' in s_c or ('Mat135H1' in s_c and 'MAT136H1' in s_c))):
            return False
        elif not ('CSC207H1' in s_c and 'CSC209H1' in s_c and (
                'CSC236H1' in s_c or 'CSC240H1' in s_c) and 'CSC258H1' in s_c and (
                          'CSC263H1' in s_c or 'CSC265H1' in s_c) and ('MAT223H1' in s_c or 'MAT240H1' in s_c) and (
                          'STA247H1' in s_c or 'STA237H1' in s_c or 'STA255H1' in s_c or 'STA257H1' in s_c)):
            return False
        later_year_credits = 0
        csc_4_credits = 0
        mat_sta_credits = 0
        for course in s_c:
            if course[:4] == 'CSC3' or course == 'CSC369H1' or course == 'CSC373H1' or \
                    course[:4] == 'CSC4' or course == 'MAT224H1' or course == 'MAT247H1' or course == 'MAT235Y1' or \
                    course == 'MAT237Y1' or course == 'MAT257Y1' or course == 'STA248H1' or course == 'STA238H1' or \
                    course == 'STA261H1' or course[:4] == 'STA3' or course[:4] == 'STA4' or \
                    ((course[:4] == 'MAT3' or course[:4] == 'MAT4') and course not in
                     {'MAT329Y1', 'MAT390H1', 'MAT391H1'}):
                if course[6] == 'H':
                    later_year_credits += 0.5
                else:
                    later_year_credits += 1.0
                if course[:4] == 'CSC4':
                    if course[6] == 'H':
                        csc_4_credits += 0.5
                    else:
                        csc_4_credits += 1.0
                if course[:3] == 'MAT' or course[:3] == 'STA':
                    if course[6] == 'H':
                        mat_sta_credits += 0.5
                    else:
                        mat_sta_credits += 1.0
        if not (later_year_credits >= 6.0 and any(
                course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in
                s_c) and csc_4_credits >= 1.5 and (later_year_credits - mat_sta_credits) >= 4.0):
            return False
        return True


def check_eligibility_focus(focus: str, student: cc.Student) -> bool:
    """
        Given a focus and a student, returns True if the student
        has completed all the requirements for the provided focus and is eligible to obtain
        the degree or returns False if missing certain requirements. Note that the specific
        degree type(major/specialist) does not matter here as some focuses are only available
        for the specialist and for those found in both types, the requirements are identical.
        Also note that only MAT, CSC, and STA courses were included in the requirements.

        Preconditions:
        - focus in {'scientific computing', 'game design', 'computer vision', 'computational linguistics and natural
          language processing', 'artificial intelligence', 'web and internet technologies', 'theory of computation',
          'human-computer interaction', 'computer systems'}
        - degree == 'major' or degree == 'specialist'
    """
    s_c = []  # s_c is student courses
    for course in student.academic_history:
        s_c.append(course.course_taken.course_code)
    if focus == 'scientific computing':
        category_2_counter = 0
        category_3_counter = 0
        for course in s_c:
            if (course == 'CSC336H1' or course == 'CSC436H1' or course == 'CSC446H1' or course == 'CSC456H1'
                    or course == 'CSC466H1'):
                category_2_counter += 0.5
            elif (course == 'CSC317H1' or course == 'CSC320H1' or course == 'CSC417H1' or course == 'CSC418H1' or
                  course == 'CSC419H1' or course == 'CSC311H1' or course == 'CSC411H1' or course == 'CSC343H1' or
                  course == 'CSC384H1' or course == 'CSC358H1' or course == 'CSC457H1' or course == 'CSC458H1'):
                category_3_counter += 0.5
        if not (any(course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in
                    s_c) and category_2_counter >= 1.5 and category_3_counter >= 1.0):
            return False
        else:
            return True
    elif focus == 'game design':
        if not ('CSC300H1' in s_c and 'CSC301H1' in s_c and 'CSC318H1' in s_c and 'CSC384H1' in s_c and
                ('CSC317H1' in s_c or 'CSC417H1' in s_c or 'CSC418H1' in s_c or 'CSC419H1' in s_c)
                and 'CSC404H1' in s_c):
            return False
        else:
            return True
    elif focus == 'computer vision':
        if not (('MAT235Y1' in s_c or 'MAT237Y1' in s_c or 'MAT257Y1' in s_c) and 'CSC320H1' in s_c
                and 'CSC336H1' in s_c and ('CSC311H1' in s_c or 'CSC411H1' in s_c) and 'CSC420H1' in s_c and
                ('CSC412H1' in s_c or 'CSC417H1' in s_c or 'CSC317H1' in s_c or 'CSC418H1' in s_c or 'CSC419H1' in s_c
                 or 'CSC2503H' in s_c)):
            return False
        else:
            return True
    elif focus == 'computational linguistics and natural language processing':
        category_4_counter = 0
        for course in s_c:
            if course in {'CSC309H1', 'CSC413H1', 'CSC421H1', 'CSC321H1', 'CSC311H1', 'CSC411H1', 'CSC428H1',
                          'CSC486H1'}:
                category_4_counter += 0.5
        if not ('CSC318H1' in s_c and 'CSC401H1' in s_c and 'CSC485H1' in s_c and category_4_counter >= 1.5):
            return False
        else:
            return True
    elif focus == 'artificial intelligence':
        category_1_counter = 0
        category_2_counter = 0
        for course in s_c:
            if course in {'CSC336H1', 'MAT235Y1', 'MAT237Y1', 'MAT257Y1', 'MAT224H1', 'MAT247H1', 'STA238H1',
                          'STA248H1', 'STA261H1', 'STA302H1', 'STA347H1'}:
                if course[6] == 'H':
                    category_1_counter += 0.5
                else:
                    category_1_counter += 1.0
            elif course in {'CSC401H1', 'CSC485H1', 'CSC320H1', 'CSC420H1', 'CSC413H1', 'CSC421H1', 'CSC321H1',
                            'CSC311H1',
                            'CSC411H1', 'STA314H1', 'CSC412H1', 'STA414H1', 'CSC304H1', 'CSC384H1', 'CSC486H1'}:
                category_2_counter += 0.5
        if not (category_1_counter >= 1.0 and category_2_counter >= 2.5):
            return False
        else:
            return True
    elif focus == 'web and internet technologies':
        if not (('STA238H1' in s_c or 'STA248H1' in s_c or 'STA261H1' in s_c) and 'CSC309H1' in s_c and 'CSC343H1' in
                s_c and ('CSC358H1' in s_c or 'CSC457H1' in s_c) and 'CSC458H1' in s_c and
                ('CSC311H1' in s_c or 'CSC411H1' in s_c) and
                ('CSC367H1' in s_c or 'CSC443H1' in s_c or 'CSC469H1' in s_c)):
            return False
        else:
            return True
    elif focus == 'theory of computation':
        category_3_counter = 0
        category_4_counter = 0
        for course in s_c:
            if course in {'CSC304H1', 'CSC336H1', 'CSC438H1', 'CSC448H1', 'CSC473H1', 'MAT309H1', 'MAT332H1',
                          'MAT344H1'}:
                category_3_counter += 0.5
            elif course in {'MAT224H1', 'MAT247H1', 'MAT237Y1' 'MAT257Y1', 'MAT244H1', 'MAT267H1', 'MAT301H1',
                            'MAT347Y1',
                            'MAT315H1', 'MAT327H1', 'MAT334H1', 'MAT354H1', 'MAT335H1', 'MAT337H1', 'MAT357H1',
                            'STA238H1', 'STA248H1', 'STA261H1', 'STA347H1'} \
                    or course[:4] == 'MAT4':
                if course[6] == 'H':
                    category_4_counter += 0.5
                else:
                    category_4_counter += 1.0
        if not (any(course == 'MAT137Y1' or course == 'MAT157Y1' or course == 'MAT237Y1' for course in
                    s_c) and 'CSC463H1' in s_c and category_3_counter >= 2.0 and category_4_counter >= 2.0):
            return False
        else:
            return True
    elif focus == 'human-computer interaction':
        category_3_counter = 0
        for course in s_c:
            if course in {'CSC309H1', 'CSC320H1', 'CSC321H1', 'CSC343H1', 'CSC384H1', 'CSC401H1', 'CSC404H1',
                          'CSC418H1', 'CSC485H1', 'CSC490H1', 'CSC491H1'}:
                category_3_counter += 0.5
        if not ('CSC300H1' in s_c and 'CSC301H1' in s_c and 'CSC318H1' in s_c and 'CSC428H1' in s_c and
                category_3_counter >= 1.0):
            return False
        else:
            return True
    else:
        category_2_counter = 0
        category_2_courses = []
        category_3_counter = 0
        for course in s_c:
            if course in {'CSC358H1', 'CSC457H1', 'CSC443H1', 'CSC458H1'}:
                category_2_counter += 0.5
                category_2_courses.append(course)
            if course in {'CSC358H1', 'CSC457H1', 'CSC458H1', 'CSC324H1', 'CSC385H1',
                          'CSC488H1'} and course not in category_2_courses:
                category_3_counter += 0.5
        if not ('CSC343H1' in s_c and 'CSC367H1' in s_c and 'CSC469H1' in s_c and category_2_counter >= 1.0 and
                category_3_counter >= 1.0):
            return False
        else:
            return True


def get_requirements(program: str, degree_type: str, student: cc.Student) -> str:
    """
        Given the program/focus, returns the missing requirements to
        complete the program. For the computer science major/specialist, the
        year corresponding to the missing credits will be returned and for
        the focus, the category/group of courses missing will be returned. Note
        that since there are multiple pathways to completing the requirements,
        specific courses will not be returned but only the year or group of courses

        Preconditions:
        - program in {'computer science', 'scientific computing', 'game design', 'computer vision', 'computational
          linguistics and natural language processing', 'artificial intelligence', 'web and internet technologies',
          'theory of computation', 'human-computer interaction', 'computer systems'}
        - degree_type == 'major' or degree_type == 'specialist'
    """
    s_c = []
    for course in student.academic_history:
        s_c.append(course.course_taken.course_code)
    if program == 'computer science':
        if degree_type == 'major':
            if not ((('CSC108H1' in s_c and 'CSC148H1' in s_c and ('CSC165H1' in s_c or 'CSC240H1' in s_c)) or (
                    'CSC110Y1' in s_c and 'CSC111H1' in s_c)) and (
                            'Mat137Y1' in s_c or 'MAT157Y1' in s_c or ('Mat135H1 in s_c' and 'MAT136H1' in s_c))):
                return 'missing first year requirements'
            elif not ('CSC207H1' in s_c and ('CSC236H1' in s_c or 'CSC240H1' in s_c) and 'CSC258H1' in s_c and (
                    'CSC263H1' in s_c or 'CSC265H1' in s_c) and (
                              'STA247H1' in s_c or 'STA237H1' in s_c or 'STA255H1' in s_c or 'STA257H1' in s_c)):
                return 'missing second year requirements'
            later_year_credits = 0
            for course in s_c:
                if course[:4] == 'CSC2' or course[:4] == 'CSC3' or course[:4] == 'CSC4' or course == 'MAT223H1' or \
                        course == 'MAT240H1' or course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' or\
                        course == 'STA414H1' or ((course[:4] == 'MAT3' or course[:4] == 'MAT4') and course not in
                                                 {'MAT329Y1', 'MAT390H1', 'MAT391H1'}):
                    if course[6] == 'H':
                        later_year_credits += 0.5
                    else:
                        later_year_credits += 1.0
            if not (later_year_credits >= 3.0 and any(course[:4] == 'CSC4' for course in s_c) and any(
                    course[3] == '4' for course in s_c) and any(
                course == 'MAT223H1' or course == 'MAT240H1' for course in s_c) and
                    any(course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in s_c)):
                return 'missing later year requirements(post second year)'
            return 'no missing requirements, degree can be obtained'
        else:
            if not ((('CSC108H1' in s_c and 'CSC148H1' in s_c and ('CSC165H1' in s_c or 'CSC240H1' in s_c)) or (
                    'CSC110Y1' in s_c and 'CSC111H1 in s_c')) and (
                            'Mat137Y1' in s_c or 'MAT157Y1' in s_c or ('Mat135H1' in s_c and 'MAT136H1' in s_c))):
                return 'missing first year credits'
            elif not ('CSC207H1' in s_c and 'CSC209H1' in s_c and (
                    'CSC236H1' in s_c or 'CSC240H1' in s_c) and 'CSC258H1' in s_c and (
                              'CSC263H1' in s_c or 'CSC265H1' in s_c) and ('MAT223H1' in s_c or 'MAT240H1' in s_c) and (
                              'STA247H1' in s_c or 'STA237H1' in s_c or 'STA255H1' in s_c or 'STA257H1' in s_c)):
                return 'missing second year requirements'
            later_year_credits = 0
            csc_4_credits = 0
            mat_sta_credits = 0
            for course in s_c:
                if course[:4] == 'CSC3' or course == 'CSC369H1' or course == 'CSC373H1' or \
                        course[:4] == 'CSC4' or course == 'MAT224H1' or course == 'MAT247H1' or course == 'MAT235Y1' or\
                        course == 'MAT237Y1' or course == 'MAT257Y1' or course == 'STA248H1' or course == 'STA238H1' or\
                        course == 'STA261H1' or course[:4] == 'STA3' or course[:4] == 'STA4' or \
                        ((course[:4] == 'MAT3' or course[:4] == 'MAT4') and course not in
                         {'MAT329Y1', 'MAT390H1', 'MAT391H1'}):
                    if course[6] == 'H':
                        later_year_credits += 0.5
                    else:
                        later_year_credits += 1.0
                    if course[:4] == 'CSC4':
                        if course[6] == 'H':
                            csc_4_credits += 0.5
                        else:
                            csc_4_credits += 1.0
                    if course[:3] == 'MAT' or course[:3] == 'STA':
                        if course[6] == 'H':
                            mat_sta_credits += 0.5
                        else:
                            mat_sta_credits += 1.0
            if not (later_year_credits >= 6.0 and any(
                    course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in
                    s_c) and csc_4_credits >= 1.5 and (later_year_credits - mat_sta_credits) >= 4.0):
                return 'missing later year requirements(post second year)'
            return 'no missing requirements, degree can be obtained'
    if program == 'scientific computing':
        category_2_counter = 0
        category_3_counter = 0
        for course in s_c:
            if (course == 'CSC336H1' or course == 'CSC436H1' or course == 'CSC446H1' or course == 'CSC456H1' or
                    course == 'CSC466H1'):
                category_2_counter += 0.5
            elif (course == 'CSC317H1' or course == 'CSC320H1' or course == 'CSC417H1' or course == 'CSC418H1'
                  or course == 'CSC419H1' or course == 'CSC311H1' or course == 'CSC411H1' or course == 'CSC343H1' or
                  course == 'CSC384H1' or course == 'CSC358H1' or course == 'CSC457H1' or course == 'CSC458H1'):
                category_3_counter += 0.5
        if not (any(course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' for course in
                    s_c) and category_2_counter >= 1.5 and category_3_counter >= 1.0):
            if category_2_counter < 1.5 and category_3_counter < 1.0:
                return 'missing ' + str(
                    1.5 - category_2_counter) + ' credits from the following group of courses:' + \
                    ' CSC336H1, CSC436H1, CSC446H1, CSC456H1, CSC466H1' + 'and missing' + str(1.0 - category_3_counter)\
                    + 'credits from the following group of courses:' + ' CSC317H1 CSC320H1 CSC417H1,' + \
                    ' CSC418H1, CSC419H1, CSC311H1, CSC411H1, CSC343H1, CSC384H1, CSC358H1, CSC457H1, CSC458H1'
            elif category_2_counter < 1.5:
                return 'missing ' + str(1.5 - category_2_counter) + ' credits from the following group of courses:' + \
                    ' CSC336H1, CSC436H1, CSC446H1, CSC456H1, CSC466H1'
            elif category_3_counter < 1.0:
                return 'missing' + str(1.0 - category_3_counter) + 'credits from the following group of courses:' \
                    + ' CSC317H1 CSC320H1 CSC417H1, ' \
                      'CSC418H1, CSC419H1, CSC311H1, CSC411H1, CSC343H1, CSC384H1, CSC358H1, CSC457H1, CSC458H1'
            else:
                return 'missing a credit from the following list of courses:MAT235Y1, MAT237Y1, MAT257Y1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'game design':
        requirement_counter = 0
        for course in s_c:
            if course == 'CSC300H1' or course == 'CSC301H1' or course == 'CSC318H1' or course == 'CSC384H1' or \
                    course == 'CSC317H1' or course == 'CSC417H1' or course == 'CSC418H1' or course == 'CSC419H1' or \
                    course == 'CSC404H1':
                requirement_counter += 0.5
        if requirement_counter < 3.0:
            return 'missing ' + str(
                3.0 - requirement_counter) + ' credits from the following group of courses that have not already ' \
                                             'been completed: CSC300H, CSC301H1, CSC318H1, CSC384H1, CSC317H1, ' \
                                             'CSC417H1, CSC418H1, CSC419H1, CSC404H1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'computer vision':
        category_1_counter = 0
        category_2_counter = 0
        for course in s_c:
            if course == 'MAT235Y1' or course == 'MAT237Y1' or course == 'MAT257Y1' or course == 'CSC320H1' \
                    or course == 'CSC336H1' or course == 'CSC311H1' or course == 'CSC411H1' or course == 'CSC420H1':
                if course[6] == 'H':
                    category_1_counter += 0.5
                else:
                    category_1_counter += 1.0
            elif course == 'CSC412H1' or course == 'CSC417H1' or course == 'CSC317H1' or course == 'CSC418H1' \
                    or course == 'CSC419H1' or course == 'CSC2503H':
                category_2_counter += 0.5
        if not (category_1_counter >= 2.5 and category_2_counter >= 0.5):
            if category_1_counter < 2.5 and category_2_counter < 0.5:
                return 'missing ' + str(2.5 - category_1_counter) + ' credits from the following group of courses ' \
                                                                    'not already completed: MAT235Y1, MAT237Y1,' \
                                                                    ' MAT257Y1, CSC320H1, CSC336H1, CSC311H1, ' \
                                                                    'CSC411H1, CSC420H1 and missing 0.5 credits from' \
                                                                    ' the following list of courses: CSC412H1, ' \
                                                                    'CSC417H1, CSC317H1, CSC418H1, CSC419H1'
            elif category_1_counter < 2.5:
                return 'missing ' + str(2.5 - category_1_counter) + ' credits from the following group of courses ' \
                                                                    'not already completed: MAT235Y1, MAT237Y1, ' \
                                                                    'MAT257Y1, CSC320H1, CSC336H1, CSC311H1, ' \
                                                                    'CSC411H1, CSC420H1'
            else:
                return 'missing 0.5 credits from the following list of courses: CSC412H1, CSC417H1, ' \
                       'CSC317H1, CSC418H1, CSC419H1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'computational linguistics and natural language processing':
        category_4_counter = 0
        for course in s_c:
            if course in {'CSC309H1', 'CSC413H1', 'CSC421H1', 'CSC321H1', 'CSC311H1', 'CSC411H1', 'CSC428H1',
                          'CSC486H1'}:
                category_4_counter += 0.5
        if not ('CSC318H1' in s_c and 'CSC401H1' in s_c and 'CSC485H1' in s_c and category_4_counter >= 1.5):
            if 'CSC318H1' not in s_c and 'CSC401H1' not in s_c and 'CSC485H1' not in s_c and category_4_counter < 1:
                return 'missing CSC318H1, CSC401H1 and CSC485H1, and missing ' \
                    + str(1.0 - category_4_counter) + ' credits from the following group of courses not already ' \
                                                      'taken: CSC309H1, CSC413H1, CSC421H1, CSC321H1, CSC311H1, ' \
                                                      'CSC411H1, CSC428H1, CSC486H1'
            elif 'CSC318H1' not in s_c:
                return 'missing CSC318H1'
            elif 'CSC401H1' not in s_c:
                return 'missing CSC401H1'
            elif 'CSC485H1' not in s_c:
                return 'missing CSC485H1'
            else:
                return 'missing' + str(
                    1.0 - category_4_counter) + ' credits from the following group of courses not already taken: ' \
                    + 'CSC309H1, CSC413H1, CSC421H1, CSC321H1, CSC311H1, CSC411H1, CSC428H1, CSC486H1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'artificial intelligence':
        category_1_counter = 0
        category_2_counter = 0
        for course in s_c:
            if course in {'CSC336H1', 'MAT235Y1', 'MAT237Y1', 'MAT257Y1', 'MAT224H1', 'MAT247H1', 'STA238H1',
                          'STA248H1', 'STA261H1', 'STA302H1', 'STA347H1'}:
                if course[6] == 'H':
                    category_1_counter += 0.5
                else:
                    category_1_counter += 1.0
            elif course in {'CSC401H1', 'CSC485H1', 'CSC320H1', 'CSC420H1', 'CSC413H1', 'CSC421H1', 'CSC321H1',
                            'CSC311H1',
                            'CSC411H1', 'STA314H1', 'CSC412H1', 'STA414H1', 'CSC304H1', 'CSC384H1', 'CSC486H1'}:
                category_2_counter += 0.5
        if not (category_1_counter >= 1.0 and category_2_counter >= 2.5):
            if category_1_counter < 1.0 and category_2_counter < 2.5:
                return 'missing ' + str(
                    1.0 - category_1_counter) + ' credits from the following group of courses not already ' \
                                                'completed: CSC336H1, MAT235Y1, MAT237Y1, MAT257Y1, MAT224H1, ' \
                                                'MAT247H1, STA238H1, STA248H1, STA261H1, STA302H1, STA347H1 and ' \
                    + 'missing ' + str(2.5 - category_2_counter) + ' credits from the following group of courses ' \
                                                                   'not already taken: CSC401H1, CSC485H1, ' \
                                                                   'CSC320H1, CSC420H1, CSC413H1, CSC421H1, ' \
                                                                   'CSC321H1, CSC311H1, CSC411H1, STA314H1, ' \
                                                                   'CSC412H1, STA414H1, CSC304H1, CSC384H1, CSC486H1'
            elif category_1_counter < 1.0:
                return 'missing ' + str(1.0 - category_1_counter) + ' credits from the following group of courses not' \
                                                                    ' already completed: CSC336H1, MAT235Y1, ' \
                                                                    'MAT237Y1, MAT257Y1, MAT224H1, MAT247H1, ' \
                                                                    'STA238H1, STA248H1, STA261H1, STA302H1, STA347H1'
            else:
                return 'missing ' + str(
                    2.5 - category_2_counter) + ' credits from the following group of courses not already taken: ' \
                    + 'CSC401H1, CSC485H1, CSC320H1, CSC420H1, CSC413H1, CSC421H1, CSC321H1, CSC311H1,' \
                    + 'CSC411H1, STA314H1, CSC412H1, STA414H1, CSC304H1, CSC384H1, CSC486H1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'web and internet technologies':
        requirement_counter = 0
        for course in s_c:
            if (course == 'STA238H1' or course == 'STA248H1' or course == 'STA261H1' or course == 'CSC309H1'
                    or course == 'CSC343H1' or course == 'CSC358H1' or course == 'CSC457H1' or course == 'CSC458H1' or
                    course == 'CSC311H1' or course == 'CSC411H1' or course == 'CSC367H1' or course == 'CSC443H1' or
                    course == 'CSC469H1'):
                requirement_counter += 0.5
        if requirement_counter < 3.5:
            return 'missing ' + str(
                3.5 - requirement_counter) + ' credits from the following group of courses not already taken: ' \
                + 'STA238H1, STA248H1, STA261H1, CSC309H1, CSC343H1, CSC358H1, CSC457H1, CSC458H1, CSC311H1, ' \
                  'CSC411H1, CSC367H1, CSC443H1, CSC469H1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'theory of computation':
        category_3_counter = 0
        category_4_counter = 0
        for course in s_c:
            if course in {'CSC304H1', 'CSC336H1', 'CSC438H1', 'CSC448H1', 'CSC473H1', 'MAT309H1', 'MAT332H1',
                          'MAT344H1'}:
                category_3_counter += 0.5
            elif course in {'MAT224H1', 'MAT247H1', 'MAT237Y1' 'MAT257Y1', 'MAT244H1', 'MAT267H1', 'MAT301H1',
                            'MAT347Y1',
                            'MAT315H1', 'MAT327H1', 'MAT334H1', 'MAT354H1', 'MAT335H1', 'MAT337H1', 'MAT357H1',
                            'STA238H1', 'STA248H1', 'STA261H1', 'STA347H1'} \
                    or course[:4] == 'MAT4':
                if course[6] == 'H':
                    category_4_counter += 0.5
                else:
                    category_4_counter += 1.0
        if not (any(course == 'MAT137Y1' or course == 'MAT157Y1' or course == 'MAT237Y1' for course in s_c)
                and 'CSC463H1' in s_c and category_3_counter >= 2.0 and category_4_counter >= 2.0):
            if category_3_counter < 2.0 and category_4_counter < 2.0:
                return 'missing ' + str(
                    2.0 - category_3_counter) + ' credits from the following courses not already taken: ' \
                    + 'CSC304H1, CSC336H1, CSC438H1, CSC448H1, CSC473H1; MAT309H1, MAT332H1, MAT344H1 and missing' \
                    + str(2.0 - category_4_counter) \
                    + 'credits from the following group of courses not already taken: MAT224H1, MAT247H1, ' \
                      'MAT237Y1, MAT257Y1, MAT244H1, MAT267H1, MAT301H1, MAT347Y1,' \
                    + 'MAT315H1, MAT327H1, MAT334H1, MAT354H1, MAT335H1, MAT337H1, MAT357H1, STA238H1,' \
                      ' STA248H1, STA261H1, STA347H1'
            elif category_3_counter < 2.0:
                return 'missing ' + str(
                    2.0 - category_3_counter) + ' credits from the following courses not already taken: ' \
                    + 'CSC304H1, CSC336H1, CSC438H1, CSC448H1, CSC473H1; MAT309H1, MAT332H1, MAT344H1'
            elif category_4_counter < 2.0:
                return 'missing' + str(2.0 - category_4_counter) \
                    + 'credits from the following group of courses not already taken: MAT224H1, MAT247H1, ' \
                      'MAT237Y1, MAT257Y1, MAT244H1, MAT267H1, MAT301H1, MAT347Y1,' \
                    + 'MAT315H1, MAT327H1, MAT334H1, MAT354H1, MAT335H1, MAT337H1, MAT357H1, STA238H1, ' \
                      'STA248H1, STA261H1, STA347H1'
            else:
                return 'missing CSC463H1 and one of the following courses: MAT137Y1, MAT157Y1, MAT237Y1'
        else:
            return 'no missing requirements, degree can be obtained'
    elif program == 'human-computer interaction':
        category_3_counter = 0
        for course in s_c:
            if course in {'CSC309H1', 'CSC320H1', 'CSC321H1', 'CSC343H1', 'CSC384H1', 'CSC401H1', 'CSC404H1',
                          'CSC418H1', 'CSC485H1', 'CSC490H1', 'CSC491H1'}:
                category_3_counter += 0.5
        if not ('CSC300H1' in s_c and 'CSC301H1' in s_c and 'CSC318H1' in s_c and 'CSC428H1' in s_c
                and category_3_counter >= 1.0):
            if category_3_counter < 1.0:
                return 'missing ' + str(
                    1.0 - category_3_counter) + ' credits from the following group of courses not already taken: ' \
                    + ' CSC309H1, CSC320H1, CSC321H1, CSC343H1, CSC384H1, CSC401H1, CSC404H1, CSC418H1, ' \
                      'CSC485H1, CSC490H1, CSC491H1'
            else:
                return 'missing 2 credits from the following group of courses: CSC300H1, CSC301H1, CSC318H1, CSC428H1'
        else:
            return 'no missing requirements, degree can be obtained'
    else:
        category_2_counter = 0
        category_2_courses = []
        category_3_counter = 0
        for course in s_c:
            if course in {'CSC358H1', 'CSC457H1', 'CSC443H1', 'CSC458H1'}:
                category_2_counter += 0.5
                category_2_courses.append(course)
            if course in {'CSC358H1', 'CSC457H1', 'CSC458H1', 'CSC324H1', 'CSC385H1',
                          'CSC488H1'} and course not in category_2_courses:
                category_3_counter += 0.5
        if not ('CSC343H1' in s_c and 'CSC367H1' in s_c and 'CSC469H1' in s_c and category_2_counter >= 1.0 and
                category_3_counter >= 1.0):
            if category_2_counter < 1.0 and category_3_counter < 1.0:
                return 'missing ' + str(1.0 - category_2_counter) + ' credits from the following group of courses: ' \
                    + 'CSC358H1, CSC457H1, CSC443H1, CSC458H1 and missing ' + str(1.0 - category_3_counter) \
                    + ' credits from the following group of courses not already taken: CSC324H1, CSC385H1, CSC488H1'
            elif category_2_counter < 1.0:
                return 'missing ' + str(1.0 - category_2_counter) + ' credits from the following group of courses: ' \
                    + 'CSC358H1, CSC457H1, CSC443H1, CSC458H1'
            elif category_3_counter < 1.0:
                return 'missing ' + str(1.0 - category_3_counter) + ' credits' \
                    + 'from the following group of courses not already taken: CSC324H1, CSC385H1, CSC488H1'
            else:
                return 'missing 1.5 credits from the following group of courses: CSC343H1, CSC367H1, CSC469H1 '
        else:
            return 'no missing requirements, degree can be obtained'


def run_example(student: cc.Student) -> None:
    """
        Runs an example of the graph visualizer with a Student object.

        Note: please fullscreen the Matplotlib window.
    """
    graph = Program(course_data, student)
    di_graph = nx.DiGraph()
    graph.create_graph(di_graph)
    visualize_graph(di_graph)


if __name__ == '__main__':
    # raw data taken from CourseScrapper.py
    raw_data = CourseScrapper.read_from_csv('CourseData.csv')

    # formatted data
    course_data = create_course_mapping(raw_data)

    # runs an example of the visualizer using a Student object
    student_example = cc.Student(1, 'Student', [cc.Record(course_data['CSC110Y1'], 80, 0.5),
                                                cc.Record(course_data['CSC111H1'], 80, 0.5)])
    run_example(student_example)
