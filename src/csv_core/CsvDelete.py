from . import CsvRead
import csv
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

def college(College_Code):

    college_data = CsvRead.college()

    new_college_data = []
    for row in college_data:
        if row[0].lower() != College_Code.lower():
            new_college_data.append(row)

    with open(CsvCollege, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_college_data)

def program(Program_Code):

    program_data = CsvRead.program()

    new_program_data = []
    for row in program_data:
        if row[1].lower() != Program_Code.lower():
            new_program_data.append(row)

    with open(CsvProgram, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_program_data)

def student(student_ID):

    student_data = CsvRead.student()

    new_student_data = []
    for row in student_data:
        if row[0].lower() != student_ID.lower():
            new_student_data.append(row)

    with open(CsvStudent, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_student_data)