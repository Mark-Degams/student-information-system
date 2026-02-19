import csv
from . import CsvRead
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

def college(new_data, replace = False):
    if not new_data: return
    college_data = CsvRead.college()
    header = college_data[0]

    if replace:
        data = {row[0]: row for row in new_data}
    else:
        past_data = college_data[1:]
        data = {row[0]: row for row in past_data}
        for line in new_data:
            if line and line[0].strip():
                data[line[0]] = line
    
    sorted_data = sorted(data.values(), key=lambda x: (x[0], x[1]))

    with open(CsvCollege, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

def program(new_data, replace = False):
    if not new_data: return
    program_data = CsvRead.program()
    header = program_data[0]

    if replace:
        data = {row[1]: row for row in new_data}
    else:
        past_data = program_data[1:]
        data = {row[1]: row for row in past_data}
        for line in new_data:
            if line and line[1].strip():
                data[line[1]] = line

    sorted_data = sorted(data.values(), key=lambda x: (x[0], x[1]))

    with open(CsvProgram, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)

def student(new_data, replace = False):
    if not new_data: return
    student_data = CsvRead.student()
    header = student_data[0]

    if replace:
        data = {row[0]: row for row in new_data}
    else:
        past_data = student_data[1:]
        data = {row[0]: row for row in past_data}
        for line in new_data:
            if line and line[0].strip():
                data[line[0]] = line
        
    sorted_data = sorted(data.values(), key=lambda x: (int(x[0].split('-')[0]), int(x[0].split('-')[1])))
    
    with open(CsvStudent, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)





        