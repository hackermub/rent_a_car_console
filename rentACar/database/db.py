from datetime import datetime

from rentACar.models.car import Car
from rentACar.models.user import User
from rentACar.models.rentedCars import RentedCar

class DB:

    FILE_PATH = "rentACar/database/files/"

    def __init__(self) -> None:
        self.cars = self.load_cars()
        self.users = self.load_users()
        self.rentedCars = self.load_rented_cars()

    def load_cars(self):
        # Load cars from file Vehicles.txt
        with open(DB.FILE_PATH+"Vehicles.txt", "r") as file:
            lines = file.readlines()
            cars = []
            for line in lines:
                car = line.split(",")
                cars.append(Car(car[0], car[1], car[2], car[3:]))
            return cars

    def load_users(self):
        # Load users from file Customers.txt
        with open(DB.FILE_PATH+"Customers.txt", "r") as file:
            lines = file.readlines()
            users = []
            for line in lines:
                user = line.split(",")
                users.append(User(user[0], user[1], user[2], user[3].rstrip()))
            return users

    def load_rented_cars(self):
        # Load rented cars from file rentedVehicles.txt
        with open(DB.FILE_PATH+"rentedVehicles.txt", "r") as file:
            lines = file.readlines()
            rentedCars = []
            for line in lines:
                car = line.split(",")
                rentedCars.append(RentedCar(self.get_car(car[0]), self.get_user(car[1]), car[2].rstrip()))
            return rentedCars

    def load_transactions(self):
        # Load transactions from file transActions.txt
        total = 0
        with open(DB.FILE_PATH+"transActions.txt", "r") as file:
            lines = file.readlines()
            transactions = []
            for line in lines:
                transaction = line.split(",")
                total+= float(transaction[5])
        return total

    def availableCars(self):
        # Return a list of all available cars
        availableCars = {car.registerPlateNumber for car in self.cars}
        for rentedCar in self.rentedCars:
            availableCars.remove(rentedCar.car.registerPlateNumber)

        return [self.get_car(car) for car in availableCars]   

    def get_car(self, registerPlateNumber, includeRentedCars=True):
        # Return a car object with the given register plate number
        cars = self.cars if includeRentedCars else self.availableCars()
        for car in cars:
            if car.registerPlateNumber == registerPlateNumber:
                return car
        return "Car not found"

    def get_user(self,birthday):
        # Return a user object with the given birthday
        for user in self.users:
            if user.get_birthday() == birthday:
                return user
        return "User not found"

    def add_user(self, user: User):
        # Add a user to the database
        self.users.append(user)
        with open(DB.FILE_PATH+"Customers.txt", "a") as file:
            file.write(f"{user.get_birthday()},{user.firstName},{user.lastName},{user.email}")
    
    def rent_car(self, car: Car, user: User):
        # Rent a car
        rentedCar = RentedCar(car, user, datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.rentedCars.append(rentedCar)
        with open(DB.FILE_PATH+"rentedVehicles.txt", "a") as file:
            file.write(f"{car.registerPlateNumber},{user.get_birthday()},{datetime.now().strftime('%d/%m/%Y %H:%M')}")

        return rentedCar

    def is_rented(self, car: Car):
        # Check if a car is rented
        for rentedCar in self.rentedCars:
            if rentedCar.car.registerPlateNumber == car.registerPlateNumber:
                return rentedCar
        return False
    
    def return_car(self, rentedCar: RentedCar):
        # Return a car
        
        endDate = datetime.now()
        days = (endDate - rentedCar.startDate).days
        price = float(days * rentedCar.car.dailyRate)


        with open(DB.FILE_PATH+"transActions.txt", "a") as file:
            file.write(f"{rentedCar.car.registerPlateNumber},{rentedCar.user.get_birthday()},{rentedCar.startDate.strftime('%d/%m/%Y %H:%M')},{endDate.strftime('%d/%m/%Y %H:%M')},{days},{price}\n")
        
        self.rentedCars.remove(rentedCar)
        with open(DB.FILE_PATH+"rentedVehicles.txt", "w") as file:
            file.truncate()
            for rentedCar in self.rentedCars:
                file.write(f"{rentedCar.car.registerPlateNumber},{rentedCar.user.get_birthday()},{rentedCar.startDate.strftime('%d/%m/%Y %H:%M')}\n")


        print(f"The rent lasted {days} days and the cost is {price} euros")