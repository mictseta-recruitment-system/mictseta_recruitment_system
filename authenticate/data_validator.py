import re

def validate_email(value):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, value):
        return False
    return True

