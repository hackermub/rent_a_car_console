from datetime import datetime

from .car import Car
from .user import User

class RentedCar:

    def __init__(self,car: Car,user: User,  startDate: str):
        self.car = car
        self.user = user
        self.startDate = datetime.strptime(startDate, "%d/%m/%Y %H:%M")

    def __str__(self):
        return f"* Car: {self.car.registerPlateNumber}, User: {self.user.firstName} {self.user.birthday}, Start date: {self.startDate}"
