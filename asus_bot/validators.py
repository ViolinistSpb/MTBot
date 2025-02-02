import re


def is_valid_mariinsky_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@mariinsky\.ru$"
    return bool(re.match(pattern, email))