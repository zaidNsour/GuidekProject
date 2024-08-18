import re

######################## auth, user ########################
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


'''

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    return True, ""
'''
def validate_password(value):
    if not value:
        return False, 'Please enter your password'
    elif len(value) < 8:
        return False,'Password must be at least 8 characters'
    elif not re.search(r'[A-Z]', value):
        return False,'Password must contain at least one uppercase letter'
    elif not re.search(r'[0-9]', value):
        return False,'Password must contain at least one number'
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        return False,'Password must contain at least one special character'
    return True, ""
    

def validate_fullname(fullname):
    return len(fullname) >= 3

def validate_phone(phone):
    return len(phone) >= 10

def validate_number(number):
    return len(number) >= 3
######################## auth, user ########################


######################## announcements ########################
def validate_announ_title(title):
    return len(title) >= 6

def validate_announ_content(content):
    return len(content) >= 10
######################## announcements ########################


######################## transactions ########################
def validate_fee(fee):
    return isinstance(fee, float) and 0 <= fee <= 1000

def validate_expected_time(time):
    return isinstance(time, int) and 0 <= time <= 180

def validate_step_description(description):
    return len(description) >= 8

######################## transactions ########################