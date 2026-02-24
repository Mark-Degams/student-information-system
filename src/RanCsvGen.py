import random
from src.csv_core import CsvRead
from src.csv_core import CsvWrite

def generate_random_student(student_count = 5000):

    generate_program_college()

    def create_student_ID(year_prefix):
        student_number = f"{random.randint(1,9999):04d}" 
        student_id = f"{year_prefix}-{student_number}"

        if student_id in student_ids: 
            student_id = create_student_ID(year_prefix)
        return student_id

    data = [
        ["Student ID", "Last Name", "First Name", "Program Code", "Year", "Gender"]
    ]

    student_ids = []

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris",
        "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright",
        "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall",
        "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
        "Gomez", "Phillips", "Evans", "Turner", "Diaz",
        "Parker", "Cruz", "Edwards", "Collins", "Reyes",
        "Stewart", "Morris", "Morales", "Murphy", "Cook",
        "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard",
        "Ramos", "Kim", "Cox", "Ward", "Richardson",
        "Watson", "Brooks", "Chavez", "Wood", "James",
        "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel",
        "Myers", "Long", "Ross", "Foster", "Jimenez",
        "Powell", "Jenkins", "Perry", "Russell", "Sullivan",
        "Adeva", "Bongcawel", "Villadolid", "Dela Cruz", "Santos"
    ]

    first_names = [
        "James", "Mary", "John", "Patricia", "Robert",
        "Jennifer", "Michael", "Linda", "William", "Elizabeth",
        "David", "Barbara", "Richard", "Susan", "Joseph",
        "Jessica", "Thomas", "Sarah", "Charles", "Karen",
        "Christopher", "Nancy", "Daniel", "Lisa", "Matthew",
        "Betty", "Anthony", "Margaret", "Mark", "Sandra",
        "Donald", "Ashley", "Steven", "Kimberly", "Paul",
        "Emily", "Andrew", "Donna", "Joshua", "Michelle",
        "Kenneth", "Dorothy", "Kevin", "Carol", "Brian",
        "Amanda", "George", "Melissa", "Edward", "Deborah",
        "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason",
        "Laura", "Jeffrey", "Sharon", "Ryan", "Cynthia",
        "Jacob", "Kathleen", "Gary", "Amy", "Nicholas",
        "Shirley", "Eric", "Angela", "Jonathan", "Helen",
        "Stephen", "Anna", "Larry", "Brenda", "Justin",
        "Pamela", "Scott", "Nicole", "Brandon", "Emma",
        "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory",
        "Christine", "Alexander", "Debra", "Frank", "Rachel",
        "Patrick", "Catherine", "Raymond", "Carolyn", "Jack",
        "Janet", "Dennis", "Maria", "Jerry", "Heather",
        "Tyler", "Diane", "Aaron", "Ruth", "Jose",
        "Olivia", "Henry", "Evelyn", "Adam", "Sophia"
    ]

    program_codes = []
    for row in CsvRead.program()[1:]:
        program_codes.append(row[1])
    genders = ["M", "F"]

    for _ in range(student_count):
        year_prefix = random.choice([2019,2020,2021,2022,2023,2024,2025])
        student_id = create_student_ID(year_prefix)

        last = random.choice(last_names)
        first = random.choice(first_names)
        program = random.choice(program_codes)
        year = random.randint(1,2026-year_prefix)
        if year > 5: year = 5
        gender = random.choice(genders)
        
        data.append([student_id, last, first, program, year, gender])
        student_ids.append(student_id)

    CsvWrite.student(data[1:])

def generate_program_college():
    colleges = [
        ["CASS", "COLLEGE OF ARTS AND SOCIAL SCIENCES"],
        ["CBAA", "COLLEGE OF BUSINESS AND ACCOUNTANCY"],
        ["CCS", "COLLEGE OF COMPUTER STUDIES"],
        ["CED", "COLLEGE OF EDUCATION"],
        ["COE", "COLLEGE OF ENGINEERING"],
        ["CON", "COLLEGE OF NURSING"],
        ["CSM", "COLLEGE OF SCIENCE AND MATHEMATICS"]
    ]
    programs = [
        ["CASS","BAELS","BACHELOR OF ARTS IN ENGLISH LANGUAGE STUDIES"],
        ["CASS","BAFil","BACHELOR OF ARTS IN FILIPINO"],
        ["CASS","BAHis","BACHELOR OF ARTS IN HISTORY"],
        ["CASS","BALCS","BACHELOR OF ARTS IN LITERATURE AND CULTURAL STUDIES"],
        ["CASS","BAPan","BACHELOR OF ARTS IN PANITIKAN"],
        ["CASS","BAPols","BACHELOR OF ARTS IN POLITICAL SCIENCE"],
        ["CASS","BAPsych","BACHELOR OF ARTS IN PSYCHOLOGY"],
        ["CASS","BASoc","BACHELOR OF ARTS IN SOCIOLOGY"],
        ["CASS","BSPhilo","BACHELOR OF SCIENCE IN PHILOSOPHY MAJOR IN APPLIED ETHICS"],
        ["CASS","BSPsych","BACHELOR OF SCIENCE IN PSYCHOLOGY"],
        ["CBAA","BSA","BACHELOR OF SCIENCE IN ACCOUNTANCY"],
        ["CBAA","BSBA-BE","BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (BUSINESS ECONOMICS)"],
        ["CBAA","BSBA-EM","BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ENTREPRENEURIAL MARKETING)"],
        ["CBAA","BSBA-Econ","BACHELOR OF SCIENCE IN BUSINESS ADMINISTRATION (ECONOMICS)"],
        ["CBAA","BSHRM","BACHELOR OF SCIENCE IN HOTEL AND RESTAURANT MANAGEMENT"],
        ["CCS","BSCA","BACHELOR OF SCIENCE IN COMPUTER APPLICATION"],
        ["CCS","BSCS","BACHELOR OF SCIENCE IN COMPUTER SCIENCE"],
        ["CCS","BSIS","BACHELOR OF SCIENCE IN INFORMATION SYSTEMS"],
        ["CCS","BSIT","BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY"],
        ["CED","BEED-Eng","BACHELOR OF ELEMENTARY EDUCATION (ENGLISH)"],
        ["CED","BEED-SH","BACHELOR OF ELEMENTARY EDUCATION (SCIENCE AND HEALTH)"],
        ["CED","BSED-Bio","BACHELOR OF SECONDARY EDUCATION (BIOLOGY)"],
        ["CED","BSED-Chem","BACHELOR OF SECONDARY EDUCATION (CHEMISTRY)"],
        ["CED","BSED-GenSci","BACHELOR OF SECONDARY EDUCATION (GENERAL SCIENCE)"],
        ["CED","BSED-Mapeh","BACHELOR OF SECONDARY EDUCATION (MAPEH)"],
        ["CED","BSED-Math","BACHELOR OF SECONDARY EDUCATION (MATHEMATICS)"],
        ["CED","BSED-Phys","BACHELOR OF SECONDARY EDUCATION (PHYSICS)"],
        ["CED","BSED-TLE","BACHELOR OF SECONDARY EDUCATION (TLE)"],
        ["CED","BSIE-Draft","BACHELOR OF SCIENCE IN INDUSTRIAL EDUCATION (DRAFTING)"],
        ["CED","BSTTE-DT","BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (DRAFTING TECH)"],
        ["CED","BSTTE-IT","BACHELOR OF SCIENCE IN TECHNOLOGY TEACHER EDUCATION (INDUSTRIAL TECH)"],
        ["COE","BSCE","BACHELOR OF SCIENCE IN CIVIL ENGINEERING"],
        ["COE","BSCerE","BACHELOR OF SCIENCE IN CERAMICS ENGINEERING"],
        ["COE","BSChE","BACHELOR OF SCIENCE IN CHEMICAL ENGINEERING"],
        ["COE","BSCpE","BACHELOR OF SCIENCE IN COMPUTER ENGINEERING"],
        ["COE","BSEE","BACHELOR OF SCIENCE IN ELECTRICAL ENGINEERING"],
        ["COE","BSEcE","BACHELOR OF SCIENCE IN ELECTRONICS & COMMUNICATIONS ENGINEERING"],
        ["COE","BSEnE","BACHELOR OF SCIENCE IN ENVIRONMENTAL ENGINEERING"],
        ["COE","BSME","BACHELOR OF SCIENCE IN MECHANICAL ENGINEERING"],
        ["COE","BSMetE","BACHELOR OF SCIENCE METALLURGICAL ENGINEERING"],
        ["COE","BSMinE","BACHELOR OF SCIENCE IN MINING ENGINEERING"],
        ["CON","BSN","BACHELOR OF SCIENCE IN NURSING"],
        ["CSM","BSBio-Bot","BACHELOR OF SCIENCE IN BIOLOGY (BOTANY)"],
        ["CSM","BSBio-Gen","BACHELOR OF SCIENCE IN BIOLOGY (GENERAL)"],
        ["CSM","BSBio-Mar","BACHELOR OF SCIENCE IN BIOLOGY (MARINE)"],
        ["CSM","BSBio-Zoo","BACHELOR OF SCIENCE IN BIOLOGY (ZOOLOGY)"],
        ["CSM","BSChem","BACHELOR OF SCIENCE IN CHEMISTRY"],
        ["CSM","BSMath","BACHELOR OF SCIENCE IN MATHEMATICS"],
        ["CSM","BSPhys","BACHELOR OF SCIENCE IN PHYSICS"],
        ["CSM","BSStat","BACHELOR OF SCIENCE IN STATISTICS"]
    ]
    CsvWrite.program(programs)
    CsvWrite.college(colleges)


if __name__ == "__main__":
    generate_random_student()