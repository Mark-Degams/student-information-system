from src import StudentSytemGUI
import csv
import os

def initialize_csv_files():
    folder = "CSV_Files"
    files = {
        "College.csv": ["College Code", "College Name"],
        "Program.csv": ["College Code", "Program Code", "Program Name"],
        "Student.csv": ["Student ID", "Last Name", "First Name", "Program Code", "Year Level", "Gender"]
    }

    if not os.path.exists(folder):
        os.makedirs(folder)

    for file_name, headers in files.items():
        file_path = os.path.join(folder, file_name)

        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

def main():
    initialize_csv_files()
    app = StudentSytemGUI.student_system_gui()
    app.mainloop()


if __name__ == "__main__":
    main()