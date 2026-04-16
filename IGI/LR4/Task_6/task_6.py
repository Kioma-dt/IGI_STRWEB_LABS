"""
Program to work with Pandas
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 16-04-2026
"""

import user_input
import pandas as pd
import numpy as np
from IPython.display import display
from os import system

def menu() -> None:
    """
    Menu for Task_6
    """
        
    while True:
        try:
            system("clear")

            print("Program to work with Pandas")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 16-04-2026")
            print()

            gender_series = pd.Series(
                ['male','female','male','female','female'],
                ['P1','P2','P3','P4','P5'])
            
            display(gender_series)
            print()
            
            df = pd.read_csv("titanic.csv")

            print("Info: ")
            display(df.info())
            print()

            print("All Data:\n")
            display(df)
            print()

            age_first_class_mean = df[df["Pclass"] == 1]["Age"].mean()
            age_third_class_mean = df[df["Pclass"] == 3]["Age"].mean()

            print("The First Classes Age Mean: ")
            print(f"{age_first_class_mean:.2f}")
            print()

            print("The Third Classes Age Mean: ")
            print(f"{age_third_class_mean:.2f}")
            print()

            print("Age Ratio: ")
            print(f"{age_first_class_mean / age_third_class_mean :.2f}")


        
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