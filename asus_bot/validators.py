import re


def validate_email(email):
    pattern = r"^[A-Za-z.]{2,20}$"
    return bool(re.match(pattern, email))


def validate_password(password):
    pattern = r"^[^\u0400-\u04FF]{1,30}$"
    return bool(re.match(pattern, password))
