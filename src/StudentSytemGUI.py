from src.csv_core import *
from tkinter import *
from tkinter import ttk, messagebox
from pathlib import Path

from src import RanCsvGen
from src import Constraints

def student_system_gui():
    bg_color = "#ffffff"

    window = Tk()
    window.geometry("600x400")
    window.title("Student Information System(Lite)")
    window.config(bg=bg_color)
    window.config()
    window.resizable(False, False)

    icon_path = Path(__file__).parent.parent / "Images" / "icon.png"
    icon = PhotoImage(file=icon_path)
    window.iconphoto(True, icon)

    header = Frame(window, height=30, bg="#B90000")
    header.pack(fill=X)

    header.grid_columnconfigure(0, weight=3)
    header.grid_columnconfigure(1, weight=1) 

    title = Label(
        header,
        text="Student Information System",
        font=("Helvetica", 12, "bold"),
        bg="#B90000",
        fg="#FFD700"
    )
    title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    button_frame = Frame(header, bg="#B90000")
    button_frame.grid(row=0, column=1, sticky="e", padx=20)

    button_search_student = Button(button_frame, text="Student", bg="#ffffff",fg = "#000000")
    button_search_program = Button(button_frame, text="Program", bg="#B90000",fg = "#FFD700")
    button_search_college = Button(button_frame, text="College", bg="#B90000",fg = "#FFD700")

    header_buttons = [button_search_student, button_search_program, button_search_college]
    for buttons in header_buttons:
        buttons.pack(side=LEFT, padx=2)
        buttons.config(font=("Helvetica", 9), 
                       relief= FLAT, overrelief= FLAT,
                       activebackground="#B90000", 
                       bd=0, highlightthickness=0, borderwidth=0,
                       width=8)

    input_frame = Frame(window, bg=bg_color, width=575)
    input_frame.pack(pady=10)

    toggle_search_button = Button(input_frame, width=16,text="Search by: Default")
    input_entry = Entry(input_frame, width=30, font=("Arial", 12))
    add_button = Button(input_frame,  text = "+", width=2, height=1)
    toggle_sort_button = Button(input_frame, width=18, text="Sort by: Student ID")

    toggle_search_button.pack(side=LEFT, padx=5)
    input_entry.pack(side=LEFT, padx=5)
    add_button.pack(side=LEFT)
    toggle_sort_button.pack(side=LEFT, padx=5)

    output_frame = Frame(window, bg=bg_color)
    output_frame.pack(pady=20)

    # --- GUI Functions ---

    def empty_csv_check():

        def generate_student():
            response = messagebox.askyesno("Generate Random Student", "Its look like your CSV Files are empty, do you want to generate random student?")
            if response:
                RanCsvGen.generate_random_student()
                search_student()
                show_notif("100 Random Students Are Added")

        if len(CsvRead.student()) == 1:
            generate_student()
 
    def add_placeholder(entry, text):
        entry.delete(0, END)
        entry.insert(0, text)
        entry.config(fg="gray")

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, END)
                entry.config(fg="black")

        def on_focus_out(e):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def search_student():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()

        def display_result(data):
            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            if sort_by_year: data = sorted(data, key=lambda x: x[4])
            elif sort_by_name: data = sorted(data, key=lambda x: (x[1], x[2]))
            elif sort_by_program: data = sorted(data, key=lambda x: (x[3], x[4]))

            headers = CsvRead.student()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings")
            tree.pack(fill=BOTH, expand=TRUE)

            for i in range (len(headers)):
                tree.heading(headers[i], text=headers[i].title())
                if i == 0: tree.column(headers[i], width=75, anchor=CENTER)
                elif i == 1: tree.column(headers[i], width=150, )
                elif i == 2: tree.column(headers[i], width=150)
                elif i == 3: tree.column(headers[i], width=100)
                elif i == 4: tree.column(headers[i], width=50, anchor=CENTER)
                elif i == 5: tree.column(headers[i], width=50, anchor=CENTER)

            for item in data:
                tree.insert("", END, values=item,)

            tree.bind("<Button-3>", lambda event: on_right_click(event, tree))

        result = None

        if search_by_student_ID:
            students = CsvRead.student()[1:]
            result = [row for row in students if input_text.lower() in row[0].lower()]
        elif search_by_student_name:
            students = CsvRead.student()[1:]
            result = [row for row in students if input_text.lower() in row[1].lower() or input_text.lower() in row[2].lower()]
        elif search_by_student_program:
            students = CsvRead.student()[1:]
            result = [row for row in students if input_text.lower() in row[3].lower()]
        else:
            if CsvSearch.studentID(input_text):
                result = CsvSearch.studentID(input_text)
            elif CsvSearch.studentName(input_text):
                result = CsvSearch.studentName(input_text)
            elif CsvSearch.studentProgram(input_text):
                result = CsvSearch.studentProgram(input_text)
            elif CsvSearch.studentCollege(input_text):
                result = CsvSearch.studentCollege(input_text)
            elif CsvSearch.studentYear(input_text):
                result = CsvSearch.studentYear(input_text)
            elif input_text.lower() in ["male", "female", "m", "f"]:
                result = CsvSearch.studentGender(input_text)
            elif input_text.lower() in ["all"] or input_text == "" or input_text == "Enter Student Info...":
                result = CsvRead.student()[1:]

        display_result(result)

    def search_program():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()

        def display_result(data):
            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            if sort_by_program_name: data = sorted(data, key=lambda x: x[2])
            elif sort_by_program_code: data = sorted(data, key=lambda x: x[1])

            headers = CsvRead.program()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings")
            tree.pack(fill="both", expand=True)

            for i in range(len(headers)):
                h = headers[i]
                tree.heading(h, text=headers[i].title())
                if i == 0: tree.column(h, width=90, anchor=CENTER)
                elif i == 1: tree.column(h, width=90)
                elif i == 2: tree.column(h, width=395)

            for item in data:
                tree.insert("", END, values=item)

            tree.bind("<Button-3>", lambda event: on_right_click(event, tree))

        result = None

        if search_by_program_code:
            programs = CsvRead.program()[1:]
            result = [row for row in programs if input_text.lower() in row[1].lower()]
        elif search_by_program_name:
            programs = CsvRead.program()[1:]
            result = [row for row in programs if input_text.lower() in row[2].lower()]
        elif search_by_program_college:
            programs = CsvRead.program()[1:]
            result = [row for row in programs if input_text.lower() in row[0].lower()]
        else:
            if CsvSearch.programCode(input_text):
                result = [CsvSearch.programCode(input_text)]
            elif CsvSearch.programName(input_text):
                result = CsvSearch.programName(input_text)
            elif CsvSearch.programCollege(input_text):
                result = CsvSearch.programCollege(input_text)
            elif input_text.lower() in ["all"] or input_text == "" or input_text == "Enter Program Info...":
                result = CsvRead.program()[1:]

        display_result(result)

    def search_college():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()
        
        def display_result(data):
            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            if sort_by_college_name: data = sorted(data, key=lambda x: x[1])

            headers = CsvRead.college()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings")
            tree.pack(fill="both", expand=True)

            for i in range(len(headers)):
                h = headers[i]
                tree.heading(h, text=headers[i].title())
                if i == 0: tree.column(h, width=100, anchor=CENTER)
                elif i == 1: tree.column(h, width=475)

            for item in data:
                tree.insert("", END, values=item)

            tree.bind("<Button-3>", lambda event: on_right_click(event, tree))

        result = None

        if search_by_college_code:
            college = CsvRead.college()[1:]
            result = [row for row in college if input_text.lower() in row[0].lower()]
        elif search_by_college_name:
            college = CsvRead.college()[1:]
            result = [row for row in college if input_text.lower() in row[1].lower()]
        else:
            if CsvSearch.collegeCode(input_text):
                result = [CsvSearch.collegeCode(input_text)]
            elif CsvSearch.collegeName(input_text):
                result = CsvSearch.collegeName(input_text)
            elif input_text.lower() in ["all"] or input_text == "" or input_text == "Enter College Info...":
                result = CsvRead.college()[1:]

        display_result(result)

    def toggle_search_by(freeze = False):
        window.focus_set()
        global search_by_Student, search_by_Program, search_by_College
        button_name = "Search by: "

        if search_by_Student:
            global search_by_student_ID, search_by_student_name, search_by_student_program, toggle_search_by_student_value

            if not freeze:
                if toggle_search_by_student_value == 4: toggle_search_by_student_value = 1
                else: toggle_search_by_student_value += 1

            match toggle_search_by_student_value:
                case 1:
                    search_by_student_ID = False
                    search_by_student_name = False
                    search_by_student_program = False
                    button_name += "Default"
                    add_placeholder(input_entry, "Enter Student Info...")
                case 2:
                    search_by_student_ID = True
                    search_by_student_name = False
                    search_by_student_program = False
                    button_name += "ID"
                    add_placeholder(input_entry, "Enter Student ID...")
                case 3:
                    search_by_student_ID = False
                    search_by_student_name = True
                    search_by_student_program = False
                    button_name += "Name"
                    add_placeholder(input_entry, "Enter Student Name...")
                case 4:
                    search_by_student_ID = False
                    search_by_student_name = False
                    search_by_student_program = True
                    button_name += "Program"
                    add_placeholder(input_entry, "Enter Student Program...")

        elif search_by_Program: 
            global search_by_program_code, search_by_program_name, search_by_program_college, toggle_search_by_program_value

            if not freeze:
                if toggle_search_by_program_value == 4: toggle_search_by_program_value = 1
                else: toggle_search_by_program_value += 1

            match toggle_search_by_program_value:
                case 1:
                    search_by_program_code = False
                    search_by_program_name = False
                    search_by_program_college = False
                    button_name += "Default"
                    add_placeholder(input_entry, "Enter Program Info...")
                case 2:
                    search_by_program_code = True
                    search_by_program_name = False
                    search_by_program_college = False
                    button_name += "Code"
                    add_placeholder(input_entry, "Enter Program Code...")
                case 3:
                    search_by_program_code = False
                    search_by_program_name = True
                    search_by_program_college = False
                    button_name += "Name"
                    add_placeholder(input_entry, "Enter Program Name...")
                case 4:
                    search_by_program_code = False
                    search_by_program_name = False
                    search_by_program_college = True
                    button_name += "College"
                    add_placeholder(input_entry, "Enter Program College...")

        else:
            global search_by_college_code, search_by_college_name, toggle_search_by_college_value

            if not freeze:
                if toggle_search_by_college_value ==  3: toggle_search_by_college_value = 1
                else: toggle_search_by_college_value += 1

            match toggle_search_by_college_value:
                case 1:
                    search_by_college_code = False
                    search_by_college_name = False
                    button_name += "Default"
                    add_placeholder(input_entry, "Enter College Info...")
                case 2: 
                    search_by_college_code = True
                    search_by_college_name = False
                    button_name += "Code"
                    add_placeholder(input_entry, "Enter College Code...")
                case 3:
                    search_by_college_code = False
                    search_by_college_name = True
                    button_name += "Name"
                    add_placeholder(input_entry, "Enter College Name...")

        toggle_search_button.config(text=button_name)
    
    def toggle_search(index = 1):
        global search_by_Student, search_by_Program, search_by_College
        global toggle_search_by_student_value, toggle_search_by_program_value, toggle_search_by_college_value
        toggle_search_by_student_value, toggle_search_by_program_value, toggle_search_by_college_value = 1, 1, 1

        button_search_student.config(bg= "#B90000", fg= "#FFD700")
        button_search_program.config(bg= "#B90000", fg= "#FFD700")
        button_search_college.config(bg= "#B90000", fg= "#FFD700")
        
        input_value = input_entry.get()
        new_placeholder = False
        if input_value == "": new_placeholder = True
        elif input_value == "Enter Student Info...": new_placeholder = True
        elif input_value == "Enter Program Info...": new_placeholder = True
        elif input_value == "Enter College Info...": new_placeholder = True

        if new_placeholder: window.focus_set()

        match index:
            case 1:
                button_search_student.config(bg= "#ffffff", fg="#000000")
                search_by_Program = False
                search_by_College = False
                search_by_Student = True
                if new_placeholder: add_placeholder(input_entry, "Enter Student Info...")
                toggle_search_by(True)
                toggle_sort_Student(True)
            case 2:
                button_search_program.config(bg= "#ffffff", fg="#000000")
                search_by_Program = True
                search_by_College = False
                search_by_Student = False
                if new_placeholder: add_placeholder(input_entry, "Enter Program Info...")
                toggle_search_by(True)
                toggle_sort_Program(True)
            case 3:
                button_search_college.config(bg= "#ffffff", fg="#000000")
                search_by_Program = False
                search_by_College = True
                search_by_Student = False
                if new_placeholder: add_placeholder(input_entry, "Enter College Info...")
                toggle_search_by(True)
                toggle_sort_College(True)

    def toggle_sort_Student(freeze = False):
        global sort_by_year, sort_by_name, sort_by_program, toggle_sort_student
        button_name = "Sort by: "

        if not freeze:
            if toggle_sort_student == 4: toggle_sort_student = 1
            else: toggle_sort_student += 1

        match toggle_sort_student:
            case 1:
                sort_by_year = False
                sort_by_name = False
                sort_by_program = False
                button_name += "Student ID"
            case 2:
                sort_by_year = False
                sort_by_name = True
                sort_by_program = False
                button_name += "Student Name"
            case 3:
                sort_by_year = False
                sort_by_name = False
                sort_by_program = True  
                button_name += "Student Program"
            case 4:
                sort_by_year = True
                sort_by_name = False
                sort_by_program = False
                button_name += "Student Year"

        toggle_sort_button.config(text=button_name)
        search_student()

    def toggle_sort_Program(freeze = False):
        global sort_by_program_name, sort_by_program_code, toggle_sort_program
        button_name = "Sort by: "

        if not freeze:
            if toggle_sort_program == 3: toggle_sort_program = 1
            else: toggle_sort_program += 1

        match toggle_sort_program:
            case 1:
                sort_by_program_name = False
                sort_by_program_code = False
                button_name += "Program College"
            case 2:
                sort_by_program_name = False
                sort_by_program_code = True
                button_name += "Program Code"
            case 3:
                sort_by_program_name = True
                sort_by_program_code = False
                button_name += "Program Name"

        toggle_sort_button.config(text=button_name)
        search_program()

    def toggle_sort_College(freeze = False):
        global sort_by_college_name, toggle_sort_college
        button_name = "Sort by: "

        if not freeze:
            if toggle_sort_college == 2: toggle_sort_college = 1
            else: toggle_sort_college += 1

        match toggle_sort_college:
            case 1:
                sort_by_college_name = False
                button_name += "College Code"
            case 2:
                sort_by_college_name = True
                button_name += "College Name"

        toggle_sort_button.config(text=button_name)
        search_college()

    def delete_confirm(data_id):

        m, message = "Confirm Delete", f"Are you sure you want to delete "
        if search_by_Student: message += f"Student {data_id}?"
        elif search_by_Program: message += f"Program {data_id}?\nThis would also delete all the Student belong to this Program"
        elif search_by_College: message += f"College {data_id}?\nThis would also delete all the Program and Student belong to this College"
        response = messagebox.askyesno(m, message)

        if response:
            notify = ""
            if search_by_Student:
                CsvDelete.student(data_id)
                search_student()
                notify = f"Student {data_id} "
            elif search_by_Program:
                if CsvSearch.studentProgram(data_id):
                    for student in CsvSearch.studentProgram(data_id):
                        CsvDelete.student(student[0])
                CsvDelete.program(data_id)
                search_program()
                notify = f"Program {data_id} "
            elif search_by_College:
                if CsvSearch.studentCollege(data_id):
                    for student in CsvSearch.studentCollege(data_id):
                        CsvDelete.student(student[0])
                if CsvSearch.programCollege(data_id):
                    for program in CsvSearch.programCollege(data_id):
                        CsvDelete.program(program[1])
                CsvDelete.college(data_id)
                search_college()
                notify = f"College {data_id} "
            
            show_notif (f"{notify} deleted successfully!", color="#e74c3c")

    def open_student_form(student_data=None):
        is_edit = student_data is not None
        form_window = Toplevel(window)
        form_window.title("Edit Student Information" if is_edit else "Add New Student")
        form_window.geometry("350x250")
        form_window.config(bg=bg_color, padx=20, pady=20)
        form_window.resizable(False, False)
        form_window.grab_set()

        college_codes = [row[0] for row in CsvRead.college()[1:]]
        existing_ids = [row[0] for row in CsvRead.student()[1:]]
        tooltip_window = None

        for i in range(6):
            form_window.grid_columnconfigure(i, weight=1)

        def show_tooltip(text, event):
            nonlocal tooltip_window
            if tooltip_window: return
            tooltip_window = Toplevel(form_window)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.config(bg="#ffcccb")
            Label(tooltip_window, text=text, bg="#ffcccb", fg="red", font=("Arial", 8), 
                padx=5, pady=2, relief="solid", borderwidth=1).pack()
            move_tooltip(event)

        def move_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

        def hide_tooltip(event=None):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        Label(form_window, text="Student ID (YYYY-NNNN)", bg=bg_color, font=("Arial", 8, "bold")).grid(row=0, column=0, columnspan=6, sticky=W)
        id_entry = Entry(form_window, highlightthickness=0)
        id_entry.grid(row=1, column=0, columnspan=6, pady=(0, 10), sticky=EW)
        if is_edit:
            id_entry.insert(0, student_data[0])
            id_entry.config(state='readonly', readonlybackground="#f0f0f0")

        Label(form_window, text="Last Name", bg=bg_color).grid(row=2, column=0, columnspan=3, sticky=W)
        Label(form_window, text="First Name", bg=bg_color).grid(row=2, column=3, columnspan=3, sticky=W)
        last_entry = Entry(form_window, highlightthickness=0)
        last_entry.grid(row=3, column=0, columnspan=3, sticky=EW, padx=(0, 5), pady=(0, 10))
        first_entry = Entry(form_window, highlightthickness=0)
        first_entry.grid(row=3, column=3, columnspan=3, sticky=EW, pady=(0, 10))

        Label(form_window, text="College", bg=bg_color).grid(row=4, column=0, sticky=W)
        col_box = ttk.Combobox(form_window, values=college_codes, state="readonly", width=7)
        col_box.grid(row=5, column=0, sticky=W, padx=(0, 5))

        Label(form_window, text="Program", bg=bg_color).grid(row=4, column=1, columnspan=2, sticky=W)
        prog_box = ttk.Combobox(form_window, state="readonly", width=12)
        prog_box.grid(row=5, column=1, columnspan=2, sticky=EW, padx=(0, 5))

        Label(form_window, text="Year", bg=bg_color).grid(row=4, column=3, sticky=W)
        year_box = ttk.Combobox(form_window, values=["1", "2", "3", "4", "5"], state="readonly", width=3)
        year_box.grid(row=5, column=3, sticky=EW, padx=(0, 5))

        Label(form_window, text="Gender", bg=bg_color).grid(row=4, column=4, columnspan=2, sticky=W)
        gen_box = ttk.Combobox(form_window, values=["Male", "Female"], state="readonly", width=7)
        gen_box.grid(row=5, column=4, columnspan=2, sticky=EW)

        if is_edit:
            last_entry.insert(0, student_data[1])
            first_entry.insert(0, student_data[2])
            try:
                current_col = CsvSearch.programCode(student_data[3])[0]
                col_box.set(current_col)
                prog_list = [row[1] for row in CsvSearch.programCollege(current_col)]
                prog_box.config(values=prog_list)
            except: pass
            prog_box.set(student_data[3])
            year_box.set(student_data[4])
            gen_box.set("Male" if student_data[5].upper() == "M" else "Female")

        def validate(event=None):
            id_val, last_val, first_val = id_entry.get().strip(), last_entry.get().strip(), first_entry.get().strip()
            
            id_v, id_err = Constraints.validate_id(id_val, [] if is_edit else existing_ids)
            last_v, last_err = Constraints.validate_name(last_val)
            first_v, first_err = Constraints.validate_name(first_val)

            id_entry.config(highlightthickness=1 if not id_v else 0, highlightbackground="red")
            last_entry.config(highlightthickness=1 if not last_v else 0, highlightbackground="red")
            first_entry.config(highlightthickness=1 if not first_v else 0, highlightbackground="red")

            if all([id_v, last_v, first_v, col_box.get(), prog_box.get(), year_box.get(), gen_box.get()]):
                btn_save.config(state=NORMAL)
                hide_tooltip()
            else:
                btn_save.config(state=DISABLED)
            return (id_v, id_err), (last_v, last_err), (first_v, first_err)

        def save():
            new_student = [id_entry.get(), last_entry.get(), first_entry.get(), 
                        prog_box.get(), year_box.get(), gen_box.get()[0].upper()]
            
            if is_edit:
                CsvReplace.student(student_data[0], new_student)
                show_notif(f"Student {new_student[0]} updated!")
            else:
                CsvWrite.student([new_student])
                show_notif(f"Student {new_student[0]} created!")
                
            form_window.destroy()
            if search_by_Student: search_student()
            elif search_by_Program: search_program()
            else: search_college()

        def on_enter(event):
            (id_v, id_e), (l_v, l_e), (f_v, f_e) = validate(event)
            if event.widget == id_entry and not id_v: show_tooltip(id_e, event)
            elif event.widget == last_entry and not l_v: show_tooltip(l_e, event)
            elif event.widget == first_entry and not f_v: show_tooltip(f_e, event)
            if tooltip_window: event.widget.bind("<Motion>", move_tooltip)

        for entry in [id_entry, last_entry, first_entry]:
            entry.bind("<KeyRelease>", validate)
            entry.bind("<Enter>", on_enter)
            entry.bind("<Leave>", lambda e: (hide_tooltip(), e.widget.unbind("<Motion>")))

        col_box.bind("<<ComboboxSelected>>", lambda e: (
            (progs := CsvSearch.programCollege(col_box.get())),
            prog_box.config(values=[row[1] for row in progs] if progs else []),
            prog_box.set(""), 
            validate()
            ))
        
        for box in [prog_box, year_box, gen_box]: 
            box.bind("<<ComboboxSelected>>", validate)

        btn_save = Button(form_window, text="Save Changes" if is_edit else "Add Student", 
                        bg="#2ecc71", fg=bg_color, font=("Arial", 10, "bold"), 
                        state=DISABLED, command=save)
        btn_save.grid(row=6, column=0, columnspan=6, pady=20, sticky=EW)

        validate()
        form_window.protocol("WM_DELETE_WINDOW", lambda: (hide_tooltip(), form_window.destroy()))

    def open_program_form(program_data=None):
        is_edit = program_data is not None
        old_code = program_data[1] if is_edit else None
        
        form_window = Toplevel(window)
        form_window.title("Edit Program" if is_edit else "Create Program")
        form_window.geometry("400x200") 
        form_window.config(bg=bg_color, padx=20, pady=15)
        form_window.resizable(False, False)
        form_window.grab_set()

        college_codes = [row[0] for row in CsvRead.college()[1:]]
        existing_programs = [row[1] for row in CsvRead.program()[1:]]
        tooltip_window = None

        for i in range(4): 
            form_window.grid_columnconfigure(i, weight=1)

        def show_tooltip(text, event):
            nonlocal tooltip_window
            if tooltip_window: return
            tooltip_window = Toplevel(form_window)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.config(bg="#ffcccb")
            Label(tooltip_window, text=text, bg="#ffcccb", fg="red", font=("Arial", 8), 
                padx=5, pady=2, relief="solid", borderwidth=1).pack()
            move_tooltip(event)

        def move_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

        def hide_tooltip(event=None):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        Label(form_window, text="College Code", bg=bg_color, font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=2, sticky=W)
        col_box = ttk.Combobox(form_window, values=college_codes, state="readonly")
        col_box.grid(row=1, column=0, columnspan=2, pady=(2, 10), sticky=EW, padx=(0, 10))

        Label(form_window, text="Program Code", bg=bg_color, font=("Arial", 9, "bold")).grid(row=0, column=2, columnspan=2, sticky=W)
        code_entry = Entry(form_window, highlightthickness=0)
        code_entry.grid(row=1, column=2, columnspan=2, pady=(2, 10), sticky=EW)

        Label(form_window, text="Program Name", bg=bg_color, font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=4, sticky=W)
        name_entry = Entry(form_window, highlightthickness=0)
        name_entry.grid(row=3, column=0, columnspan=4, pady=(2, 15), sticky=EW)

        if is_edit:
            col_box.set(program_data[0])
            code_entry.insert(0, program_data[1])
            name_entry.insert(0, program_data[2])

        def validate(event=None):
            code_val = code_entry.get().strip()
            name_val = name_entry.get().strip()

            code_v, code_err = Constraints.validate_code(code_val, old_code, existing_programs)
            name_v, name_err = Constraints.validate_name(name_val)

            code_entry.config(highlightthickness=1 if not code_v else 0, highlightbackground="red")
            name_entry.config(highlightthickness=1 if not name_v else 0, highlightbackground="red")

            if all([code_v, name_v, col_box.get()]):
                btn_save.config(state=NORMAL)
                hide_tooltip()
            else:
                btn_save.config(state=DISABLED)
            
            return (code_v, code_err), (name_v, name_err)

        def save():
            new_row = [col_box.get(), code_entry.get().strip(), name_entry.get().strip().upper()]
            
            if is_edit:
                if old_code != new_row[1]:
                    students = CsvSearch.studentProgram(old_code)
                    if students:
                        for s in students: s[3] = new_row[1]
                        CsvWrite.student(students)
                CsvReplace.program(old_code, new_row)
                show_notif(f"Program {new_row[1]} updated!")
            else:
                CsvWrite.program([new_row])
                show_notif(f"Program {new_row[1]} created!")
            
            form_window.destroy()
            if search_by_Student: search_student()
            elif search_by_Program: search_program()
            else: search_college()

        def on_enter(event):
            (c_v, c_err), (n_v, n_err) = validate(event)
            if event.widget == code_entry and not c_v: show_tooltip(c_err, event)
            elif event.widget == name_entry and not n_v: show_tooltip(n_err, event)
            if tooltip_window: event.widget.bind("<Motion>", move_tooltip)

        def on_leave(event):
            hide_tooltip()
            event.widget.unbind("<Motion>")

        for entry in [code_entry, name_entry]:
            entry.bind("<KeyRelease>", validate)
            entry.bind("<Enter>", on_enter)
            entry.bind("<Leave>", on_leave)

        col_box.bind("<<ComboboxSelected>>", validate)

        btn_save = Button(form_window, text="Save Changes" if is_edit else "Add Program", 
                        command=save, bg="#2ecc71", fg=bg_color, font=("Arial", 10, "bold"),
                        state=DISABLED)
        btn_save.grid(row=4, column=0, columnspan=4, pady=(10, 0), sticky=EW)

        validate()
        form_window.protocol("WM_DELETE_WINDOW", lambda: (hide_tooltip(), form_window.destroy()))

    def open_college_form(college_data=None):
        is_edit = college_data is not None
        old_code = college_data[0] if is_edit else None
        
        form_window = Toplevel(window)
        form_window.title("Edit College" if is_edit else "Create College")
        form_window.geometry("400x180") 
        form_window.config(bg=bg_color, padx=20, pady=15)
        form_window.resizable(False, False)
        form_window.grab_set()

        existing_colleges = [row[0] for row in CsvRead.college()[1:]]
        tooltip_window = None

        for i in range(4): 
            form_window.grid_columnconfigure(i, weight=1)

        def show_tooltip(text, event):
            nonlocal tooltip_window
            if tooltip_window: return
            tooltip_window = Toplevel(form_window)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.config(bg="#ffcccb")
            Label(tooltip_window, text=text, bg="#ffcccb", fg="red", font=("Arial", 8), 
                padx=5, pady=2, relief="solid", borderwidth=1).pack()
            move_tooltip(event)

        def move_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

        def hide_tooltip(event=None):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        Label(form_window, text="College Code", bg=bg_color, font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=4, sticky=W)
        code_entry = Entry(form_window, highlightthickness=0)
        code_entry.grid(row=1, column=0, columnspan=4, pady=(2, 10), sticky=EW)

        Label(form_window, text="College Name", bg=bg_color, font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=4, sticky=W)
        name_entry = Entry(form_window, highlightthickness=0)
        name_entry.grid(row=3, column=0, columnspan=4, pady=(2, 15), sticky=EW)

        if is_edit:
            code_entry.insert(0, college_data[0])
            name_entry.insert(0, college_data[1])

        def validate(event=None):
            code_val = code_entry.get().strip()
            name_val = name_entry.get().strip()

            code_v, code_err = Constraints.validate_code(code_val, old_code, existing_colleges)
            name_v, name_err = Constraints.validate_name(name_val)

            code_entry.config(highlightthickness=1 if not code_v else 0, highlightbackground="red")
            name_entry.config(highlightthickness=1 if not name_v else 0, highlightbackground="red")

            if all([code_v, name_v]):
                btn_save.config(state=NORMAL)
                hide_tooltip()
            else:
                btn_save.config(state=DISABLED)
            
            return (code_v, code_err), (name_v, name_err)

        def save():
            new_row = [code_entry.get().strip().upper(), name_entry.get().strip().upper()]
            
            if is_edit:
                if old_code != new_row[0]:
                    progs = CsvSearch.programCollege(old_code)
                    if progs:
                        for p in progs: p[0] = new_row[0]
                        CsvWrite.program(progs)
                CsvReplace.college(old_code, new_row)
                show_notif(f"College {new_row[0]} updated!")
            else:
                CsvWrite.college([new_row])
                show_notif(f"College {new_row[0]} created!")
            
            form_window.destroy()
            if search_by_Student: search_student()
            elif search_by_Program: search_program()
            else: search_college()

        def on_enter(event):
            (c_v, c_err), (n_v, n_err) = validate(event)
            if event.widget == code_entry and not c_v: show_tooltip(c_err, event)
            elif event.widget == name_entry and not n_v: show_tooltip(n_err, event)
            if tooltip_window: event.widget.bind("<Motion>", move_tooltip)

        def on_leave(event):
            hide_tooltip()
            event.widget.unbind("<Motion>")

        for entry in [code_entry, name_entry]:
            entry.bind("<KeyRelease>", validate)
            entry.bind("<Enter>", on_enter)
            entry.bind("<Leave>", on_leave)

        btn_save = Button(form_window, text="Save Changes" if is_edit else "Add College", 
                        command=save, bg="#2ecc71", fg=bg_color, font=("Arial", 10, "bold"),
                        state=DISABLED)
        btn_save.grid(row=4, column=0, columnspan=4, pady=(5, 0), sticky=EW)

        validate()
        form_window.protocol("WM_DELETE_WINDOW", lambda: (hide_tooltip(), form_window.destroy()))

    def show_add_menu():
        add_menu = Menu(window, tearoff=0)
        add_menu.add_command(label="Add Student", command=open_student_form)
        add_menu.add_command(label="Add Program", command=open_program_form)
        add_menu.add_command(label="Add College", command=open_college_form)

        x = add_button.winfo_rootx()
        y = add_button.winfo_rooty() + add_button.winfo_height()
        add_menu.tk_popup(x, y)

    def show_notif(message, color="#00e35f"):
        toast_label = Label(window, text=message, bg=color, fg=bg_color, font=("Arial", 10, "bold"), pady=5)
        toast_label.pack(side=BOTTOM, fill=X)

        def fade_out(): toast_label.destroy()
        window.after(3000, fade_out)

    def on_right_click(event, tree):

        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            if search_by_Student or search_by_College:
                data_value = tree.item(item_id, 'values')
                data_id = data_value[0]
            if search_by_Program:
                data_value = tree.item(item_id, 'values')
                data_id = data_value[1]

            menu = Menu(window, tearoff=0)
            if search_by_Student:
                menu.add_command(label="Edit", command=lambda: open_student_form(data_value))
            elif search_by_Program:
                menu.add_command(label="Edit", command=lambda: open_program_form(data_value))
            elif search_by_College:
                menu.add_command(label="Edit", command=lambda: open_college_form(data_value))
            menu.add_command(label="Delete", command=lambda: delete_confirm(data_id))
            
            menu.post(event.x_root, event.y_root)

    def on_typing(event):
        global search_job
        waiting_time = 200

        if search_job is not None:
            window.after_cancel(search_job)

        if search_by_Student:
            search_job = window.after(waiting_time, search_student)
        elif search_by_Program:
            search_job = window.after(waiting_time, search_program)
        elif search_by_College:
            search_job = window.after(waiting_time, search_college)

    def remove_focus(event):
        if event.widget == window:
            window.focus_set()

    window.bind("<Button-1>", remove_focus)
    input_entry.bind("<KeyRelease>", on_typing)

    toggle_search_button.config(command=toggle_search_by)
    toggle_sort_button.config(command=toggle_sort_Student)
    button_search_student.config(command=lambda: toggle_search(1))
    button_search_program.config(command=lambda: toggle_search(2))
    button_search_college.config(command=lambda: toggle_search(3))
    add_button.config(command=show_add_menu)

    add_placeholder(input_entry, "Enter Student Info...")
    window.after(100, empty_csv_check)
    search_student() 
    CsvSort.All()

    return window

toggle_search_by_student_value, toggle_search_by_program_value, toggle_search_by_college_value = 1, 1, 1
toggle_sort_student, toggle_sort_program, toggle_sort_college = 1, 1, 1
search_by_Student, search_by_Program, search_by_College = True, False, False

search_by_student_ID, search_by_student_name, search_by_student_program = False, False, False
sort_by_name, sort_by_year, sort_by_program = False, False, False

search_by_program_code, search_by_program_name, search_by_program_college = False, False, False
sort_by_program_code, sort_by_program_name = False, False

search_by_college_code, search_by_college_name = False, False
sort_by_college_name = False

search_job = None
