import time
import json
import colorama
from colorama import Fore
colorama.init(autoreset=True)
from recipes import Recipe
from user_interface import clear


class Machine:
    def __init__(self):
        self.recipes = Recipe()
        self.ingredients = self.load_ingredients()
        self.max_quantities = {
            "eggs": 6,
            "milk": 600,
            "butter": 600,
            "flour": 600,
            "sugar": 600,
            "chocolate": 600,
            "vanilla": 100,
            "water": 300,
            "soap": 50
        }

    def load_ingredients(self):
        try:
            with open("stored_ingredients.json", "r") as f:
                ingredients = json.load(f)
        except FileNotFoundError:
            ingredients = {}
        return ingredients

    def save_ingredients(self):
        with open("stored_ingredients.json", "w") as f:
            json.dump(self.ingredients, f, indent=4)

    def list_ingredients(self):
        for key, value in self.ingredients.items():
            max_quantity = self.max_quantities.get(key)
            if value >= 0.75 * max_quantity:
                print(f"{Fore.GREEN} {key.capitalize()} - I currently have {value} units available")
            if value >= 0.55 * max_quantity and value < 0.75 * max_quantity:
                print(f"{Fore.YELLOW} {key.capitalize()} - I currently have {value} units available")
            if value >= 0 and value < 0.55 * max_quantity:
                print(f"{Fore.RED} {key.capitalize()} - I currently have {value} units available")
        print(f"\n{Fore.GREEN} Green = Enough of ingredient to be used in ALL recipes - No need to refill")
        print(f"{Fore.YELLOW} Yellow = Enough of ingredient to be used in AT LEAST 1 recipe - You may need to refill")
        print(f"{Fore.RED} Red = Not enough of ingredient to be used in ANY recipes - You need to refill")

    def refill_ingredients(self):
        while True:
            self.list_ingredients()
            print("\nWhat would you like to do?")
            print("\n[1] Refill ingredient")
            print("[2] Return to Main Menu")
            decision = input("\nEnter the number of your choice: ")
            if decision == '1':
                clear()
                self.list_ingredients()
                try:
                    ingredient_to_refill = input("\nPlease enter the name of the ingredient you would like to refill\n").lower()
                    max_quantity = self.max_quantities.get(ingredient_to_refill)
                    clear()
                    if max_quantity is not None:
                        current_quantity = self.ingredients.get(ingredient_to_refill)
                        refill_amount = int(input(f"\nHow much/many {ingredient_to_refill.capitalize()} would you like to refill? I currently have {self.ingredients[ingredient_to_refill]} out of {self.max_quantities.get(ingredient_to_refill)}\n"))
                        if refill_amount >= 0:
                            if current_quantity + refill_amount <= max_quantity:
                                self.ingredients[ingredient_to_refill] += refill_amount
                                clear()
                                print("Refilling... Please Wait...")
                                time.sleep(3)
                                clear()
                                print(f"I now have {self.ingredients.get(ingredient_to_refill)} units of {ingredient_to_refill.capitalize()}\n")
                                time.sleep(3)
                                clear()
                            else:
                                print(f"I cannot store more than {max_quantity} units of {ingredient_to_refill.capitalize()}, please try again\n")
                                time.sleep(2)
                                clear()
                                self.refill_ingredients()
                        else:
                            print("Please enter a positive number greater than 0")
                            time.sleep(2)
                            clear()
                            self.refill_ingredients()
                    else:
                        print(f"\n{ingredient_to_refill} is not a valid ingredient, please try again")
                        time.sleep(2)
                        clear()
                        self.refill_ingredients()
                except ValueError:
                    print("\n -- Invalid input -- I can only accept numbers, please try again\n")
                    time.sleep(2)
                    clear()
                    self.refill_ingredients()
            elif decision == '2':
                clear()
                print("Returning to Main Menu...")
                break
            else:
                print("\n -- Invalid input -- Please enter either '1' or '2'\n")
                time.sleep(2)
                clear()
        self.save_ingredients()

    def display_treat(self,choice):
        if choice == '1':
            with open("cookie.txt", "r") as f:
                print(f.read())
        if choice == '2':
            with open("cupcake.txt", "r") as f:
                print(f.read())
        if choice == '3':
            with open("brownie.txt", "r") as f:
                print(f.read())
        if choice == '4':
            with open("muffin.txt", "r") as f:
                print(f.read())
        else:
            print("\n")
        print(f"Enjoy your {self.recipes.recipes[choice]['name'].capitalize()}\n \nReturning to Main Menu...")


    def bake_treat(self, choice):
        for ingredient, required_amount in self.recipes.recipes[choice].items():
            if ingredient in ['name', 'bake time']:
                continue
            if self.ingredients[ingredient] < required_amount:
                print(f"I do not have enough {ingredient} for {self.recipes.recipes[choice]['name'].capitalize()}. This recipe requires {required_amount} and I currently have {self.ingredients[ingredient]}, please refill this.")
                return
        print(f"Baking {self.recipes.recipes[choice]['name'].capitalize()}... Please Wait...")
        time.sleep(5)
        clear()
        print(f'*****{self.recipes.recipes[choice]['bake time']} minutes later*****')
        time.sleep(2)
        clear()
        print(f"Here are your {self.recipes.recipes[choice]['name']}")
        self.display_treat(choice)
        with open("date_last_accessed.txt", "a") as f:
            baked_good = str({self.recipes.recipes[choice]['name']})
            f.write(f"{baked_good},")
        time.sleep(8)
        # Reduce ingredient amounts
        for ingredient, required_amount in self.recipes.recipes[choice].items():
            if ingredient in ['name', 'bake time']:
                continue
            self.ingredients[ingredient] -= required_amount
        self.save_ingredients()

    
    def clean_machine(self):
        clear()
        if self.ingredients["water"] >= 100 and self.ingredients["soap"] >= 15:
            self.ingredients["water"] -= 100
            self.ingredients["soap"] -= 15
            print("Cleaning Machine with Soap and Water... Please wait...")
            time.sleep(5)
            clear()
            print("Cleaning Successful - I am now Spick and Span!")
            time.sleep(3)
            clear()
            self.save_ingredients()
            print("Returning to Main Menu...")
        else:
            print("Unable to Clean Machine :(\n")
            print("I do not have enough Water and Soap, please refill these")


