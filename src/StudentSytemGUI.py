from src.csv_core import *
from tkinter import *
from tkinter import ttk
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

    title_icon = Path(__file__).parent.parent / "Images" / "icon.png"
    addS_icon = PhotoImage(file=Path(__file__).parent.parent / "Images" / "addS.png")
    addP_icon = PhotoImage(file=Path(__file__).parent.parent / "Images" / "addP.png")
    addC_icon = PhotoImage(file=Path(__file__).parent.parent / "Images" / "addC.png")
    window.iconphoto(True, PhotoImage(file=title_icon))

    style = ttk.Style()
    style.theme_use('clam') 
    style.configure("Invalid.TCombobox", bordercolor="red",)
    style.configure("TCombobox", bordercolor="#cccccc")

    header = Frame(window, height=30, bg="#B90000")
    header.pack(fill=X)

    header.grid_columnconfigure(0, weight=2)
    header.grid_columnconfigure(1, weight=1) 

    title = Label(header, text="Student Information System",
                font=("Helvetica", 12, "bold"), 
                bg="#B90000", fg="#FFD700")
    title.grid(row=0, column=0, sticky=W, padx=10, pady=10)

    button_frame = Frame(header, bg="#B90000")
    button_frame.grid(row=0, column=1, sticky=E, padx=20)

    button_search_student = Button(button_frame, text="Student", bg="#ffffff",fg = "#000000")
    button_search_program = Button(button_frame, text="Program", bg="#B90000",fg = "#FFD700")
    button_search_college = Button(button_frame, text="College", bg="#B90000",fg = "#FFD700")

    header_buttons = [button_search_student, button_search_program, button_search_college]
    for buttons in header_buttons:
        buttons.pack(side=LEFT, padx=2)
        buttons.config(font=("Helvetica", 9), relief= FLAT, overrelief= FLAT, activebackground="#B90000", 
                       bd=0, highlightthickness=0, borderwidth=0, width=8)

    input_frame = Frame(window, bg=bg_color, width=575)
    input_frame.pack(pady=(20,0), padx=(0,0))

    toggle_search_button = Button(input_frame, width=16,text="Search by: Default")
    input_entry = Entry(input_frame, width=45, font=("Arial", 12), relief=FLAT, background="#cccccc")
    add_button = Button(input_frame,  text = "+", width=2, height=1)

    toggle_search_button.pack(side=LEFT, padx=(0,5))
    input_entry.pack(side=LEFT, padx=5)
    add_button.pack(side=LEFT, padx=(0,5))
    
    output_frame = Frame(window, bg=bg_color)
    output_frame.pack(pady=20)

    # --- GUI Functions ---

    def empty_csv_check():
        if len(CsvRead.student()) > 1:
            return

        overlay = Toplevel(window)
        overlay.overrideredirect(True)
        overlay.configure(bg="black")
        
        ox, oy = window.winfo_rootx(), window.winfo_rooty()
        ow, oh = window.winfo_width(), window.winfo_height()
        overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")

        modal = Toplevel(window)
        modal.withdraw()
        modal.overrideredirect(True)
        modal.configure(bg=bg_color, highlightbackground="#cccccc", highlightthickness=1)
        
        fw, fh = 350, 180 
        modal.geometry(f"{fw}x{fh}+{ox + (ow//2) - (fw//2)}+{oy + (oh//2) - (fh//2)}")

        def hide_modal():
            window.unbind("<Configure>")
            modal.grab_release()
            modal.destroy()
            overlay.destroy()

        def sync_positions(event=None):
            if modal.winfo_exists() and modal.winfo_viewable():
                nox, noy = window.winfo_rootx(), window.winfo_rooty()
                now, noh = window.winfo_width(), window.winfo_height()
                overlay.geometry(f"{now}x{noh}+{nox}+{noy}")
                overlay.lift()
                modal.geometry(f"+{nox + (now // 2) - (fw // 2)}+{noy + (noh // 2) - (fh // 2)}")
                modal.lift()

        window.bind("<Configure>", sync_positions)

        container = Frame(modal, bg=bg_color, padx=20, pady=20)
        container.pack(fill=BOTH, expand=True)

        Label(container, text="Generate Data?", bg=bg_color, font=("Arial", 11, "bold"), fg="#333").pack(pady=(0, 10))
        Label(container, text="It looks like your CSV files are empty.\nWould you like to generate 100\nrandom student records?", 
              bg=bg_color, justify=CENTER, font=("Arial", 9)).pack(pady=5)

        btn_frame = Frame(container, bg=bg_color)
        btn_frame.pack(side=BOTTOM, pady=(10, 0))

        def on_yes():
            RanCsvGen.generate_random_student()
            search_student()
            hide_modal()
            show_notif("100 Random Students Added")

        Button(btn_frame, text="Yes, Generate", bg="#2ecc71", fg="white", width=12, relief="flat", command=on_yes).pack(side=LEFT, padx=5)
        Button(btn_frame, text="No, Thanks", bg="#95a5a6", fg="white", width=12, relief="flat", command=hide_modal).pack(side=LEFT, padx=5)

        # Activation
        overlay.update_idletasks()
        overlay.deiconify()
        overlay.attributes("-alpha", 0.5)
        modal.deiconify()
        modal.lift()
        modal.grab_set()
 
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

    def treeview_sort_column(tree, col, reverse):
        global current_sort_col, current_sort_reverse
        current_sort_col, current_sort_reverse = col, reverse

        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        try:
            l.sort(key=lambda t: int(t[0]) if t[0].isdigit() else t[0].lower(), reverse=reverse)
        except Exception:
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        for column in tree['columns']:
            tree.heading(column, text=column.title())

        arrow = " ↓" if reverse else " ↑"
        tree.heading(col, text=col.title() + arrow,
                    command=lambda: treeview_sort_column(tree, col, not reverse))

    def search_student():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()

        def display_result(data):
            def handle_click(event):
                if tree.identify_region(event.x, event.y) == "separator":
                    return "break"

            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            headers = CsvRead.student()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings", height=11)
            tree.pack(fill=BOTH, expand=TRUE)

            for i in range (len(headers)):
                h = headers[i]
                tree.heading(h, text=h.title(),
                             command= lambda c = h: treeview_sort_column(tree, c, False))
                if i == 0: tree.column(h, width=75, anchor=CENTER)
                elif i == 1: tree.column(h, width=150, )
                elif i == 2: tree.column(h, width=150)
                elif i == 3: tree.column(h, width=100)
                elif i == 4: tree.column(h, width=50, anchor=CENTER)
                elif i == 5: tree.column(h, width=50, anchor=CENTER)
                tree.column(h, stretch=False)

            for item in data:
                tree.insert("", END, values=item,)

            if current_sort_col in headers:
                treeview_sort_column(tree, current_sort_col, current_sort_reverse)

            tree.bind('<Button-1>', handle_click)
            tree.bind("<Button-3>", lambda event: on_right_click(event, tree))
            tree.bind("<B1-Motion>", lambda event: on_left_drag_select(event, tree))

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
            else: 
                students = CsvRead.student()[1:]
                result = [row for row in students 
                          if input_text.lower() in row[0].lower().replace("-","") or
                          input_text.lower() in row[1].lower() or
                          input_text.lower() in row[2].lower() or
                          input_text.lower() in row[3].lower().replace("-","") or
                          input_text.lower() in row[4].lower() or
                          input_text.lower() in row[5].lower()]
                          
        display_result(result)

    def search_program():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()

        def display_result(data):
            def handle_click(event):
                if tree.identify_region(event.x, event.y) == "separator":
                    return "break" 

            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            headers = CsvRead.program()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings", height=11)
            tree.pack(fill=BOTH, expand=True)

            for i in range(len(headers)):
                h = headers[i]
                tree.heading(h, text=h.title(),
                             command= lambda c = h: treeview_sort_column(tree, c, False))
                if i == 0: tree.column(h, width=90, anchor=CENTER)
                elif i == 1: tree.column(h, width=100)
                elif i == 2: tree.column(h, width=385)

            for item in data:
                tree.insert("", END, values=item)

            if current_sort_col in headers:
                treeview_sort_column(tree, current_sort_col, current_sort_reverse)

            tree.bind('<Button-1>', handle_click)
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
            else: 
                programs = CsvRead.program()[1:]
                result = [row for row in programs if 
                          input_text.lower() in row[0].lower().replace("-","") or
                          input_text.lower() in row[1].lower().replace("-","") or
                          input_text.lower() in row[2].lower()]

        display_result(result)

    def search_college():
        for widget in output_frame.winfo_children():
            widget.destroy()

        input_text = input_entry.get().strip()
        
        def display_result(data):
            def handle_click(event):
                if tree.identify_region(event.x, event.y) == "separator":
                    return "break"

            if data is None or data == []:
                Label(output_frame, text="No results found.", bg=bg_color, fg="Red", font=("Arial", 12)).pack()
                return
            if not isinstance(data, list): data = [data]

            headers = CsvRead.college()[0]
            tree = ttk.Treeview(output_frame, columns=headers, show="headings", height=11)
            tree.pack(fill=BOTH, expand=True)

            for i in range(len(headers)):
                h = headers[i]
                tree.heading(h, text=h.title(),
                             command= lambda c = h: treeview_sort_column(tree, c, False))
                if i == 0: tree.column(h, width=100, anchor=CENTER)
                elif i == 1: tree.column(h, width=475)

            for item in data:
                tree.insert("", END, values=item)

            if current_sort_col in headers:
                treeview_sort_column(tree, current_sort_col, current_sort_reverse)

            tree.bind('<Button-1>', handle_click)
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

        Placeholders = [["Enter Student Info...", "Enter Student ID...",
                         "Enter Student Name...", "Enter Student Program..."],
                        ["Enter Program Info...", "Enter Program Code...",
                         "Enter Program Name...", "Enter Program College..."],
                        ["Enter College Info...", "Enter College Code...",
                         "Enter College Name..."]]

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
                    add_placeholder(input_entry, Placeholders[0][0])
                case 2:
                    search_by_student_ID = True
                    search_by_student_name = False
                    search_by_student_program = False
                    button_name += "ID"
                    add_placeholder(input_entry, Placeholders[0][1])
                case 3:
                    search_by_student_ID = False
                    search_by_student_name = True
                    search_by_student_program = False
                    button_name += "Name"
                    add_placeholder(input_entry, Placeholders[0][2])
                case 4:
                    search_by_student_ID = False
                    search_by_student_name = False
                    search_by_student_program = True
                    button_name += "Program"
                    add_placeholder(input_entry, Placeholders[0][3])

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
                    add_placeholder(input_entry, Placeholders[1][0])
                case 2:
                    search_by_program_code = True
                    search_by_program_name = False
                    search_by_program_college = False
                    button_name += "Code"
                    add_placeholder(input_entry, Placeholders[1][1])
                case 3:
                    search_by_program_code = False
                    search_by_program_name = True
                    search_by_program_college = False
                    button_name += "Name"
                    add_placeholder(input_entry, Placeholders[1][2])
                case 4:
                    search_by_program_code = False
                    search_by_program_name = False
                    search_by_program_college = True
                    button_name += "College"
                    add_placeholder(input_entry, Placeholders[1][3])

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
                    add_placeholder(input_entry, Placeholders[2][0])
                case 2: 
                    search_by_college_code = True
                    search_by_college_name = False
                    button_name += "Code"
                    add_placeholder(input_entry, Placeholders[2][1])
                case 3:
                    search_by_college_code = False
                    search_by_college_name = True
                    button_name += "Name"
                    add_placeholder(input_entry, Placeholders[2][2])

        toggle_search_button.config(text=button_name)
    
    def toggle_search(index = 1):
        global search_by_Student, search_by_Program, search_by_College
        global current_sort_col, current_sort_reverse
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
                current_sort_col = "Student ID"
                button_search_student.config(bg= "#ffffff", fg="#000000")
                search_by_Program = False
                search_by_College = False
                search_by_Student = True
                if new_placeholder: add_placeholder(input_entry, "Enter Student Info...")
                toggle_search_by(True)
                search_student()
            case 2:
                current_sort_col = "Program Code"
                button_search_program.config(bg= "#ffffff", fg="#000000")
                search_by_Program = True
                search_by_College = False
                search_by_Student = False
                if new_placeholder: add_placeholder(input_entry, "Enter Program Info...")
                toggle_search_by(True)
                search_program()
            case 3:
                current_sort_col = "College Code"
                button_search_college.config(bg= "#ffffff", fg="#000000")
                search_by_Program = False
                search_by_College = True
                search_by_Student = False
                if new_placeholder: add_placeholder(input_entry, "Enter College Info...")
                toggle_search_by(True)
                search_college()

    def delete_confirm(data_id):

        overlay = Toplevel(window)
        overlay.overrideredirect(True)
        overlay.configure(bg="black")
        overlay.attributes("-alpha", 0.5)
        
        ox = window.winfo_rootx()
        oy = window.winfo_rooty()
        ow = window.winfo_width()
        oh = window.winfo_height()
        overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")

        preview_window = Toplevel(window)
        preview_window.overrideredirect(True)
        preview_window.configure(bg=bg_color, highlightbackground="#cccccc", highlightthickness=1)
        
        fw, fh = 420, 480 

        def hide_modal():
            window.unbind("<Configure>")
            preview_window.grab_release()
            preview_window.destroy()
            overlay.destroy()

        def sync_positions(event=None):
            if preview_window.winfo_exists() and preview_window.winfo_viewable():
                ox = window.winfo_rootx()
                oy = window.winfo_rooty()
                ow = window.winfo_width()
                oh = window.winfo_height()
                overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")
                overlay.deiconify()
                fx = ox + (ow // 2) - (fw // 2)
                fy = oy + (oh // 2) - (fh // 2)
                preview_window.geometry(f"+{fx}+{fy}")
                preview_window.deiconify()

        window.bind("<Configure>", sync_positions)

        container = Frame(preview_window, bg=bg_color)
        container.pack(fill=BOTH, expand=True, padx=15, pady=15)

        students_to_delete = []
        programs_to_delete = []

        # STUDENT DELETE

        is_bulk = isinstance(data_id, list)

        if search_by_Student:
            if is_bulk:
                fw, fh = 300, 240
                Label(
                    container, text=f"⚠ Are you sure you \nwant to delete {len(data_id)} Students?",
                    bg=bg_color, fg="#e9240e", font=("Arial", 11, "bold")
                ).pack(pady=(5,0))

                frame = Frame(container)
                frame.pack(fill=BOTH, expand=True, pady=5)

                tree = ttk.Treeview(frame, columns=("Student ID",),
                    show="headings", height=3)

                scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side="left", fill=BOTH, expand=True)
                scrollbar.pack(side="right", fill="y")

                tree.heading("Student ID", text="Student ID")
                tree.column("Student ID", width=200, anchor=CENTER)

                for row in data_id:
                    tree.insert("", END, values=(row))

            else:
                fw, fh = 420, 150
                Label(
                    container, text=f"⚠ Are you sure you want to delete Student?",
                    bg=bg_color, fg="#e9240e", font=("Arial", 11, "bold")
                ).pack(pady=(5,0))
                Label(container, text=f"{data_id}?",
                    bg=bg_color, fg="#000000", font=("Arial", 12, "bold")
                ).pack(pady=(0,0))

        # PROGRAM DELETE

        elif search_by_Program:
            fw, fh = 300, 270

            all_students = CsvRead.student()[1:]
            students_to_delete = [row for row in all_students if row[3] == data_id]

            Label(
                container,
                text=f"⚠ Deleting Program {data_id}\nwill also delete:",
                bg=bg_color, fg="#e9240e", font=("Arial", 11, "bold")
            ).pack(pady=5)

            if students_to_delete:

                frame = Frame(container)
                frame.pack(fill=BOTH, expand=True, pady=5)

                tree = ttk.Treeview(frame, columns=("Student ID",),
                    show="headings", height=4)

                scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side="left", fill=BOTH, expand=True)
                scrollbar.pack(side="right", fill="y")

                tree.heading("Student ID", text="Student ID")
                tree.column("Student ID", width=200, anchor=CENTER)

                for row in students_to_delete:
                    tree.insert("", END, values=(row[0],))

            else:
                fw, fh = 300, 170
                Label(container, text="No students affected.", bg=bg_color).pack(pady=(10,0))

        # COLLEGE DELETE

        elif search_by_College:

            all_programs = CsvRead.program()[1:]
            programs_to_delete = [row for row in all_programs if row[0] == data_id]

            all_students = CsvRead.student()[1:]
            program_codes = [p[1] for p in programs_to_delete]
            students_to_delete = [row for row in all_students if row[3] in program_codes]

            Label(container, text=f"⚠ Deleting College {data_id} will also delete:",
                bg=bg_color, fg="#e9240e", font=("Arial", 10, "bold")
            ).pack(pady=5)

            if programs_to_delete:
                fw, fh = (480, 420) if students_to_delete else (480, 270)

                Label(container, text=f"{len(programs_to_delete)} Programs", fg="blue", bg=bg_color)\
                    .pack(pady=(10, 0))

                prog_frame = Frame(container)
                prog_frame.pack(fill="x", pady=5)

                prog_tree = ttk.Treeview(
                    prog_frame,
                    columns=("Program Code",),
                    show="headings",
                    height=4
                )

                prog_scroll = Scrollbar(prog_frame, orient="vertical",
                                        command=prog_tree.yview)
                prog_tree.configure(yscrollcommand=prog_scroll.set)

                prog_tree.pack(side="left", fill=BOTH, expand=True)
                prog_scroll.pack(side="right", fill="y")

                prog_tree.heading("Program Code", text="Program Code")
                prog_tree.column("Program Code", width=250, anchor=CENTER)

                for row in programs_to_delete:
                    prog_tree.insert("", END, values=(row[1],))

            if students_to_delete:

                Label(container, text=f"{len(students_to_delete)} Students", fg="blue", bg=bg_color)\
                    .pack(pady=(10, 0))

                stu_frame = Frame(container)
                stu_frame.pack(fill=BOTH, expand=True, pady=5)

                stu_tree = ttk.Treeview(
                    stu_frame,
                    columns=("Student ID", "Program Code"),
                    show="headings",
                    height=4
                )

                stu_scroll = Scrollbar(stu_frame, orient="vertical",
                                    command=stu_tree.yview)
                stu_tree.configure(yscrollcommand=stu_scroll.set)

                stu_tree.pack(side="left", fill=BOTH, expand=True)
                stu_scroll.pack(side="right", fill="y")

                stu_tree.heading("Student ID", text="Student ID")
                stu_tree.heading("Program Code", text="Program Code")

                stu_tree.column("Student ID", width=150, anchor=CENTER)
                stu_tree.column("Program Code", width=150, anchor=CENTER)

                students_to_delete = sorted(students_to_delete, key=lambda x: x[3])

                for row in students_to_delete:
                    stu_tree.insert("", END, values=(row[0], row[3]))

            if not programs_to_delete and not students_to_delete:
                fw, fh = 480, 170
                Label(container,
                    text="No dependent records found.",
                    bg=bg_color).pack(pady=10)

        btn_frame = Frame(preview_window, bg=bg_color)
        btn_frame.pack(pady=(5,10))

        fx = ox + (ow // 2) - (fw // 2)
        fy = oy + (oh // 2) - (fh // 2)
        preview_window.geometry(f"{fw}x{fh}+{fx}+{fy}")

        def confirm_delete():

            if search_by_Student:
                if is_bulk: 
                    for Id in data_id: CsvDelete.student(Id)
                else: CsvDelete.student(data_id)
                search_student()

            elif search_by_Program:
                for student in students_to_delete:
                    CsvDelete.student(student[0])
                CsvDelete.program(data_id)
                search_program()

            elif search_by_College:
                for student in students_to_delete:
                    CsvDelete.student(student[0])
                for program in programs_to_delete:
                    CsvDelete.program(program[1])
                CsvDelete.college(data_id)
                search_college()

            hide_modal()
            if is_bulk:
                show_notif(f"{len(data_id)} Students deleted successfully!", color="#e74c3c")
            else:
                show_notif(f"{data_id} deleted successfully!", color="#e74c3c")

        Label(container, text=f"⚠ This Action Cannot be Undone",
                bg=bg_color, fg="#e9240e", font=("Arial", 8, "bold")
            ).pack(pady=(0, 0))

        Button(btn_frame, text="Confirm", bg="#e74c3c", fg="white", 
               width=12, command=confirm_delete).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Cancel", width=12, command=hide_modal).pack(side=LEFT)

        overlay.update_idletasks()
        overlay.deiconify()
        overlay.attributes("-alpha", 0.5)
        
        preview_window.deiconify()
        preview_window.lift()
        preview_window.focus_force()
        preview_window.grab_set()

    def open_student_form(student_data=None):
        is_edit = student_data is not None
        
        overlay = Toplevel(window)
        overlay.overrideredirect(True)
        overlay.configure(bg="black")
        overlay.attributes("-alpha", 0.5)
        
        ox = window.winfo_rootx()
        oy = window.winfo_rooty()
        ow = window.winfo_width()
        oh = window.winfo_height()
        overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")

        form_window = Toplevel(window)
        form_window.overrideredirect(True)
        form_window.configure(bg=bg_color, highlightbackground="#cccccc", highlightthickness=1)
        
        fw, fh = 350, 270 
        fx = ox + (ow // 2) - (fw // 2)
        fy = oy + (oh // 2) - (fh // 2)
        form_window.geometry(f"{fw}x{fh}+{fx}+{fy}")

        overlay.update_idletasks()
        overlay.deiconify()
        form_window.update_idletasks()
        form_window.deiconify()
        
        form_window.grab_set()

        def hide_modal():
            if tooltip_window: tooltip_window.destroy()
            form_window.grab_release()
            form_window.destroy()
            overlay.destroy()

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

        def start_drag(event):
            form_window._x, form_window._y = event.x, event.y

        def do_drag(event):
            nx = form_window.winfo_x() + event.x - form_window._x
            ny = form_window.winfo_y() + event.y - form_window._y
            form_window.geometry(f"+{max(ox, min(nx, ox + ow - fw))}+{max(oy, min(ny, oy + oh - fh))}")

        def sync_positions(event=None):
            if form_window.winfo_exists() and form_window.winfo_viewable():
                ox = window.winfo_rootx()
                oy = window.winfo_rooty()
                ow = window.winfo_width()
                oh = window.winfo_height()
                overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")
                overlay.deiconify()
                fx = ox + (ow // 2) - (fw // 2)
                fy = oy + (oh // 2) - (fh // 2)
                form_window.geometry(f"+{fx}+{fy}")
                form_window.deiconify()

        container = Frame(form_window, bg=bg_color, padx=20, pady=15)
        container.pack(fill=BOTH, expand=True)
        container.bind("<Button-1>", start_drag)
        container.bind("<B1-Motion>", do_drag)
        window.bind("<Configure>", sync_positions)

        college_codes = [row[0] for row in CsvRead.college()[1:]]
        existing_ids = [row[0] for row in CsvRead.student()[1:]]
        tooltip_window = None

        for i in range(6):
            container.grid_columnconfigure(i, weight=1)

        Label(container, text="Edit Student" if is_edit else "Create Student", bg=bg_color, 
              font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 10))

        Label(container, text="Student ID (YYYY-NNNN)", bg=bg_color, 
              font=("Arial", 8, "bold")).grid(row=1, column=0, columnspan=6, sticky=W)
        id_entry = Entry(container, highlightthickness=0, bd=1, relief="solid")
        id_entry.grid(row=2, column=0, columnspan=6, pady=(0, 10), sticky=EW)
        
        if is_edit:
            id_entry.insert(0, student_data[0])
            id_entry.config(state='readonly', readonlybackground="#f0f0f0")

        Label(container, text="Last Name", bg=bg_color).grid(row=3, column=0, columnspan=3, sticky=W)
        Label(container, text="First Name", bg=bg_color).grid(row=3, column=3, columnspan=3, sticky=W)
        last_entry = Entry(container, highlightthickness=0, bd=1, relief="solid")
        last_entry.grid(row=4, column=0, columnspan=3, sticky=EW, padx=(0, 5), pady=(0, 10))
        first_entry = Entry(container, highlightthickness=0, bd=1, relief="solid")
        first_entry.grid(row=4, column=3, columnspan=3, sticky=EW, pady=(0, 10))

        Label(container, text="College", bg=bg_color).grid(row=5, column=0, sticky=W)
        Label(container, text="Program", bg=bg_color).grid(row=5, column=1, columnspan=2, sticky=W)
        Label(container, text="Year", bg=bg_color).grid(row=5, column=3, sticky=W)
        Label(container, text="Gender", bg=bg_color).grid(row=5, column=4, columnspan=2, sticky=W)

        col_box = ttk.Combobox(container, values=college_codes, state="readonly", width=5)
        col_box.grid(row=6, column=0, sticky=W, padx=(0, 5))
        prog_box = ttk.Combobox(container, state="readonly", width=10)
        prog_box.grid(row=6, column=1, columnspan=2, sticky=EW, padx=(0, 5))
        year_box = ttk.Combobox(container, values=["1", "2", "3", "4", "5"], state="readonly", width=3)
        year_box.grid(row=6, column=3, sticky=EW, padx=(0, 5))
        gen_box = ttk.Combobox(container, values=["Male", "Female"], state="readonly", width=7)
        gen_box.grid(row=6, column=4, columnspan=2, sticky=EW)

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
            id_val = id_entry.get().strip()
            last_val = last_entry.get().strip()
            first_val = first_entry.get().strip()
            
            id_v, id_err = Constraints.validate_id(id_val, [] if is_edit else existing_ids)
            last_v, last_err = Constraints.validate_name(last_val)
            first_v, first_err = Constraints.validate_name(first_val)

            id_entry.config(highlightthickness=1 if not id_v else 0, highlightbackground="red")
            last_entry.config(highlightthickness=1 if not last_v else 0, highlightbackground="red")
            first_entry.config(highlightthickness=1 if not first_v else 0, highlightbackground="red")

            combos = [col_box, prog_box, year_box, gen_box]
            for cb in combos:
                if cb.get()=="":
                    cb.config(style="Invalid.TCombobox")
                else:
                    cb.config(style="TCombobox")

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
                
            hide_modal()
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

        btn_frame = Frame(container, bg=bg_color)
        btn_frame.grid(row=7, column=0, columnspan=6, pady=(20, 0), sticky=EW)

        btn_save = Button(btn_frame, text="Save Changes" if is_edit else "Add Student", 
                        bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), 
                        state=DISABLED, command=save)
        btn_save.pack(side=RIGHT, padx=5)

        btn_cancel = Button(btn_frame, text="Cancel", command=hide_modal, bg="#e74c3c", fg="white")
        btn_cancel.pack(side=RIGHT, padx=5)

        validate()
        
    def open_program_form(program_data=None):
        is_edit = program_data is not None
        old_code = program_data[1] if is_edit else None
        
        overlay = Toplevel(window)
        overlay.overrideredirect(True)
        overlay.configure(bg="black")
        overlay.attributes("-alpha", 0.5)
        
        ox = window.winfo_rootx()
        oy = window.winfo_rooty()
        ow = window.winfo_width()
        oh = window.winfo_height()
        overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")

        form_window = Toplevel(window)
        form_window.overrideredirect(True)
        form_window.config(bg=bg_color, highlightbackground="#cccccc", highlightthickness=1)
        
        fw, fh = 320, 200 
        fx, fy = ox + (ow // 2) - (fw // 2), oy + (oh // 2) - (fh // 2)
        form_window.geometry(f"{fw}x{fh}+{fx}+{fy}")

        overlay.update_idletasks()
        overlay.deiconify()
        form_window.update_idletasks()
        form_window.deiconify()
        form_window.grab_set()

        def hide_modal():
            if tooltip_window: tooltip_window.destroy()
            form_window.destroy()
            overlay.destroy()

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

        def start_drag(event):
            form_window._x, form_window._y = event.x, event.y
        def do_drag(event):
            nx = form_window.winfo_x() + event.x - form_window._x
            ny = form_window.winfo_y() + event.y - form_window._y
            form_window.geometry(f"+{max(ox, min(nx, ox + ow - fw))}+{max(oy, min(ny, oy + oh - fh))}")
        def sync_positions(event=None):
            if form_window.winfo_exists() and form_window.winfo_viewable():
                ox = window.winfo_rootx()
                oy = window.winfo_rooty()
                ow = window.winfo_width()
                oh = window.winfo_height()
                overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")
                overlay.deiconify()
                fx = ox + (ow // 2) - (fw // 2)
                fy = oy + (oh // 2) - (fh // 2)
                form_window.geometry(f"+{fx}+{fy}")
                form_window.deiconify()

        container = Frame(form_window, bg=bg_color, padx=20, pady=15)
        container.pack(fill=BOTH, expand=True)
        container.bind("<Button-1>", start_drag); container.bind("<B1-Motion>", do_drag)
        window.bind("<Configure>", sync_positions)

        college_codes = [row[0] for row in CsvRead.college()[1:]]
        existing_programs = [row[1] for row in CsvRead.program()[1:]]
        tooltip_window = None

        for i in range(6):
            container.grid_columnconfigure(i, weight=1)

        Label(container, text="Edit Program" if is_edit else "Create Program", bg=bg_color, 
              font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 10))

        Label(container, text="College Code", bg=bg_color, 
              font=("Arial", 9, "bold")).grid(row=1, column=0, columnspan=3, sticky=W)
        col_box = ttk.Combobox(container, values=college_codes, state="readonly")
        col_box.grid(row=2, column=0, columnspan=3, pady=(2, 10), sticky=EW, padx=(0, 10))

        Label(container, text="Program Code", bg=bg_color, 
              font=("Arial", 9, "bold")).grid(row=1, column=3, columnspan=6, sticky=W)
        code_entry = Entry(container, highlightthickness=0)
        code_entry.grid(row=2, column=3, columnspan=6, pady=(2, 10), sticky=EW)

        Label(container, text="Program Name", bg=bg_color, 
              font=("Arial", 9, "bold")).grid(row=3, column=0, columnspan=6, sticky=W)
        name_entry = Entry(container, highlightthickness=0)
        name_entry.grid(row=4, column=0, columnspan=6, pady=(2, 15), sticky=EW)

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

            if col_box.get() == "":
                col_box.config(style="Invalid.TCombobox")
            else:
                col_box.config(style="TCombobox")
        
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
            
            hide_modal()
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

        btn_frame = Frame(container, bg=bg_color)
        btn_frame.grid(row=5, column=0, columnspan=6, pady=(0, 10), sticky=EW)

        btn_save = Button(btn_frame, text="Save Changes" if is_edit else "Create Programs", 
                          command=save,bg="#2ecc71", fg="white", state=DISABLED)
        btn_save.pack(side=RIGHT, padx=5)
        Button(btn_frame, text="Cancel", command=hide_modal, 
               bg="#e74c3c", fg="white").pack(side=RIGHT)

        validate()
        form_window.protocol("WM_DELETE_WINDOW", lambda: (hide_tooltip(), form_window.destroy()))

    def open_college_form(college_data=None):
        is_edit = college_data is not None
        old_code = college_data[0] if is_edit else None
        
        overlay = Toplevel(window)
        overlay.overrideredirect(True)
        overlay.configure(bg="black")
        overlay.attributes("-alpha", 0.5)

        ox = window.winfo_rootx()
        oy = window.winfo_rooty()
        ow = window.winfo_width()
        oh = window.winfo_height()
        overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")

        form_window = Toplevel(window)
        form_window.overrideredirect(True)
        form_window.configure(bg=bg_color, highlightbackground="#cccccc", highlightthickness=1)

        fw, fh = 400, 220
        form_window.geometry(f"{fw}x{fh}+{ox + (ow//2) - (fw//2)}+{oy + (oh//2) - (fh//2)}")

        overlay.update_idletasks()
        overlay.deiconify()
        form_window.update_idletasks()
        form_window.deiconify()
        form_window.grab_set()

        def hide_modal():
            if tooltip_window: tooltip_window.destroy()
            form_window.destroy(); overlay.destroy()

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

        def start_drag(event):
            form_window._x, form_window._y = event.x, event.y

        def do_drag(event):
            nx = form_window.winfo_x() + event.x - form_window._x
            ny = form_window.winfo_y() + event.y - form_window._y
            form_window.geometry(f"+{max(ox, min(nx, ox + ow - fw))}+{max(oy, min(ny, oy + oh - fh))}")

        def sync_positions(event=None):
            if form_window.winfo_exists() and form_window.winfo_viewable():
                ox = window.winfo_rootx()
                oy = window.winfo_rooty()
                ow = window.winfo_width()
                oh = window.winfo_height()
                overlay.geometry(f"{ow}x{oh}+{ox}+{oy}")
                overlay.deiconify()
                fx = ox + (ow // 2) - (fw // 2)
                fy = oy + (oh // 2) - (fh // 2)
                form_window.geometry(f"+{fx}+{fy}")
                form_window.deiconify()

        container = Frame(form_window, bg=bg_color, padx=20, pady=15)
        container.pack(fill=BOTH, expand=True)
        container.bind("<Button-1>", start_drag); container.bind("<B1-Motion>", do_drag)
        window.bind("<Configure>", sync_positions)

        existing_colleges = [row[0] for row in CsvRead.college()[1:]]
        tooltip_window = None

        for i in range(4): 
            container.grid_columnconfigure(i, weight=1)

        Label(container, text="Edit College" if is_edit else "Create College", bg=bg_color, 
              font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10))

        Label(container, text="College Code", bg=bg_color, 
              font=("Arial", 9, "bold")).grid(row=1, column=0, columnspan=4, sticky=W)
        code_entry = Entry(container, highlightthickness=0)
        code_entry.grid(row=2, column=0, columnspan=4, pady=(2, 10), sticky=EW)

        Label(container, text="College Name", bg=bg_color, 
              font=("Arial", 9, "bold")).grid(row=3, column=0, columnspan=4, sticky=W)
        name_entry = Entry(container, highlightthickness=0)
        name_entry.grid(row=4, column=0, columnspan=4, pady=(2, 15), sticky=EW)

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
            
            hide_modal()
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

        btn_frame = Frame(container, bg=bg_color)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=(5, 0), sticky=E)

        btn_save = Button(btn_frame, text="Save Changes" if is_edit else "Create College", 
                          bg="#2ecc71", fg="white", state=DISABLED, command=save)
        btn_save.pack(side=RIGHT, padx=5)
        Button(btn_frame, text="Cancel", command=hide_modal, 
               bg="#e74c3c", fg="white").pack(side=RIGHT)

        validate()
        form_window.protocol("WM_DELETE_WINDOW", lambda: (hide_tooltip(), form_window.destroy()))

    def show_add_menu():
        add_menu = Menu(window, tearoff=0)
        add_menu.add_command(image=addS_icon, label="Add Student", 
                             command=open_student_form, compound=LEFT)
        add_menu.add_command(image=addP_icon, label="Add Program", 
                             command=open_program_form, compound=LEFT)
        add_menu.add_command(image=addC_icon, label="Add College", 
                             command=open_college_form, compound=LEFT)

        x = add_button.winfo_rootx()
        y = add_button.winfo_rooty() + add_button.winfo_height()
        add_menu.tk_popup(x, y)
        add_menu.config()

    def show_notif(message, color="#00e35f"):
        toast_label = Label(window, text=message, bg=color, fg=bg_color, font=("Arial", 10, "bold"), pady=5)
        toast_label.pack(side=BOTTOM, fill=X)

        def fade_out(): toast_label.destroy()
        window.after(3000, fade_out)

    def on_left_drag_select(event, tree):
        item_id = tree.identify_row(event.y)
        
        if item_id:
            current_selection = list(tree.selection())

            if item_id not in current_selection:
                current_selection.append(item_id)
                tree.selection_set(current_selection)

                tree.see(item_id)

    def on_right_click(event, tree):
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
            
        selected_items = tree.selection()
        
        if search_by_Student:
            if (item_id not in selected_items):
                tree.selection_set(item_id)
                selected_items = (item_id,)
        else:
            tree.selection_set(item_id)
            selected_items = (item_id,)

        menu = Menu(window, tearoff=0)

        if search_by_Student and len(selected_items) > 1:
            all_ids = [tree.item(item, 'values')[0] for item in selected_items]
            
            menu.add_command(
                label=f"Delete {len(selected_items)} Selected Students", 
                command=lambda: delete_confirm(all_ids)
            )
        else:
            data_value = tree.item(item_id, 'values')
            data_id = data_value[1] if search_by_Program else data_value[0]

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
    button_search_student.config(command=lambda: toggle_search(1))
    button_search_program.config(command=lambda: toggle_search(2))
    button_search_college.config(command=lambda: toggle_search(3))
    add_button.config(command=show_add_menu)

    add_placeholder(input_entry, "Enter Student Info...")
    window.after(100, empty_csv_check)
    search_student() 
    CsvSort.All()

    return window

current_sort_col, current_sort_reverse = "Student ID", False

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
