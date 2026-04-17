"""
Program to Calculate ln((x + 1) / (x - 1)) with Macloren Series
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 16-04-2026
"""

from graphs import Graph
from series import Series
from series_stats import SeriesStats
import math
from os import system
from user_input import UserInput



def menu() -> None:
    """
    Menu for Task_3
    """
    function = lambda x: math.log((x + 1) / (x - 1))
    series_func = lambda n, x: 2 * (1 / (2 * n + 1) / math.pow(x, 2 * n + 1))
    series = Series(function, series_func)
        
    while True:
        try:
            system("clear")

            print("Program to work with regexes")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 15-04-2026")
            print()

            # Get user input
            x = UserInput.get_float("Input Function Argument: ")
            eps = UserInput.get_float("Input Precision (eps > 0): ", 0)
            max_iter = UserInput.get_pos_int("Input Max Iterations: ")

            # Calculate
            results = series.calculate(x, eps, max_iter)
            math_result = math.log((x + 1) / (x - 1))
            series_seq = list(series.series_generator(x, results[1]))
            stats = SeriesStats(series_seq)


            # Results
            Graph.print_results(x, eps, math_result, results) 
            print(stats)

            print("\nGraphical:")

            x_start = UserInput.get_float("Input Start Function Argument: ")
            x_end = UserInput.get_float("Input End Function Argument: ")
            step = UserInput.get_float("Input Step: ", 0)
            eps = UserInput.get_float("Input Precision (eps > 0): ", 0)
            max_iter = UserInput.get_pos_int("Input Max Iterations: ")

            Graph.draw(function, series_func, x_start, x_end, step, eps, max_iter)

        except IOError as e:
            print(f"Input Output Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not UserInput.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break
        

# If module is executing run it
if __name__ == "__main__":
    menu()