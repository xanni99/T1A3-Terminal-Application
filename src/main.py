from baker3000 import Machine
from recipes import Recipe
from date import Date
import user_interface as ui
import time


"""
This module contains the main function for the baker3000 Simulation.
"""
def main():
    """The main function for the baker3000 simulation"""
    ui.clear()
    ui.welcome_message()
    time.sleep(3)
    #Estabilish instances
    baker3000 = Machine()
    recipes = Recipe()
    date = Date()
    #Check if machine has been used today
    past_date = date.past_accessed_date()
    #If machine has not been used today, clean machine
    date.check_date(past_date)
    #Stores todays date in JSON file
    date.date_today()
    #Main menu loop
    while True:
        #Displays Main Menu to user
        ui.user_menu()
        #Takes user input 
        user_action = input("\n:")
        #Matches user input with feature of Baker3000 Simulation
        match user_action:
            #User selects 'Bake a Treat'
            case "1":
                ui.clear()
                choice_number = recipes.recipe_selection()
                choice = str(choice_number)
                ui.clear()
                baker3000.bake_treat(choice)
                time.sleep(6)
            #User selects 'View Supply Levels'
            case "2":
                ui.clear()
                baker3000.list_ingredients()
                print
                print("\nReturning to Main Menu in 10 seconds...")
                time.sleep(12)
            #User selects 'Refill Ingredients'
            case "3":
                ui.clear()
                baker3000.refill_ingredients()
                time.sleep(3)
            #User selects 'Add a Recipe'
            case "4":
                ui.clear()
                recipes.add_recipe()
                time.sleep(3)
            #User selects 'Clean Machine'
            case "5":
                baker3000.clean_machine()
                time.sleep(3)
            #User selects 'View Baking Log'
            case "6":
                ui.clear()
                date.print_log()
                time.sleep(3)
            #User selects 'Turn Off'
            case "7":
                ui.clear()
                ui.goodbye_message()
                time.sleep(4)
                ui.clear()
                break
            #User enters invalid input
            case _:
                print(f"\n Sorry, {user_action} is not a valid option. I can only accept 1, 2, 3, 4, 5, 6 or 7\n")
                time.sleep(4)
        

main()



