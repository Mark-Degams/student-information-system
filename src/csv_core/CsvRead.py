import csv
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

def college():
    with open(CsvCollege, "r") as file:
        reader = csv.reader(file)
        college_data = list(reader)

    return college_data

def program():
    with open(CsvProgram, "r") as file:
        reader = csv.reader(file)
        program_data = list(reader)

    return program_data

def student():
    with open(CsvStudent, "r") as file:
        reader = csv.reader(file)
        student_data = list(reader)

    return student_data