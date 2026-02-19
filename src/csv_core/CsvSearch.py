from . import CsvRead
from pathlib import Path

BaseParent = Path(__file__).parent.parent.parent
CsvCollege = BaseParent / "CSV_Files" / "College.csv"
CsvProgram = BaseParent / "CSV_Files" / "Program.csv"
CsvStudent = BaseParent / "CSV_Files" / "Student.csv"

# --- College Search ---

def collegeCode(College_Code, boolean = False):
    college_data = CsvRead.college()

    for row in college_data:
        if row[0].lower() == College_Code.lower():
            return row
    return None

def collegeName(College_Name):
    college_data = CsvRead.college()

    college_with_name = []
    for row in college_data:
        if row[1].lower() == College_Name.lower():
            college_with_name.append(row)

    if college_with_name:
        return college_with_name
    return None

# --- Program Search ---

def programCollege(College_Code):
    program_data = CsvRead.program()

    programs_in_college = []
    for row in program_data:
        if row[0].lower() == College_Code.lower():
            programs_in_college.append(row)
    
    if programs_in_college:
        return programs_in_college
    return None

def programCode(Program_Code):
    program_data = CsvRead.program()

    for row in program_data:
        if row[1].lower() == Program_Code.lower():
            return row
    return None

def programName(Program_Name):
    program_data = CsvRead.program()

    program_with_name = []
    for row in program_data:
        if row[2].lower() == Program_Name.lower():
            program_with_name.append(row)

    if program_with_name:
        return program_with_name
    return None

# --- Student Search ---

def studentID(student_ID):
    student_data = CsvRead.student()

    for row in student_data:
        if row[0] == student_ID:
            return [row]
    return None

def studentName(student_name):
    student_data = CsvRead.student()

    student_with_name = []
    for row in student_data:
        if row[1].lower() == student_name.lower() or row[2].lower() == student_name.lower():
            student_with_name.append(row)
        elif f"{row[1]} {row[2]}".lower() == student_name.lower() or f"{row[2]} {row[1]}".lower() == student_name.lower():
            student_with_name.append(row)
    
    if student_with_name:
        return student_with_name 
    return None

def studentProgram(program):
    student_data = CsvRead.student()

    if programCode(program):
        program_code = program
    elif programName(program):
        program_code = programName(program)[1]
    else:
        return None

    students_in_program = []
    for row in student_data:
        if row[3].lower() == program_code.lower():
            students_in_program.append(row)

    if students_in_program:
        return students_in_program
    return None

def studentCollege(student_college):
    student_data = CsvRead.student()
    program_data = CsvRead.program()

    if collegeCode(student_college):
        college_code = student_college.lower()
    elif collegeName(student_college):
        college_code = collegeName(student_college)[0].lower()
    else:
        return None
    
    programs_in_college = programCollege(college_code)
    programs = []
    for rows in programs_in_college:
        programs.append(rows[1])
    
    students_in_college = []
    for row in student_data:
        if row[3] in programs:
            students_in_college.append(row)

    if students_in_college:
        return students_in_college
    return None

def studentYear(student_year):
    student_data = CsvRead.student()

    students_in_year = []
    for row in student_data:
        if row[4] == student_year:
            students_in_year.append(row)

    if students_in_year:
        return students_in_year
    return None

def studentGender(student_gender):
    student_data = CsvRead.student()

    if student_gender.lower() == "male":
        student_gender = "m"
    elif student_gender.lower() == "female":
        student_gender = "f"

    students_in_gender = []
    for row in student_data:
        if row[5].lower() == student_gender.lower():
            students_in_gender.append(row)

    if students_in_gender:
        return students_in_gender
    return None
