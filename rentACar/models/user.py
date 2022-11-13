from datetime import datetime

class User:
    def __init__(self, birthday: str, firstName: str, lastName: str, email: str):
        self.birthday = datetime.strptime(birthday, "%d/%m/%Y")
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def __str__(self):
        return f"* Birthday: {self.birthday}, First name: {self.firstName}, Last name: {self.lastName}, Email: {self.email}"

    def get_birthday(self):
        return datetime.strftime(self.birthday, "%d/%m/%Y")