import re

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    return True, ""

def validate_fullname(fullname):
    return len(fullname) >= 3

def validate_phone(fullname):
    return len(fullname) >= 10

def validate_announ_title(title):
    return len(title) >= 6

def validate_announ_content(content):
    return len(content) >= 10