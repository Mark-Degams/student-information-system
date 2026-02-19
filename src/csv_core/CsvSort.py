import csv
from . import CsvRead
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

def college():
    college_data = CsvRead.college()
    header = college_data[0]
    data = college_data[1:]

    sorted_data = sorted(data, key=lambda x: (x[0], x[1]))

    with open(CsvCollege, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

def program():
    program_data = CsvRead.program()
    header = program_data[0]
    data = program_data[1:]

    sorted_data = sorted(data, key=lambda x: (x[0], x[1]))

    with open(CsvProgram, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

def student():
    student_data = CsvRead.student()
    header = student_data[0]
    data = student_data[1:]
        
    sorted_data = sorted(data, key=lambda x: (int(x[0].split('-')[0]), int(x[0].split('-')[1])))
    
    with open(CsvStudent, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

def All():
    student()
    program()
    college()



        