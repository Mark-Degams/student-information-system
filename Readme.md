# Simple Student Information System 🎓

A lightweight student information manager with a Tkinter GUI that stores data in CSV files. Built for educational purposes (`CSC151`), it lets you create, edit, search, sort, and delete Colleges, Programs, and Students using simple CSV-backed storage.

## ✨ Features

| Feature | Description |
|---|---|
| GUI 🖥️ | Graphical interface built with `tkinter` for browsing and managing records |
| CSV Storage 💾 | Uses `CSV_Files/College.csv`, `CSV_Files/Program.csv`, `CSV_Files/Student.csv` (no DB required) |
| CRUDL ✍️ | Create, Read, Update, Delete, and List for Students, Programs, and Colleges |
| Search 🔎 | Search by ID, name, program, college, year, gender — supports multi-key queries |
| Validation ✅ | Enforces code, name, and Student ID (`YYYY-NNNN`) rules via `src/Constraints.py` |
| Data Generator 🧪 | Bulk random data generator (5000 students) for testing/demo (`src/RanCsvGen.py`) |

## 🛠 Requirements

- Python 3.10+ (uses `match`/pattern matching syntax)
- Standard library only: `tkinter`, `csv`, `pathlib`, etc. No third-party packages required.

## ▶️ Quickstart

1. Clone or download the repository.
2. From the project root, run:

```bash
python main.py
```

The app will create the `CSV_Files/` folder and header rows if they don't exist.

On first run, if CSVs are empty the GUI offers to generate 5000 random student records. You can also add Colleges/Programs/Students from the Add menu.

You can also generate sample data from the command line:

```bash
python -c "from src.RanCsvGen import generate_random_student; generate_random_student()"
```

## 📁 Project Structure

| Path | Purpose |
|---|---|
| `main.py` | App entry point (initializes CSVs and starts GUI) |
| `README.md` | This file |
| `CSV_Files/` | Data storage (auto-created): `College.csv`, `Program.csv`, `Student.csv` |
| `src/StudentSytemGUI.py` | Main Tkinter UI and controllers |
| `src/RanCsvGen.py` | Random data generator for colleges, programs, students |
| `src/Constraints.py` | Input validation helpers |
| `src/csv_core/` | CSV layer: `CsvRead.py`, `CsvWrite.py`, `CsvSearch.py`, `CsvSort.py`, `CsvReplace.py`, `CsvDelete.py` |

## 💡 Useful Notes

- The GUI sorts and persists CSV files via the utilities in `src/csv_core/`.
- Student ID format enforced: `YYYY-NNNN` (see `src/Constraints.py`).
- The random generator also seeds College/Program data (`src/RanCsvGen.py`).
- Sorting: click any table column header to sort (arrow shows direction); numeric parts (like year or the numeric part of `Student ID`) sort numerically.
- Multi-key search: separate keywords with spaces to intersect results across keys (e.g., `2022 Smith BSCS`).
- Left Click and Drag to Multi-Select `Student` or `Programs` to Open Mutli Delete or Transfer.

## 🗃️ CSV Data Model

The application stores data in three CSV files located in the `CSV_Files/` folder. Each file uses a header row as described below.

### `CSV_Files/College.csv`

| Column | Type | Description |
|---|---:|---|
| `College Code` | string | Short unique code (e.g., `CASS`). Used as primary key and referenced by `Program.csv`. |
| `College Name` | string | Full college name (uppercase recommended). |

### `CSV_Files/Program.csv`

| Column | Type | Description |
|---|---:|---|
| `College Code` | string | Foreign key referencing `College.csv`'s `College Code`. |
| `Program Code` | string | Unique program identifier (e.g., `BSCS`). Used as primary key and referenced by `Student.csv`. |
| `Program Name` | string | Full program name (uppercase recommended). |

### `CSV_Files/Student.csv`

| Column | Type | Description |
|---|---:|---|
| `Student ID` | string (YYYY-NNNN) | Primary key in format `YYYY-NNNN` (validated in `src/Constraints.py`). |
| `Last Name` | string | Student's last name. |
| `First Name` | string | Student's first name. |
| `Program Code` | string | Foreign key referencing `Program.csv`'s `Program Code`. |
| `Year` | integer/string | Year level (e.g., `1`, `2`, `3`). |
| `Gender` | string | `M` or `F` (stored as single-letter code). |

Notes:
- Header rows are required and automatically created by `main.py` if missing.
- `CsvRead`, `CsvWrite`, and other helpers in `src/csv_core/` assume the column order shown above.

## 📜 License

This project is licensed under the MIT License. See the full text in the [LICENSE](LICENSE) file.