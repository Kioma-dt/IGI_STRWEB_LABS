"""
Program to work with Numpy
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 16-04-2026
"""

from median import ManualMedian
import user_input
import numpy as np
from os import system




def menu() -> None:
    """
    Menu for Task_5
    """
        
    while True:
        try:
            system("clear")

            print("Program to work with Numpy")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 16-04-2026")
            print()

            n = user_input.get_pos_int("Input First Dimension: ")
            m = user_input.get_pos_int("Input Second Dimension: ")
            min_element = user_input.get_int("Input Min Element: ")
            max_element = user_input.get_int("Input Max Element: ")

            A = np.random.randint(min_element, max_element + 1, size=(n, m))

            print()
            print(f"Random Matrix\n{A}")
            print("Some Array: ")
            print(np.array([1,2,3,4]))
            print("\nRows: ")
            for i in range(A.shape[0]):
                print(A[i])

            print("\nColumns: ")
            for i in range(A.shape[1]):
                print(A[:,i])

            print("\nSquared: ")
            print(A**2)

            print()
            print(f"Mean: {np.mean(A)}")
            print(f"Median: {np.median(A)}")
            print(f"Correlation Coefficient:\n{np.corrcoef(A)}")
            print(f"Variation: {np.var(A)}")
            print(f"Standard Division : {np.std(A)}")

            print()
            column_sums = np.sum(A, axis=0)
            min_column_sum_index = np.argmin(column_sums)
            column_min_sum = A[:, min_column_sum_index]
            median_manual = ManualMedian.calculate(column_min_sum)
            median_numpy = np.median(column_min_sum)
            print(f"Column Sums: {column_sums}")
            print(f"Column with Min Sum: {column_min_sum}")
            print(f"Manual Median of Column with Min Sum: {median_manual}")
            print(f"NumPy Median of Column with Min Sum: {median_numpy}")




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