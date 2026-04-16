"""
Program to work with Figures
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 16-04-2026
"""

from color import Color
from figures import IsoscelesTriangle
import math
from os import system
import user_input



def menu() -> None:
    """
    Menu for Task_4
    """
        
    while True:
        try:
            system("clear")

            print("Program to work with Figures")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 16-04-2026")
            print()

            a = user_input.get_float("Input Side: ", 0)
            h = user_input.get_float("Input Height: ", 0)
            print("Input Color: ", end='')
            color = Color(input())

            triangle = IsoscelesTriangle(a, h, color)
            print()
            print(triangle)
            triangle.draw()
            
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