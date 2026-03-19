"""
Program to calculate sum of list element squares
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 19-03-2026
"""


import user_input
from os import system

def sum_squares(lst : list[int]) -> int:
    """
    Sums squares of the list elements
    
    Args:
        lst: List

    Returns:
        int: Squares sum
    """

    return sum((x ** 2 for x in lst))

def menu():
    """
    Menu for Task_2
    """

    while True:
        try:
            system("clear")

            print("Program to calculate sum of list element squares")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 19-03-2026")
            print()

            lst = []

            # User Input
            if(user_input.get_yes_or_no("Would you like to generate list? (y/n)")):
                lst_size = user_input.get_pos_int("Input list size: ")
                lst = list(user_input.generator_int_list(lst_size))
            else:
                lst = user_input.get_int_list("Input List: ")

            print("Your list: ", end = "")
            print(*lst, sep = ", ")
            
            # Output
            print(f"Sum of Squares: {sum_squares(lst)}")    

        except ValueError as e:
            print(f"Value Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not user_input.get_yes_or_no("\nWould you like to try again? (yes / no)"):
                break


# If module is executing run it
if __name__ == "__main__":
    menu()
