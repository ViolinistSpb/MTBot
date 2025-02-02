import re


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@mariinsky\.ru$"
    return bool(re.match(pattern, email))


def validate_password(password):
    pattern = r"^[A-Za-z0-9]{1,20}$"
    return bool(re.match(pattern, password))
