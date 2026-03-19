"""
Program to Work With Float List (Sum of Negative; Multiplication Between Max and Min Elements)
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 19-03-2026
"""

import user_input
from os import system
from typing import Callable


def count_sum_of_negative(lst : list[float]) -> float:
    """
    Counts Sum Of Negative Elements
    
    Args:
        lst: List of Elements

    Returns:
        float: Sum
    """

    count = 0

    for el in lst:
        if el < 0:
            count += el

    return count


# def check_list_size(func : Callable) -> Callable:
#     def wrapper(lst, *args, **kwargs):
#         if len(lst) < 2:
#             raise ValueError("Can't Calculate Multiplication: List Size Must Be More Then 1")
        
#         return func(lst, *args, **kwargs)
    
#     return wrapper


# @check_list_size
def count_multiplication(lst : list[float], count_first_appearance : bool = True) -> float:
    """
    Counts Multiplication Between Max and Min Elements
    
    Args:
        lst: List of Elements

    Returns:
        float: Multiplication
    """

    max_element = max(lst)
    min_element = min(lst)

    if count_first_appearance:
        max_element_index = lst.index(max_element)
        min_element_index = lst.index(min_element)
    else:
        max_element_index = lst[::-1].index(max_element)
        min_element_index = lst[::-1].index(min_element)

    left = min(max_element_index, min_element_index)
    right = max(max_element_index, min_element_index)

    if (right - left) < 2:
        raise ValueError("Can't Calculate Multiplication: No Elements Between Min And Max")

    result = 1
    
    for el in lst[left + 1:right]:
        result *= el

    return result


def menu() -> None:
    """
    Menu for Task_5
    """

    while True:
        try:
            system("clear")

            print("Program to Work With Float List (Sum of Negative; Multiplication Between Max and Min Elements)")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 19-03-2026")
            print()

            lst = []

            # User Input
            if(user_input.get_yes_or_no("Would You Like to Generate List? (y/n)")):
                lst_size = user_input.get_pos_int("Input List Size: ")
                lst = list(user_input.generator_float_list(lst_size))
            else:
                lst_size = user_input.get_pos_int("Input List Size: ")
                lst = user_input.get_float_list("Input List: ", lst_size)

            print("Your List: ", end = "")
            print(*lst, sep = ", ")

            answer = user_input.get_yes_or_no("Count First Appearance For Max and Min? (y/n)")
            
            # Output
            print(f"\nSum of Negative Elements: {count_sum_of_negative(lst)}") 
            print(f"\nMultiplication Between Max and Min Elements: {count_multiplication(lst, answer)}")       

        except ValueError as e:
            print(f"Value Error: {e}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not user_input.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break


# If module is executing run it
if __name__ == "__main__":
    menu()

