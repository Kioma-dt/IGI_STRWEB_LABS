"""
Program to Calculate Number of Capital Letters in String
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 19-03-2026
"""

from os import system
import user_input

# Set of All Capital Letters
capital_letters = set("QWERTYUIOPASDFGHJKLZXCVBNMЙЦУКЕНГШЩЗХЪЁФЫВАПРОЛДЖЭЯЧСМИТЬБЮ")

def count_capital_letters(string : str) -> int:
    """
    Get Number of Capital Letters
    
    Args:
        string: Checkable String

    Returns:
        int: Number of Capital Letters
    """

    count = 0

    for ch in string:
        count += (ch in capital_letters)

    return count


def menu() -> None:
    """
    Menu for Task_3
    """

    while True:
        try:
            system("clear")

            print("Program to Calculate Number of Capital Letters in String")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 19-03-2026")
            print()

            # User Input
            string = input("Input Some String: ")
            
            # Output
            print(f"Number of Capital Letters: {count_capital_letters(string)}")    

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


