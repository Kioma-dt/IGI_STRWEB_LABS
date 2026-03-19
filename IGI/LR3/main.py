"""
Main Menu
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 19-03-2026
"""


import task_1
import task_2
import task_3
import task_4
import task_5
from os import system


def main_menu() -> None:
    """
    Main Menu For All Tasks
    """

    while True:
        try:
            system("clear")
            print("Main Menu")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 19-03-2026")
            print()

            print("Choose Menu Option:")
            print("1. Run Task_1")
            print("2. Run Task_2")
            print("3. Run Task_3")
            print("4. Run Task_4")
            print("5. Run Task_5")
            print("6. Exit")

            option = input()

            match option:
                case "1":
                    task_1.menu()
                case "2":
                    task_2.menu()
                case "3":
                    task_3.menu()
                case "4":
                    task_4.menu()
                case "5":
                    task_5.menu()
                case "6":
                    return
                case _:
                    raise ValueError("Wrong Option Format!")

        except ValueError as error:
            print(f"Value Error: {error}")
            print("Press Enter...")
            input()

        except Exception as error:
            print(f"Error: {error}")
            print("Press Enter...")
            input()            


# If module is executing run it
if __name__ == "__main__":
    main_menu()
