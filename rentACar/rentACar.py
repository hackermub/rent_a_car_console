import os 
import time 

from .database.db import DB
from .utils import utils
from .models.car import Car
from .models.user import User

class App:
    def __init__(self):
        self.db = DB()
        self.run()

    def clear(self):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    
    def run(self):
        while(True):
            self.clear()
            print("You may select one of the following:")
            print("1) List available cars")
            print("2) Rent a car")
            print("3) Return a car")
            print("4) Count the money")
            print("0) Exit")
            print("What is your selection? ", end="")

            selection = input()

            # Exit
            if selection == "0":
                self.clear()
                print("Thank you for using our service!")
                time.sleep(2)
                break
            
            # List available cars
            elif selection == "1":
                self.clear()
                print("The following cars are available:\n")
                for car in self.db.availableCars():
                    print(car)
                input("Press enter to continue...")

            # Rent a car
            elif selection == "2":
                self.clear()
                registerPlateNumber = input("Enter the register plate number of the car you want to rent: ")
                car = self.db.get_car(registerPlateNumber, includeRentedCars=False)
                if car == "Car not found":
                    print("Car not found or already rented")
                    input("Press enter to continue...")
                    continue
                
                birthday = input("Enter your birthday (dd/mm/yyyy): ")

                if not utils.validFormat(birthday):
                    print("Invalid date format, please use dd/mm/yyyy")
                    input("Press enter to continue...")
                    continue
                
                age = utils.getAge(birthday)

                if age < 18:
                    print("You are too young to rent a car")
                    input("Press enter to continue...")
                    continue
                elif age>=100:
                    print("You are too old to rent a car")
                    input("Press enter to continue...")
                    continue

                user = self.db.get_user(birthday)

                if user == "User not found":
                    firstName = input("Enter your first name: ")
                    lastName = input("Enter your last name: ")
                    email = input("Enter your email: ")

                    if not utils.validEmail(email):
                        print("Invalid email")
                        input("Press enter to continue...")
                        continue
                    
                    user = User(birthday, firstName, lastName, email)
                    self.db.add_user(user)

                rentedCar = self.db.rent_car(car, user)
                print(f"Hello {user.firstName}\nYou rented the car {rentedCar.car.registerPlateNumber}")
                input("Press enter to continue...")
                continue

            # Return a car
            elif selection == "3":
                self.clear()
                registerPlateNumber = input("Enter the register plate number of the car you want to return: ")
                
                car = self.db.get_car(registerPlateNumber, includeRentedCars=True)

                if car == "Car not found":
                    print("Car not found")
                    input("Press enter to continue...")
                    continue

                rentedCar = self.db.is_rented(car)
                if not rentedCar:
                    print("Car not rented")
                    input("Press enter to continue...")
                    continue
                print(rentedCar)
                self.db.return_car(rentedCar)
                input("Press enter to continue...")
                continue
            
            # Count the money
            elif selection == "4":
                self.clear()
                total = self.db.load_transactions()
                print(f"The total amount of money is {total} euros")
                input("Press enter to continue...")
                continue