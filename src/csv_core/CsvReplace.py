from . import CsvRead
from . import CsvWrite
import csv
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

def college(College_Code, replacement_data):

    college_data = CsvRead.college()[1:]

    new_college_data = []
    for row in college_data:
        if row[0].lower() != College_Code.lower():
            new_college_data.append(row)
        else:
            new_college_data.append(replacement_data)

    CsvWrite.college(new_college_data, True)

def program(Program_Code, replacement_data):

    program_data = CsvRead.program()[1:]

    new_program_data = []
    for row in program_data:
        if row[1].lower() != Program_Code.lower():
            new_program_data.append(row)
        else:
            new_program_data.append(replacement_data)

    CsvWrite.program(new_program_data, True)

def student(student_ID, replacement_data):

    student_data = CsvRead.student()[1:]

    new_student_data = []
    for row in student_data:
        if row[0].lower() != student_ID.lower():
            new_student_data.append(row)
        else:
            new_student_data.append(replacement_data)

    CsvWrite.student(new_student_data, True)
