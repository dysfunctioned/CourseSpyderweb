"""
TO DO: Add Docstring
"""
from dataclasses import dataclass


@dataclass
class Course:
    """
        A class for a course in the system.

        Instance Attributes:
        - course_code: A string of characters representing the course code.
        - course_description: A description of the course
        - prerequisites: A list of courses that must be completed before taking this course.
        - recommended: A list of other recommended courses to take.
        - corequisite: A list of courses that are to be taken simultaneously with this course.
        - exclusion: A list of courses that a student is excluded from taking due to similarities in course content.
        - breadth_requirements: An number representing the breadth requirement that this course satisfies.

        Representation Invariants:
        - self.course_code != ''
        - self.course_department != ''
        - 0 < self.breadth_requirements <= 5
    """
    course_code: str
    course_title: str
    course_description: str
    prerequisites: list[str]
    recommended: list[str]
    corequisite: list[str]
    exclusion: list[str]
    breadth_requirements: int


@dataclass
class Record:
    """
        An academic record on a student's academic transcript for a course.

        Instance Attributes:
        - course_taken: A course that the student has completed.
        - grade: The grade that the student has received for the course taken.
        - weight: The weight of the course, worth either 0.5 or 1.0 credits.

        Representation Invariants:
        - 0 <= self.grade <= 100
        - self.weight == (0.5 or 1.0)
    """
    course_taken: Course
    grade: int
    weight: float


@dataclass
class Student:
    """
        A class representing a student profile.

        Instance Attributes:
        - student_number: A 10-digit number that serves as the student's unique identifier.
        - student_name: The student's full name.
        - academic_history: A list of all the student's academic records, each consisting of a course and
        their corresponding information.

        Representation Invariants:
        - len(self.student_number) == 10
        - self.student_name != ''
    """
    student_number: int
    student_name: str
    academic_history: list[Record]
