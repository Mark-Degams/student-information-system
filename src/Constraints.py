def validate_code(new_code, old_code, codes):
    if new_code: new_code = new_code.lower()
    if old_code: old_code = old_code.lower()

    if codes:
        existing_codes = []
        for code in codes:
            existing_codes.append(code.lower())
    else: existing_codes = codes

    if not new_code.strip():
        return False, "Fields cannot be empty!"
    
    if new_code != old_code and new_code in existing_codes:
        return False, "Code already exists!"
    
    if len(new_code) > 10:
        return False, "Code too long (max 10)!"
    
    clean_code = new_code.replace("-", "").replace("_", "")
    if not clean_code.isalpha():
        return False, "Invalid Characters!"

    return True, "" 

def validate_name(name):
    if not name.strip():
        return False, "Fields cannot be empty!"
    
    clean_name = name.replace("-", "").replace("_", "").replace(" ", "").replace("(", "").replace(")", "")
    if not clean_name.isalpha():
        return False, "Invalid Characters"
    
    return True, ""

def validate_id(id_val, existing_ids):
    import re
    if not re.match(r"^\d{4}-\d{4}$", id_val): 
        return False, "Format must be YYYY-NNNN"
    
    if id_val in existing_ids: 
        return False, "Student ID already exists!"
    
    return True, ""