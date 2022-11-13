from datetime import datetime
import re

def validFormat(date):
    try:
        datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def getAge(date):
    date = datetime.strptime(date, "%d/%m/%Y")
    today = datetime(2022,12,31) 
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return int(age)

def validEmail(email):
    # check if the email is valid using regex
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

