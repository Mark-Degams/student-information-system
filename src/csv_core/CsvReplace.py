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
    if isinstance(Program_Code, list):
        Program_Code = [row.lower() for row in Program_Code]
        for row in program_data:
            if row[1].lower() in Program_Code:
                row[0] = replacement_data
                print(row)
            new_program_data.append(row)
            
    else:
        for row in program_data:
            if row[1].lower() != Program_Code.lower():
                new_program_data.append(row)
            else:
                new_program_data.append(replacement_data)

    CsvWrite.program(new_program_data, True)

def programCollege(program_codes, value):
    program_data = CsvRead.program()[1:]

    for row in program_data:
        if row[1] in program_codes:
            row[0] = value

    CsvWrite.program(program_data, True)

def student(student_ID, replacement_data):

    student_data = CsvRead.student()[1:]

    new_student_data = []
    for row in student_data:
        if row[0].lower() != student_ID.lower():
            new_student_data.append(row)
        else:
            new_student_data.append(replacement_data)

    CsvWrite.student(new_student_data, True)

def studentProgram(student_ids, value):
    student_data = CsvRead.student()[1:]

    for row in student_data:
        if row[0] in student_ids:
            row[3] = value

    CsvWrite.student(student_data, True)

